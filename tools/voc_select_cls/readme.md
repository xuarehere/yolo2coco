<!--
 * @Author: xuarehere
 * @Date: 2023-01-05 14:17:17
 * @LastEditTime: 2023-01-05 14:55:45
 * @LastEditors: xuarehere
 * @Description: 
 * @FilePath: /sutpc_object_detections_datasets_10cls/tools/voc/voc.md
 * 
-->

从 voc 数据集中筛选出制定数据


1. 下载原始数据并解压
```
$ mkdir voc_2007_2012
$ cp merge_labels.py  voc_label.py  voc_2007_2012/
$ cd voc_2007_2012
$ tar xf       VOCtest_06-Nov-2007.tar 
$ tar xf       VOCtrainval_06-Nov-2007.tar  
$ tar xf       VOCtrainval_11-May-2012.tar
```

文件结构
```
.
└── VOCdevkit
    ├── VOC2007
    │   ├── Annotations
    │   ├── ImageSets
    │   │   ├── Layout
    │   │   ├── Main
    │   │   └── Segmentation
    │   ├── JPEGImages
    │   ├── SegmentationClass
    │   └── SegmentationObject
    └── VOC2012
        ├── Annotations
        ├── ImageSets
        │   ├── Action
        │   ├── Layout
        │   ├── Main
        │   └── Segmentation
        ├── JPEGImages
        ├── SegmentationClass
        └── SegmentationObject
```

2. 生成训练的格式
```

python voc_label.py
```


3. 生成需要保留的类别
需要保留的类别，放进去 self.merge_labels 中
```
python merge_labels.py 
```

从 voc 中筛选出类别，并生成训练时候的的数据信息。

self.new_labels     是训练时候的类别

self.merge_labels   融合的类别，将需要**保留类别、融合的类别**放在这里，下面的案例中，显示了在voc 中保存 person 类别



相关的参数修改见下面


类  DataOpts 中进行相关参数的修改，见 self.init_param() 函数

```
        # 原始参数信息
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
            "Bus": [],
            "Car": [],
            "Cycle": [], 
            "Pedestrian": ["person"], 
            "Truck": [],
            "BigTruck": [],
            "Tanker": [],
            "GarbageTruck":[],
            "MuckTruck": [],
            "CoachesCar": [],
        }   

```


