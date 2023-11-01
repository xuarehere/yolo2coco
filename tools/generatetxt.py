'''
Author: xuarehere
Date: 2022-12-19 17:53:42
LastEditTime: 2023-01-10 14:17:22
LastEditors: xuarehere
Description: 
FilePath: /special_site_2d_220801/generatetxt.py

'''

import os
import random
import sys



root_path = "./VOC2007"
# root_path = "."

xmlfilepath = root_path + '/Annotations'

txtsavepath = root_path + '/ImageSets/Main'

save_info_path = './trainVal.py'
write_info = []

if not os.path.exists(root_path):
    print("cannot find such directory: " + root_path)
    exit()

if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

trainval_percent = 1
train_percent = 0.7
total_xml = os.listdir(xmlfilepath)
num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

print("train and val site:", tv)
print("train site:", tr)

ftrainval = open(txtsavepath + '/trainval.txt', 'w')
ftest = open(txtsavepath + '/test.txt', 'w')
ftrain = open(txtsavepath + '/train.txt', 'w')
fval = open(txtsavepath + '/val.txt', 'w')


def write_data(file_path, str_list, mode='a', encoding='utf-8'):
    with open(file_path, mode, encoding=encoding) as fp:
        for item in str_list:
            fp.writelines(item)
            fp.flush()
            
            
            
for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()

write_info.append(["#train and val site:", str(tv), "\n",
                   "#train site:", str(tr)
                   ])
write_data(save_info_path, write_info, mode='w')
