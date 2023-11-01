'''
Author: xuarehere
Date: 2022-12-30 15:51:25
LastEditTime: 2023-01-05 15:10:10
LastEditors: xuarehere
Description: 类别合并、映射、丢弃
FilePath: /voc_2007_2012_Pedestrain/merge_labels.py

'''
import glob
from pathlib import Path
import os
from re import S
import shutil 



def img2label_paths(img_paths):
    # Define label paths as a function of image paths
    # ----------- start: default ----------- 
    # sa, sb = os.sep + 'images' + os.sep, os.sep + 'labels' + os.sep  # /images/, /labels/ substrings          # default
    # sa = '/images/'
    # sb  = '/labels/'
    # ----------- end: default ----------- 

    # img_paths[0]= '../coco128/images/train2017/000000000443.jpg'
    # ----------- start: baoao ----------- 
    sa, sb = os.sep + 'JPEGImages' + os.sep, os.sep + 'labels' + os.sep  # /images/, /labels/ substrings        # baoao, xuarehere
    # ----------- end: baoao -----------     
    #               '../coco128/labels/train2017/000000000009.txt'
    return [x.replace(sa, sb, 1).replace('.' + x.split('.')[-1], '.txt') for x in img_paths]

def img2xml_paths(img_paths):
    # Define label paths as a function of image paths
    # ----------- start: default ----------- 
    # sa, sb = os.sep + 'images' + os.sep, os.sep + 'labels' + os.sep  # /images/, /labels/ substrings          # default
    # sa = '/images/'
    # sb  = '/labels/'
    # ----------- end: default ----------- 

    # img_paths[0]= '../coco128/images/train2017/000000000443.jpg'
    # ----------- start: baoao ----------- 
    sa, sb = os.sep + 'JPEGImages' + os.sep, os.sep + 'Annotations' + os.sep  # /images/, /labels/ substrings        # baoao, xuarehere
    # ----------- end: baoao -----------     
    #               '../coco128/labels/train2017/000000000009.txt'
    return [x.replace(sa, sb, 1).replace('.' + x.split('.')[-1], '.xml') for x in img_paths]



def write_data(file_path, str_list, mode='a', encoding='utf-8'):
    with open(file_path, mode, encoding=encoding) as fp:
        for item in str_list:
            fp.writelines(item)
            fp.flush()
            
def read_file(file_path, mode='r', encoding='utf-8'):
    with open(file_path, mode, encoding=encoding) as fp:
        # for item in str_list:
        #     fp.writelines(item)
        #     fp.flush()          
        ret = fp.readlines()
        return ret
        
def rm_file(rm_list, is_print=True):
    if is_print:
        print("remove files:", rm_list)
    for file in rm_list:
        if os.path.isdir(file):
            os.removedirs(file)
        else:
            os.remove(file)
        
def cp_file(source_file, destination_file, new_name=""):
    save_name = ""
    save_path = None
    if new_name == "":
        save_name = str.split(source_file, os.path.sep)[-1]
    else:
        save_name = new_name
        
    if os.path.isdir(destination_file):
        save_path = os.path.join( destination_file, save_name)
    else:
        save_path = destination_file
    shutil.copyfile(source_file, save_path)
    
def move_file(source_file, destination_file, new_name=""):
    # check_list = ["frame_000367.txt", 
    #             #   "004623.txt", "000763.txt", "000367.txt", "004450.txt", "004451.txt", "003662.jpg", "003663.jpg", "003664.jpg", "003665.jpg", 
    #                 ]
    # if str.split(source_file, os.path.sep)[-1] in check_list:
    #     print("check file===>")    
    save_name = ""
    save_path = None
    if new_name == "":
        save_name = str.split(source_file, os.path.sep)[-1]
    else:
        save_name = new_name
        
    if os.path.isdir(destination_file):
        save_path = os.path.join( destination_file, save_name)
    else:
        save_path = destination_file
    shutil.move(source_file, save_path)
    
            
