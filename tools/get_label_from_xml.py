'''
Author: xuarehere
Date: 2023-01-09 15:30:00
LastEditTime: 2023-10-25 10:32:45
LastEditors: xuarehere xuarehere@sutpc.com
Description: 
FilePath: /suiDaoShiJian/tools/get_label_from_xml.py

'''
"""_summary_
获取数据集中的所有 label
Returns:
    _type_: _description_
"""
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import collections
import json


labels = set()
labels_dict = collections.OrderedDict()
labels_map = collections.OrderedDict()     # id: label

def get_label(path):
    ret_label = set()
    in_file_root = path
    # out_file_root = os.path.join(root_path,'VOC%s/labels/%s.txt'%(year, image_id))
    in_file = open(in_file_root)
    # out_file = open(out_file_root, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    site = root.find('site')
    w = int(site.find('width').text)
    h = int(site.find('height').text)

    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        ret_label.add(cls)
    return ret_label
     
def write_data(file_path, str_list, mode='a', encoding='utf-8'):
    with open(file_path, mode, encoding=encoding) as fp:
        for item in str_list:
            fp.writelines(item)
            fp.flush()
            
def get_label_from_xml():
    """_summary_
    从xml标签中，统计样本数据量
    """
    write_info = []
    # get all dirs 
    dir_path = "./VOC2007/labels"
    save_label_path = './xml_labels.py'
    xml_dirs = os.listdir(dir_path)
    # get label
    for index, item in enumerate(xml_dirs):
        file = os.path.join(dir_path,item)
        if index % 1000 == 0:
            print("index:{}, path:{}".format(index, file))
        labels.update(get_label( file))
    
    # write 
    write_info.append('#"label informations"\n')
    write_info.extend(["labels = " + str(sorted(list(labels))) + "\n", "nums = " + str(len(list(labels)))])
    
    write_info.append('\n#"xml file nums"\n')
    write_info.append("xml_file_nums = " + str(len(xml_dirs)) + "\n")
    write_data(save_label_path, write_info, mode='w')
    
    pass
        



def get_label_txt(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_
        10 0.11439732142857142 0.1805921052631579 0.010044642857142856 0.030921052631578946
    """
    
    with open(file_path, 'r') as file:
        # Read the entire file content
        for line in file:
            # print(line, end='')      
            line = line.strip()
            line = line.split(' ')
            # if int(line[0]) not in labels_dict:
            #     labels_dict[int(line[0])] = 1
            # else:
            #     labels_dict[int(line[0])] += 1
            if labels_map[int(line[0])] not in labels_dict:
                labels_dict[labels_map[int(line[0])]] = 1
            else:
                labels_dict[labels_map[int(line[0])]] += 1            
    
def get_label_map(file_path):
    """_summary_
    read the label, id2label
    Args:
        file_path (_type_): _description_
        
    """
    with open(file_path, 'r') as file:
        for id, line in enumerate( file):
            line = line.strip()
            labels_map[id]=line
            
    pass
        
        
        
def get_label_from_txt():
    """_summary_
    从xml标签中，统计样本数据量
    """
    write_info = []
    # get all dirs 
    dir_path = "/workspace/dataset/suiDaoShiJian/VOC2007/labels"
    save_label_path = './labels_info.py'
    txt_dirs = os.listdir(dir_path)
    # get label
    for index, item in enumerate(txt_dirs):
        file = os.path.join(dir_path,item)
        if index % 1000 == 0:
            print("index:{}, path:{}".format(index, file))
        # labels.update(get_label_txt( file))
        get_label_txt( file)
    print(labels_dict)
    print(labels_map)
    
    # write 
    write_info.append('#"label informations"\n')
    write_info.extend(["labels = " + str(sorted(list(labels))) + "\n", "labels_nums = " + str(len(list(labels)))])

    write_info.extend('\n')
    write_info.extend('labels_dict = ' + str(labels_dict))
    write_info.extend('\n')
    write_info.extend('labels_map = ' + str(labels_map))
    
    
    write_info.append('\n#"file nums"\n')
    write_info.append("file_nums = " + str(len(txt_dirs)) + "\n")
    write_data(save_label_path, write_info, mode='w')
    
    pass
                
def main():
    # run =  DataOpts()
    # run.piplie()
    # get_label_from_xml()
    get_label_map('/workspace/dataset/suiDaoShiJian/VOC2007/label.txt')
    get_label_from_txt()
    pass




if __name__ == '__main__':
    main()
    
"""
{3: 10701, 9: 3192, 1: 11663, 2: 2681, 8: 533, 13: 1659, 10: 5118, 11: 874, 0: 114, 6: 253, 4: 999, 7: 528, 12: 68, 5: 237}
{'BigTruck': 10701, 'Person': 3192, 'Car': 11663, 'Truck': 2681, 'VanTruck': 533, 'Head': 1659, 'Coness': 5118, 'MotorCycle': 874, 'Bus': 114, 'Other': 253, 'DangerousTruck': 999, 'MiniBus': 528, 'Tire': 68, 'Box': 237}

OrderedDict([('BigTruck', 10701), ('Person', 3192), ('Car', 11663), ('Truck', 2681), ('VanTruck', 533), ('Head', 1659), ('Coness', 5118), ('MotorCycle', 874), ('Bus', 114), ('Other', 253), ('DangerousTruck', 999), ('MiniBus', 528), ('Tire', 68), ('Box', 237)])

OrderedDict([(0, 'Bus'), (1, 'Car'), (2, 'Truck'), (3, 'BigTruck'), (4, 'DangerousTruck'), (5, 'Box'), (6, 'Other'), (7, 'MiniBus'), (8, 'VanTruck'), (9, 'Person'), (10, 'Coness'), (11, 'MotorCycle'), (12, 'Tire'), (13, 'Head')])

"""    