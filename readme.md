<!--
 * @Author: xuarehere xuarehere@foxmail.com
 * @Date: 2023-10-30 16:17:32
 * @LastEditTime: 2023-11-01 17:52:50
 * @LastEditors: xujr xujianrong@sutpc.com
 * @Description: 
 * @FilePath: /github/readme.md
 * 
-->

- [数据转化](#数据转化)
- [实现](#实现)
  - [STEP 1 切分数据集](#step-1-切分数据集)
  - [STEP 2  生成 coco 格式](#step-2--生成-coco-格式)
  - [STEP 3 训练格式](#step-3-训练格式)
- [其他工具](#其他工具)



# 数据转化


YOLO 原始文件格式
```
input:
./data
├── images
    └───*.jpeg
├── labels
    └───*.txt
└───classes.txt
```

最终的生成格式

coco 的储存格式
```
/workspace/dataset/coco
├── annotations
├   ├── instances_train2017.json
├   └── instances_val2017.json
├── train2017
│   └───*.jpg
└── val2017
│   └───*.jpg
```


# 实现
## STEP 1 切分数据集
生成训练集、验证集、测试集

将 split_dataset.py 拷贝到 `./data`
在该工程下运行
```
python split_dataset.py
```

生成如下的文件结果
```
output:
./data
├── images
├── labels
├── test
│   ├── images
│      └───*.jpeg
│   └── labels
│   |  └───*.txt
│   └── label.txt
├── train
│   ├── images
│      └───*.jpeg
│   └── labels
│   |   └───*.txt
│   └── label.txt
└── val
    ├── images
    |   └───*.jpeg    
    └── labels
    |  └───*.txt 
    └── label.txt         
```





## STEP 2  生成 coco 格式

将 `yolo2coco.py` 分别拷贝到test、train、val 目录下，然后进行

```
python yolo2coco.py
```

如在 test 目录下
之后，生成
```
./data/test
├── annotations
│   └── train.json
├── images [3445 entries exceeds filelimit, not opening dir,*.jpeg]
├── labels [3445 entries exceeds filelimit, not opening dir，*.txt]
├── classes.txt
└── yolo2coco.py
```


手工对文件进行重命名，保留为 coco 的文件名。

```
./data/test
├── annotations
│   └── instances_test2017.json
├── test2017 [3445 entries exceeds filelimit, not opening dir,*.jpeg]
├── labels [3445 entries exceeds filelimit, not opening dir，*.txt]
├── classes.txt
└── yolo2coco.py
```

然后将 `annotations`、`test2017` 拷贝回去 `./data/` 目录。

其他的./data/train、./data/val 操作一样。

最后在./data 目录下的结构如下
```
./data
├── annotations
│   ├── instances_test2017.json
│   ├── instances_train2017.json
│   └── instances_val2017.json
├── images
├── labels
├── test
│   ├── labels [3445 entries exceeds filelimit, not opening dir]
│   └── classes.txt
├── test2017 [3445 entries exceeds filelimit, not opening dir]
├── train
│   ├── labels [10335 entries exceeds filelimit, not opening dir]
│   ├── classes.txt
│   └── yolo2coco.py
├── train2017 [10335 entries exceeds filelimit, not opening dir]
├── val
│   ├── labels [3445 entries exceeds filelimit, not opening dir]
│   ├── classes.txt
│   └── yolo2coco.py
├── val2017 [3445 entries exceeds filelimit, not opening dir]
├── classes.txt
├── readme.md
├── split_dataset.py
└── yolo2coco.py

12 directories, 12 files

12 directories, 12 files
```

## STEP 3 训练格式
可以吧一些中间文件简化，整理之后的结构如下：
```


./data
├── annotations
│   ├── instances_test2017.json
│   ├── instances_train2017.json
│   └── instances_val2017.json
├── test2017 [3445 entries exceeds filelimit, not opening dir,*.jpeg]
├── tmp
│   ├── test
│   │   ├── annotations
│   │   ├── labels [3445 entries exceeds filelimit, not opening dir，*.txt]
│   │   ├── classes.txt
│   │   └── yolo2coco.py
│   ├── train
│   │   ├── annotations
│   │   ├── labels [10335 entries exceeds filelimit, not opening dir，*.txt]
│   │   ├── classes.txt
│   │   └── yolo2coco.py
│   ├── val
│   │   ├── annotations
│   │   ├── labels [3445 entries exceeds filelimit, not opening dir，*.txt]
│   │   └── classes.txt
│   └── classes.txt
├── train2017 [10335 entries exceeds filelimit, not opening dir,*.jpeg]
├── val2017 [3445 entries exceeds filelimit, not opening dir,*.jpeg]
├── split_dataset.py
└── yolo2coco.py

14 directories, 11 files
```

其中，中间内容删除的话，可以简化为(具体对照coco 的训练格式):
```
./data
├── annotations
│   ├── instances_test2017.json
│   ├── instances_train2017.json
│   └── instances_val2017.json
├── test2017 [3445 entries exceeds filelimit, not opening dir,*.jpeg]
│── classes.txt
├── train2017 [10335 entries exceeds filelimit, not opening dir,*.jpeg]
├── val2017 [3445 entries exceeds filelimit, not opening dir,*.jpeg]
├── split_dataset.py
└── yolo2coco.py

```

# 其他工具
见 tools 文件夹