class DataOpts:
    def __init__(self) -> None:
        # label_path = "/workspace/dataset/special_site_jiaolian_add_site1_special_vehicle_count/VOC2007/labels"
        # path = '/workspace/dataset/special_site_jiaolian_add_site1_special_vehicle_count/VOC2007/JPEGImages/'
        # path = "./VOC2007/JPEGImages/"
        self.init_param()
        path = ["./VOCdevkit/VOC2007/JPEGImages",
                "./VOCdevkit/VOC2012/JPEGImages"
                ]
        
        self.save_dir = "./tmp/"   
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
        img_formats = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng']
        try:
            f = []  # image files
            for p in path if isinstance(path, list) else [path]:
                p = Path(p)  # os-agnostic
                if p.is_dir():  # dir
                    f += glob.glob(str(p / '**' / '*.*'), recursive=True)
                elif p.is_file():  # file
                    with open(p, 'r') as t:
                        t = t.read().strip().splitlines()
                        parent = str(p.parent) + os.sep
                        f += [x.replace('./', parent) if x.startswith('./') else x for x in t]  # local to global path
                else:
                    raise Exception('%s does not exist' % p)
            self.img_files = sorted([x.replace('/', os.sep) for x in f if x.split('.')[-1].lower() in img_formats])
            assert self.img_files, 'No images found'
        except Exception as e:
            raise Exception('Error loading data from %s: %s\n' % (path, e))
        
        self.label_files = img2label_paths(self.img_files)  # labels
        self.xml_files = img2xml_paths(self.img_files)  # xmls
        
    def init_param(self):
        # 原始参数信息
        # self.old_labels = ["Car", "Bus", "Cycle", "Pedestrian", "Truck", "TourBus", "DangerousTruck", "PoliceCar", "FireTruck", "Ambulance", "BigTruck", "Tanker", "TestCar", "OfficialCar", "DangerousCar", "GarbageTruck", "MuckTruck", "CoachesCar"]
        self.old_labels = ["aeroplane", 
                        "bicycle", 
                        "bird", 
                        "boat", 
                        "bottle", 
                        "bus", 
                        "car", 
                        "cat", 
                        "chair", 
                        "cow", 
                        "diningtable", 
                        "dog", 
                        "horse", 
                        "motorbike", 
                        "person", 
                        "pottedplant", 
                        "sheep", 
                        "sofa", 
                        "train", 
                        "tvmonitor"] # voc 原来的类别
        self.old_labels_index = list(range(len(self.old_labels)))
        self.old_labels_index = dict(zip(self.old_labels_index, self.old_labels) )# id: label
        
        # 新的参数信息
        self.new_labels = ["Bus",
                            "Car" ,
                            "Cycle" , 
                            "Pedestrian" , 
                            "Truck",
                            "BigTruck",
                            "Tanker",
                            "GarbageTruck",
                            "MuckTruck",
                            "CoachesCar",]  # 不在这里面就被抛弃
        self.new_labels_index = list(range(len(self.new_labels)))
        self.new_labels_index = dict(zip(self.new_labels_index, self.new_labels)) # id: label        
        self.merge_labels = {
            "Bus": ["TourBus",  ],
            "Car": ["PoliceCar", "Ambulance","TestCar", "OfficialCar", "DangerousCar", ],
            "Cycle": [], 
            "Pedestrian": ["person"], 
            "Truck": ["DangerousTruck", "FireTruck", ],
            "BigTruck": [],
            "Tanker": [],
            "GarbageTruck":[],
            "MuckTruck": [],
            "CoachesCar": [],
        }        
        pass
    
    pass

    def piplie(self):
        self.change_to_new_labels()
        # self.change_file_to_new_label(None)
        pass
    
    
    def change_file_to_new_label(self, path, is_print=True):
        """
        进行 id 转化
            在映射列表中，进行id 映射
            不在映射列表中，就进行 id 丢弃
        """
        # tmp_label_file = '/workspace/dataset/special_site_jiaolian_add_site1_special_vehicle_count/tmp/2022_05_09_000204.txt'        
        # check_list = ["frame_000367.txt", 
        #             #   "004623.txt", "000763.txt", "000367.txt", "004450.txt", "004451.txt", "003662.jpg", "003663.jpg", "003664.jpg", "003665.jpg", 
        #               ]
        # if str.split(path, os.path.sep)[-1] in check_list:
        #     print("check file===>")  
        tmp_label_file = path
        if os.path.exists(path) == False:
            return False
        old_ret = read_file(tmp_label_file)
        new_ret = []
        # tmp_ret = [ item.split(' ') for item in tmp_ret ] 
        
        # change label 
        # for item in 
        
        for item in old_ret:
            # tmp_new_item = item.split(' ')
            
            tmp_old_item = item.split(' ')
            tmp_new_item = tmp_old_item
            tmp_discard_flag = False
            
            tmp_label_id = int(tmp_new_item[0])
            if tmp_label_id in [0, 8, 4,10,16,17] :
                print("old:", tmp_label_id ,self.old_labels[tmp_label_id])
                
            tmp_label =  self.old_labels[tmp_label_id]
            if tmp_label in self.new_labels:
                # 在新的类别中, id 转化
                tmp_new_item[0] = str(self.new_labels.index(tmp_label))
                tmp_discard_flag = False                
                pass
            else:
                 # 是否在 merge。在，则进行映射，不在则丢弃
                tmp_discard_flag = True
                for key, value in self.merge_labels.items():
                    if tmp_label in value:
                        # 更改为新的 id
                        # tmp_label_id = self.new_labels.index(key)
                        tmp_new_item[0] = str(self.new_labels.index(key))
                        tmp_discard_flag = False
                        
            if tmp_discard_flag == False:
                new_ret.append(tmp_new_item)
            else:
                if is_print:
                    print('discard: label:{}, path:{}, '.format(self.old_labels[int(tmp_old_item[0])] , tmp_label_file, ))
                    pass
        if new_ret != []:
            new_ret = [ str.join(' ', item) for item in new_ret]  
            # write_data(tmp_label_file + '.new.txt', str_list=new_ret, mode='w' )
            write_data(tmp_label_file, str_list=new_ret, mode='w' )
            return True
        else:
            return False
        
        
                
        pass

    def change_to_new_labels(self):
        save_dir = self.save_dir
        is_delete_file = False
        rm_list = []
   
        nums = len(self.label_files)
        for index, item in enumerate(self.label_files):
            # tmp_label_file = item
            # tmp_ret = read_file(tmp_label_file)
            # tmp_ret = [ item.split(' ') for item in tmp_ret ] 
            
            if index %1000:
                print("index:{}, all:{}, index/all: {}%".format(index,nums , str(100.0*index/nums)[:5],))
            is_delete_file = not self.change_file_to_new_label(item)
            if is_delete_file:
                rm_list.append([self.img_files[index], self.label_files[index], self.xml_files[index]])
            # pass
        
        # # 删除空的文件
        # if is_delete_file:
        #     for item in rm_list:
        #         rm_file(item)
        
        # # 复制
        # save_dir = "/workspace/dataset/VOCdevkitszcity1_specialcar_addspecial_site_vehicle_count/tmp"
        # for item in rm_list:
        #     for file in item:
        #         if os.path.exists(file):
        #             cp_file( file, save_dir)
        #         else:
        #             pass
        
        # 移动
        for item in rm_list:
            for file in item:
                if os.path.exists(file):
                    move_file( file, save_dir)
                else:
                    pass        
       
    
    pass

"""
self.label_files[0]
'/workspace/dataset/special_site_jiaolian_add_site1_special/VOC2007/labels/2022_05_09_000001.txt'
self.img_files[0]
'/workspace/dataset/special_site_jiaolian_add_site1_special/VOC2007/JPEGImages/2022_05_09_000001.jpg'
"""            
        
def main():
    run =  DataOpts()
    run.piplie()
    pass




if __name__ == '__main__':
    main()