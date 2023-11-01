'''
Author: xuarehere
Date: 2022-12-28 15:59:30
LastEditTime: 2023-01-09 11:43:44
LastEditors: xuarehere
Description: 
FilePath: /special_site_2d_220801/select_class_move.py
'''

import os
import xml.etree.ElementTree as ET
import cv2
# from plots import Annotator, colors, save_one_box
import copy
import shutil
def write_data(file_path, str_list, mode='a', encoding='utf-8'):
    with open(file_path, mode, encoding=encoding) as fp:
        for item in str_list:
            fp.writelines(item)
            fp.flush()
class Select_labels:
    def __init__(self) -> None:
        # self.root_path = '/workspace/dataset/special_site_2d_220801/'
        self.root_path = os.getcwd()
        self.imgdir =       "VOC2007/JPEGImages"
        self.labdir_xmls =  "VOC2007/Annotations"
        self.labdir_txts =  "VOC2007/labels"
        self.output_dir = "./output_selected"
        
        self.save_move_info_file = "./move_info.py"       # 保存移动的信息
        self.write_info = []
        
        self.sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
        self.select_classes={
                    'BigTruck': 0.3, 
                    'GarbageTruck': 0.3, 
                    'MuckTruck': 0.3, 
                    'Truck': 0.1,
            } # 类别，选中的数量比例
        self.clscountdict = {}
        self.selected_nums={
                    'Ambulance': 0, 
                    'BigTruck': 0, 
                    'Bus': 0, 
                    'Car': 0, 
                    'CoachesCar': 0, 
                    'Cycle': 0, 
                    'DangerousCar': 0, 
                    'DangerousTruck': 0, 
                    'FireTruck': 0, 
                    'GarbageTruck': 0, 
                    'MuckTruck': 0, 
                    'Pedestrian': 0, 
                    'PoliceCar': 0, 
                    'Tanker': 0, 
                    'TourBus': 0, 
                    'Truck': 0,
            } # 统计所有类别信息
        self.check_mkdirs(self.output_dir)
        

        pass
    

    def run(self):
        self.write_info.append('#"set information"\n')
        self.write_info.extend(["select_classes = " + str(self.select_classes) + "\n"])        
        self.get_clscountdict()
        self.write_info.extend(["select_classes_nums = " + str(self.select_classes) + "\n"])        
        
        self.move_select_xmls_labels()
        
        self.write_info.append('#"actually move information"\n')        
        self.write_info.extend(["move_nums = " + str(self.selected_nums) + "\n"])        

        
        write_data(self.save_move_info_file, self.write_info, mode='w')
        
    
    def check_mkdirs(self, dir_path):
        if not os.path.exists(path=dir_path):
            os.makedirs(dir_path)

    def get_clscountdict(self):
        """
        统计数量，根据比例，获取数量
        """
        imgdir =      os.path.join(self.root_path, self.imgdir)
        labdir_xmls = os.path.join(self.root_path, self.labdir_xmls)
        labdir_txts = os.path.join(self.root_path, self.labdir_txts)         
        image_files = os.listdir( imgdir)  # sorted()
        line_thickness = 3
        miss_img_list = []
        miss_lab_list = []
        select_classes= self.select_classes
        for index, image in enumerate(image_files):
            image_path = os.path.join(imgdir, image)
            label_path = os.path.join(labdir_xmls, image[:-4] + ".xml" )        
            if os.path.exists(image_path)==False or os.path.exists(label_path)==False:
                if os.path.exists(image_path)==False:
                    miss_img_list.append(image_path)
                if os.path.exists(label_path)==False:    
                    miss_lab_list.append(label_path)
                continue            
            label_content = self.convert_annotation(label_path, select_classes=list(select_classes.keys()))
        
        # generate select nums
        for key, values in self.clscountdict.items():
            self.select_classes[key] = int(self.select_classes[key]*values)
        
        pass
    
    def move_select_xmls_labels(self):
        """
        筛选出对应的类别
        """
        is_move_miss_files = True
        select_classes = copy.deepcopy( self.select_classes)        # 需要选中的信息
        select_nums_dict = copy.deepcopy( self.selected_nums)       # 统计所有选中的数量
        # 新的保存目录
        new_imgdir =      os.path.join(self.output_dir, self.imgdir)
        new_labdir_xmls = os.path.join(self.output_dir, self.labdir_xmls)
        new_labdir_txts = os.path.join(self.output_dir, self.labdir_txts)
        self.check_mkdirs(new_imgdir)
        self.check_mkdirs(new_labdir_xmls)
        self.check_mkdirs(new_labdir_txts)
        
        # 原始的
        imgdir =      os.path.join(self.root_path, self.imgdir)
        labdir_xmls = os.path.join(self.root_path, self.labdir_xmls)
        labdir_txts = os.path.join(self.root_path, self.labdir_txts) 
        image_files = os.listdir(imgdir)  # sorted()
                
        miss_img_list = []
        miss_lab_list = []
        
        # flag 
        is_move = False
        move_id_list = []
        for index, image in enumerate(image_files):
            file_id = image[:-4] 
            image_path = os.path.join(imgdir, image)
            label_path = os.path.join(labdir_xmls, file_id + ".xml" )
            latxt_path = os.path.join(labdir_txts, file_id + ".txt" )
            
            if os.path.exists(image_path)==False or os.path.exists(label_path)==False:
                if os.path.exists(image_path)==False:
                    miss_img_list.append(image_path)
                if os.path.exists(label_path)==False:    
                    miss_lab_list.append(label_path)
                    
                # if is_move_miss_files:      # 移除丢失的文件
                #     shutil.move(image_path, new_imgdir)                 
                continue
            
            if index %100==0:
                print("index: {}, img:{}".format(index, image_path))   
                
            is_move, select_classes = self.convert_annotation_move(label_path, select_classes=list(select_classes.keys()), select_classes_dict=select_classes)
            if is_move:
                move_id_list.append(file_id)
                select_nums_dict = self.count_class_nums(label_path, count_classes_dict=select_nums_dict,)
                shutil.move(image_path, new_imgdir)
                shutil.move(label_path, new_labdir_xmls)
                shutil.move(latxt_path, new_labdir_txts)
            if select_classes =={}:
                break
            
            pass
        self.selected_nums = select_nums_dict
        
        pass
        
    
    def convert_annotation_move(self, in_file_root, select_classes=[], is_xmin_ymin_xmax_ymax=True, select_classes_dict={}):
        """
        用于分析是否 move
        """
        
        # in_file_root = os.path.join(self.root_path,'VOC%s/Annotations/%s.xml'%(year, image_id))
        # out_file_root = os.path.join(self.root_path,'VOC%s/labels/%s.txt'%(year, image_id))
        ret = []
        in_file = open(in_file_root)
        # out_file = open(out_file_root, 'w')
        tree=ET.parse(in_file)
        root = tree.getroot()
        site = root.find('site')
        w = int(site.find('width').text)
        h = int(site.find('height').text)    
        for obj in root.iter('object'):
            ele = []
            # difficult = obj.find('difficult').text
            cls = obj.find('name').text
            # if cls in self.selected_nums.keys():
            #     self.selected_nums[cls] = self.selected_nums[cls] + 1
            # else:
            #     self.selected_nums[cls] = 1
                            
            # if cls not in classes or int(difficult)==1:
            #     continue
            if cls not in select_classes:
                continue
            else:
                # 计算是否移动的数量
                select_classes_dict[cls] -=1
                if select_classes_dict[cls] <0:
                    del select_classes_dict[cls]
                    select_classes = list(select_classes_dict.keys())
                    continue
                    
            # if cls not in self.clscountdict.keys():
            #     self.clscountdict[cls] = 1
            # else:
            #     self.clscountdict[cls] = self.selected_nums[cls] + 1
            

            # cls_id = self.select_classes.index(cls)
            xmlbox = obj.find('bndbox')
            if is_xmin_ymin_xmax_ymax:
                bb = [float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymax').text)]
            else:
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = self.convert((w,h), b)
            ele.append(cls)
            ele.extend([a for a in bb])
            ret.append(ele)
            # out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        return (False, select_classes_dict) if ret ==[] else (True, select_classes_dict)
        # return ret
    
    def count_class_nums(self, in_file_root, count_classes_dict={}):
        # in_file_root = os.path.join(self.root_path,'VOC%s/Annotations/%s.xml'%(year, image_id))
        # out_file_root = os.path.join(self.root_path,'VOC%s/labels/%s.txt'%(year, image_id))
        ret = []
        in_file = open(in_file_root)
        # out_file = open(out_file_root, 'w')
        tree=ET.parse(in_file)
        root = tree.getroot()
        site = root.find('site')
        w = int(site.find('width').text)
        h = int(site.find('height').text)    
        for obj in root.iter('object'):
            ele = []
            # difficult = obj.find('difficult').text
            cls = obj.find('name').text
            # if cls not in classes or int(difficult)==1:
            #     continue
            # if cls not in select_classes:
            #     continue
            if cls not in count_classes_dict.keys():
                count_classes_dict[cls] = 1
            else:
                count_classes_dict[cls] = count_classes_dict[cls] + 1
            # cls_id = self.select_classes.index(cls)
        #     xmlbox = obj.find('bndbox')
        #     if is_xmin_ymin_xmax_ymax:
        #         bb = [float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymax').text)]
        #     else:
        #         b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        #         bb = self.convert((w,h), b)
        #     ele.append(cls)
        #     ele.extend([a for a in bb])
        #     ret.append(ele)
        #     # out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        # return ret
        return count_classes_dict

    
    # def get_all_imgs_labels(self):
    #     # for year, image_set in self.sets:
    #     # if not os.path.exists(os.path.join(self.root_path,'VOC%s/labels/'%(year))):
    #     #     os.makedirs(os.path.join(self.root_path,'VOC%s/labels/'%(year)))
    #     # image_ids_root = os.path.join(self.root_path,'VOC%s/ImageSets/Main/%s.txt'%(year, image_set))    
    #     # image_ids = open(image_ids_root).read().strip().split()
    #     # list_file_root = os.path.join(self.root_path,'%s_%s.txt'%(year, image_set))
    #     # list_file = open(list_file_root, 'w')

    #     imgdir =      os.path.join(self.root_path, self.imgdir)
    #     labdir_xmls = os.path.join(self.root_path, self.labdir_xmls)
    #     labdir_txts = os.path.join(self.root_path, self.labdir_txts) 
    #     image_files = os.listdir(imgdir)  # sorted()
    #     line_thickness = 3
    #     miss_img_list = []
    #     miss_lab_list = []
    #     for index, image in enumerate(image_files):
    #         image_path = os.path.join(imgdir, image)
    #         label_path = os.path.join(labdir_xmls, image[:-4] + ".xml" )
    #         if os.path.exists(image_path)==False or os.path.exists(label_path)==False:
    #             if os.path.exists(image_path)==False:
    #                 miss_img_list.append(image_path)
    #             if os.path.exists(label_path)==False:    
    #                 miss_lab_list.append(label_path)
    #             continue
    #         if index %100==0:
    #             print("index: {}, img:{}".format(index, image_path))          

    #         # write_str = os.path.join(self.root_path,'VOC%s/JPEGImages/%s.jpg\n'%(year, image_id))
    #         # list_file.write(write_str)
    #         # if self.select_classes == []:
    #         #     pass
    #         # else:
    #         for select in self.select_classes:
    #             path = image_path
    #             im0 = cv2.imread(path)  # BGR
    #             assert im0 is not None, f'Image Not Found {path}'
    #             # s = f'image {self.count}/{self.nf} {path}: '            
    #             self.annotator = Annotator(im0, line_width=line_thickness, example=str(select))
                
    #             label_content = []
                
    #             write_img_path = os.path.join(self.output_dir, select)
    #             self.check_mkdirs(write_img_path)
    #             write_img_path = os.path.join(write_img_path, image)
                
    #             label_content = self.convert_annotation(label_path, [select])
    #             if label_content!=[]:
    #                 self.write_to_img(write_img_path,labels=label_content)
    #     # list_file.close()
    #     print("miss files,\n", miss_img_list, miss_lab_list)
    #     pass
    
    # def generate_select_imges_labels(self):
    #     pass
    
    # def write_to_img(self, img_path, labels=[]):
    #     for ele in labels:
    #         label = ele[0]
    #         xyxy = ele[1:]
    #         # c = int(cls)  # integer class
    #         # labels = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
    #         # annotator.box_label(xyxy, label, color=colors(c, True))        
    #         self.annotator.box_label(xyxy, label, color=(255,0,0))        
    #     cv2.imwrite(img_path, self.annotator.im)    
    #     pass
    
        
    def convert_annotation(self, in_file_root, select_classes=[], is_xmin_ymin_xmax_ymax=True):
        # in_file_root = os.path.join(self.root_path,'VOC%s/Annotations/%s.xml'%(year, image_id))
        # out_file_root = os.path.join(self.root_path,'VOC%s/labels/%s.txt'%(year, image_id))
        ret = []
        in_file = open(in_file_root)
        # out_file = open(out_file_root, 'w')
        tree=ET.parse(in_file)
        root = tree.getroot()
        site = root.find('site')
        w = int(site.find('width').text)
        h = int(site.find('height').text)    
        for obj in root.iter('object'):
            ele = []
            # difficult = obj.find('difficult').text
            cls = obj.find('name').text
            # if cls not in classes or int(difficult)==1:
            #     continue
            if cls not in select_classes:
                continue
            if cls not in self.clscountdict.keys():
                self.clscountdict[cls] = 1
            else:
                self.clscountdict[cls] = self.clscountdict[cls] + 1
            # cls_id = self.select_classes.index(cls)
            xmlbox = obj.find('bndbox')
            if is_xmin_ymin_xmax_ymax:
                bb = [float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymax').text)]
            else:
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = self.convert((w,h), b)
            ele.append(cls)
            ele.extend([a for a in bb])
            ret.append(ele)
            # out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        return ret

    def convert(self, site, box):
        dw = 1./(site[0])
        dh = 1./(site[1])
        x = (box[0] + box[1])/2.0 - 1
        y = (box[2] + box[3])/2.0 - 1
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x,y,w,h)        

def main():
    start = Select_labels()
    start.run()
    pass




if __name__ == '__main__':
    main()
