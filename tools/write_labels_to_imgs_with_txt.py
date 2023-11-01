'''
Author: xuarehere
Date: 2022-12-23 19:58:00
LastEditTime: 2023-11-01 17:24:04
LastEditors: xuarehere xuarehere@sutpc.com
Description: 把每一类的标注信息单独绘制到图片中
FilePath: /suiDaoShiJian/tools/write_labels_to_imgs_with_txt.py

yolo 格式中，将标签可视化到图片上
'''
import os
import xml.etree.ElementTree as ET
import cv2
from plots import Annotator, colors, save_one_box
import collections

class Write_imgs_labels:
    def __init__(self) -> None:

        self.root_path = '/workspace/dataset/suiDaoShiJian/'
        # self.root_path = os.getcwd()        
        self.output_dir = "./output"
        self.sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
        self.labels_dict = collections.OrderedDict([(0, 'Bus'), (1, 'Car'), (2, 'Truck'), (3, 'BigTruck'), (4, 'DangerousTruck'), (5, 'Box'), (6, 'Other'), (7, 'MiniBus'), (8, 'VanTruck'), (9, 'Person'), (10, 'Coness'), (11, 'MotorCycle'), (12, 'Tire'), (13, 'Head')])
        self.select_classes=[
                        'Bus',
                        'Car',
                        'Truck',
                        'BigTruck',
                        'DangerousTruck',
                        'Box',
                        'Other',
                        'MiniBus',
                        'VanTruck',
                        'Person',
                        'Coness',
                        'MotorCycle',
                        'Tire',
                        'Head',
                        ]
        self.clscountdict = {}
        self.check_mkdirs(self.output_dir)
        pass
    

    def run(self):
        self.get_all_imgs_labels()

    
    def check_mkdirs(self, dir_path):
        if not os.path.exists(path=dir_path):
            os.makedirs(dir_path)
            
    def get_all_imgs_labels(self):
        # for year, image_set in self.sets:
        # if not os.path.exists(os.path.join(self.root_path,'VOC%s/labels/'%(year))):
        #     os.makedirs(os.path.join(self.root_path,'VOC%s/labels/'%(year)))
        # image_ids_root = os.path.join(self.root_path,'VOC%s/ImageSets/Main/%s.txt'%(year, image_set))    
        # image_ids = open(image_ids_root).read().strip().split()
        # list_file_root = os.path.join(self.root_path,'%s_%s.txt'%(year, image_set))
        # list_file = open(list_file_root, 'w')
        imgdir = os.path.join(self.root_path, "VOC2007/JPEGImages")
        labdir = os.path.join(self.root_path, "VOC2007/labels")
        image_files = os.listdir( imgdir)  # sorted()
        line_thickness = 3
        miss_img_list = []
        miss_lab_list = []
        for index, image in enumerate(image_files):
            image_path = os.path.join(imgdir, image)
            label_path = os.path.join(labdir, image[:-5] + ".txt" )
            if os.path.exists(image_path)==False or os.path.exists(label_path)==False:
                if os.path.exists(image_path)==False:
                    miss_img_list.append(image_path)
                if os.path.exists(label_path)==False:    
                    miss_lab_list.append(label_path)
                continue
            if index %100==0:
                print("index: {}, img:{}".format(index, image_path))          

            
            # write_str = os.path.join(self.root_path,'VOC%s/JPEGImages/%s.jpg\n'%(year, image_id))
            # list_file.write(write_str)
            # if self.select_classes == []:
            #     pass
            # else:
            for select in self.select_classes:
                path = image_path
                im0 = cv2.imread(path)  # BGR
                assert im0 is not None, f'Image Not Found {path}'
                # s = f'image {self.count}/{self.nf} {path}: '            
                self.annotator = Annotator(im0, line_width=line_thickness, example=str(select))
                
                label_content = []
                
                write_img_path = os.path.join(self.output_dir, select)
                self.check_mkdirs(write_img_path)
                write_img_path = os.path.join(write_img_path, image)
                
                # label_content = self.convert_annotation(label_path, [select])
                label_content = self.convert_txt(label_path, [select],im0.shape)
                if label_content!=[]:
                    self.write_to_img(write_img_path,labels=label_content)
                    
        # list_file.close()
        print("miss files,\n", miss_img_list, miss_lab_list)
        pass
    
    def generate_select_imges_labels(self):
        pass
    
    def write_to_img(self, img_path, labels=[]):
        for ele in labels:
            label = ele[0]
            xyxy = ele[1:]
            # c = int(cls)  # integer class
            # labels = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
            # annotator.box_label(xyxy, label, color=colors(c, True))        
            self.annotator.box_label(xyxy, label, color=(255,0,0))        
        cv2.imwrite(img_path, self.annotator.im)    
        pass
    
    def convert_annotation(self, in_file_root, select_classes=[], is_xmin_ymin_xmax_ymax=True):
        # in_file_root = os.path.join(self.root_path,'VOC%s/Annotations/%s.xml'%(year, image_id))
        # out_file_root = os.path.join(self.root_path,'VOC%s/labels/%s.txt'%(year, image_id))
        ret = []
        in_file = open(in_file_root)
        # out_file = open(out_file_root, 'w')
        tree=ET.parse(in_file)
        root = tree.getroot()
        # site = root.find、('site')
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

    def covner_xywh2x1y1x2y2(self, box=[], image_shape=[]):
        x, y, w, h = box
        image_height, image_width, _ = image_shape
        x_pixel = int(x * image_width)
        y_pixel = int(y * image_height)
        w_pixel = int(w * image_width)
        h_pixel = int(h * image_height)

        # x1y1-----------
        # |              |
        # |              |
        # |              |
        # |              |
        # ---------------x2y2

        x1,y1 = x_pixel - w_pixel//2, y_pixel- h_pixel//2
        x2,y2 = x_pixel + w_pixel//2, y_pixel + h_pixel//2       
        return [x1,y1,x2,y2] 
    
    def convert_txt(self,label_path, select_classes, image_shape):
        ret = []
        file =open(label_path, 'r')
        for line in file:
            ele = []
            line = line.strip()
            line = [float(item) for item in line.split()]
            
            cls = self.labels_dict[int(line[0])]
            if cls not in select_classes:
                continue
            if cls not in self.clscountdict.keys():
                self.clscountdict[cls] = 1
            else:
                self.clscountdict[cls] = self.clscountdict[cls] + 1            

            bb = self.covner_xywh2x1y1x2y2(line[1:], image_shape=image_shape)
            
            ele.append(cls)
            ele.extend([a for a in bb])
            ret.append(ele)                
        return ret
        pass
    
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
    start = Write_imgs_labels()
    start.run()
    pass




if __name__ == '__main__':
    main()
