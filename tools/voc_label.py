'''
Descripttion: 
Author: xuarehere
Date: 2021-03-13 23:17:48
LastEditors: xuarehere
LastEditTime: 2023-01-09 14:56:28
FilePath: /special_site_2d_220801/voc_label.py
'''


import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
classes = ['Ambulance',
 'BigTruck',
 'Bus',
 'Car',
 'CoachesCar',
 'Cycle',
 'DangerousCar',
 'DangerousTruck',
 'FireTruck',
 'GarbageTruck',
 'MuckTruck',
 'Pedestrian',
 'PoliceCar',
 'Tanker',
 'TourBus',
 'Truck']
clscountdict = {}

# root_path = '/workspace/dataset/special_site_2d_220801/'  
root_path = os.getcwd()
def convert(site, box):
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

def write_data(file_path, str_list, mode='a', encoding='utf-8'):
    with open(file_path, mode, encoding=encoding) as fp:
        for item in str_list:
            fp.writelines(item)
            fp.flush()
            

def convert_annotation(year, image_id):
    in_file_root = os.path.join(root_path,'VOC%s/Annotations/%s.xml'%(year, image_id))
    out_file_root = os.path.join(root_path,'VOC%s/labels/%s.txt'%(year, image_id))
    in_file = open(in_file_root)
    out_file = open(out_file_root, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    site = root.find('site')
    w = int(site.find('width').text)
    h = int(site.find('height').text)

    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult)==1:
        #     continue
        if cls not in classes:
            continue
        if cls not in clscountdict.keys():
            clscountdict[cls] = 1
        else:
            clscountdict[cls] = clscountdict[cls] + 1
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for year, image_set in sets:
    if not os.path.exists(os.path.join(root_path,'VOC%s/labels/'%(year))):
        os.makedirs(os.path.join(root_path,'VOC%s/labels/'%(year)))
    image_ids_root = os.path.join(root_path,'VOC%s/ImageSets/Main/%s.txt'%(year, image_set))    
    image_ids = open(image_ids_root).read().strip().split()
    list_file_root = os.path.join(root_path,'%s_%s.txt'%(year, image_set))
    list_file = open(list_file_root, 'w')
    for image_id in image_ids:
        write_str = os.path.join(root_path,'VOC%s/JPEGImages/%s.jpg\n'%(year, image_id))
        list_file.write(write_str)
        convert_annotation(year, image_id)
    list_file.close()

os.system("cat 2007_train.txt 2007_val.txt> train.txt")
os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt> train.all.txt")
print(clscountdict)

write_info = ["#the numbers of class\n", 'clscountdict={}'.format(str(clscountdict))]


## sort information
print("sort information")     
print(sorted(clscountdict.items(), key = lambda kv:(kv[0], kv[1])))     
write_info.extend(["\n\n#sort information of class\n", 'clscountdict_sort_class={}'.format(str(sorted(clscountdict.items(), key = lambda kv:(kv[0], kv[1]))))])
write_info.extend(["\n\n#sort information of class\n", 'clscountdict_sort_nums={}'.format(str(sorted(clscountdict.items(), key = lambda kv:(kv[1], kv[0]))))])


write_data("./clscountdict.py", write_info, mode='w')
