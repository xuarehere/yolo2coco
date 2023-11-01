'''
Author: xuarehere xuarehere@sutpc.com
Date: 2023-10-27 17:58:15
LastEditTime: 2023-11-01 15:46:00
LastEditors: xuarehere xuarehere@sutpc.com
Description: 
FilePath: /suiDaoShiJian/VOC2007/split_dataset.py

input:
├── images
├── labels


output:
├── images
├── labels
├── test
│   ├── images
│      └───*.jpeg
│   └── labels
│      └───*.txt
├── train
│   ├── images
│      └───*.jpeg
│   └── labels
│      └───*.txt
└── val
    ├── images
       └───*.jpeg    
    └── labels
       └───*.txt   
'''


import os 
import random

random.seed(1)
root_dir ={
    "root": "/workspace/dataset/suiDaoShiJian/VOC2007"
}
root_dir["images"] = os.path.join(root_dir["root"], "images")
root_dir["labels"] = os.path.join(root_dir["root"], "labels")

root_dir['root'] = "/workspace/dataset/suiDaoShiJian/VOC2007"


images_dir = os.listdir(root_dir["images"])
labels_dir = os.listdir(root_dir["labels"])

nums = len(images_dir)

if nums != len(labels_dir):
    raise Exception("Error")

split_ratio={
    'train':0.6,
    'val':0.2,
    'test':0.2,
}
# 17225×0.6 = 10335
# 17225×0.2  = 3445

def check_mkdirs(dir_path):
    """_summary_
    检测文件夹地址是否存在，不存在则创建。支持多级创建
    
    Args:
        dir_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    if not os.path.exists(path=dir_path):
        os.makedirs(dir_path)
    return dir_path
        
random.shuffle(images_dir)

train_path={
    "root":check_mkdirs(os.path.join(root_dir['root'], "train")),
}
train_path["images"] = check_mkdirs(os.path.join(train_path["root"], "images"))
train_path["labels"] = check_mkdirs(os.path.join(train_path["root"], "labels"))

val_path={
    "root":check_mkdirs(os.path.join(root_dir['root'], "val")),
}
val_path["images"] = check_mkdirs(os.path.join(val_path["root"], "images"))
val_path["labels"] = check_mkdirs(os.path.join(val_path["root"], "labels"))

test_path ={
    "root":check_mkdirs(os.path.join(root_dir['root'], "test")),
}
test_path["images"] = check_mkdirs(os.path.join(test_path["root"], "images"))
test_path["labels"] = check_mkdirs(os.path.join(test_path["root"], "labels"))


train_nums = nums*split_ratio["train"]
val_nums = nums*split_ratio["val"]
test_nums = nums - train_nums - val_nums
import shutil
for idx, file in enumerate(images_dir):
    file_name = file.split('.')[0]
    image_path = os.path.join(root_dir["images"], file)
    label_path = os.path.join(root_dir["labels"], file_name + '.txt')    
    # mv to train 
    if idx < train_nums:
        # mv 
        shutil.move(image_path, train_path["images"])
        shutil.move(label_path, train_path["labels"])
        
    elif idx < (train_nums+val_nums):
        # mv 
        shutil.move(image_path, val_path["images"])
        shutil.move(label_path, val_path["labels"])        
    else:
        # mv 
        shutil.move(image_path, test_path["images"])
        shutil.move(label_path, test_path["labels"])    
    # if idx%1000==0:
    #     print("-->", idx*1.0/nums)      
    # mv to val 
print("train_nums={}, val_nums={}, test_nums={}".format(train_nums,val_nums,test_nums))

