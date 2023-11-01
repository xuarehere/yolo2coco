import os
import shutil
import datetime
"""
./special_site_jiaolian
    |-- Annotations
    |   `-- special
    |       `-- special
    |           `-- *.xml
    |-- ImageSets
    |   `-- Main
    |       `-- default.txt
    |-- JPEGImages
    |    `-- special
    |        `-- special
    |           `-- *.jpg     
    `-- labelmap.txt    
"""

NOW_TIME = datetime.datetime.now()
# TIME_STR = NOW_TIME.strftime("%Y_%m_%d %H:%M:%S")
TIME_DATA_STR = NOW_TIME.strftime("%Y_%m_%d")
def rename_dir():
    """
    文件夹名称重命名： 将 : 代替为 _

    案例：
    ./dataset_task_special-2021_09_27_13_45_46
        |-- Annotations
        |   `-- special_site_all
        |       |-- 172.31.1.112:20101      ==> 172.31.1.112_20101
        |       ......
        |           |-- *.xml
        |-- ImageSets
        |   `-- Main
        |       |-- default.txt
        |-- JPEGImages
        |   `-- special_site_all
        |       |-- 172.31.1.112:20101
        |       |   ......
        |               |-- *.JPG
        `-- labelmap.txt

    """
    # path = "./rename_Annotations/special_site_2d_06/"
    path = "./Annotations/special_site_2d_06/"       # JPEGImages
    # path = "./JPEGImages/special_site_2d_06/"       # JPEGImages
    # 获取该目录下所有文件，存入列表中
    f_dir = os.listdir(path)
    # f_dir[0].split("%")
    # ['172.31.1.112', '3A20101']

    print(len(f_dir))

    print(f_dir[0])


    # rename dir
    for i_dir in f_dir:
        i_dir_new = i_dir.replace(i_dir[-6], "_")       # : 代替为 _
        # 用os模块中的rename方法对文件改名
        old_name = os.path.join(path, i_dir)
        new_name = os.path.join(path, i_dir_new)
        os.rename(old_name, new_name)

        # path_dir = os.path.join(path, i_dir )
        # f_dir_files = os.listdir(path_dir)
        # for i_file in f_dir_files:
        #      newname = 
        #      os.rename(path+oldname, path+newname)


def rename_files(path=""):
    if path =="":
        raise Exception("Error!path="" ")
    # path = "./rename_Annotations/special_site_2d_06/"
    # path = "./Annotations/special_site_2d_06/"       # Annotations
    # path = "./JPEGImages/special_site_2d_06/"       # JPEGImages
    # 获取该目录下所有文件，存入列表中
    f_dir = os.listdir(path)
    # f_dir[0].split("%")
    # ['172.31.1.112', '3A20101']

    print(len(f_dir))

    print(f_dir[0])


    # rename dir
    i = 0 
    for i_dir in f_dir:
        if os.path.isdir(i_dir):
            files_path = os.path.join(path, i_dir)
            f_dir_files = os.listdir(files_path)
            for i_file in f_dir_files:
                if i_dir in i_file:
                    continue
                old_name = os.path.join(files_path, i_file)
                new_name = os.path.join(files_path, i_dir + "_" + i_file)
                os.rename(old_name, new_name) 
                i +=1

        else:
            old_name = os.path.join(path, i_dir)
            new_name = os.path.join(path, TIME_DATA_STR + "_" + i_dir)
            os.rename(old_name, new_name) 
            i +=1
        if i %10 == 0:
            print("deal file i:{}".format(i))
    print("deal file i:{}".format(i))



        # i_dir_new = i_dir.replace(i_dir[-6], "_")       # : 代替为 _
        # # 用os模块中的rename方法对文件改名
        # old_name = os.path.join(path, i_dir)
        # new_name = os.path.join(path, i_dir_new)
        # os.rename(old_name, new_name)

        # path_dir = os.path.join(path, i_dir )
        # f_dir_files = os.listdir(path_dir)
        # for i_file in f_dir_files:
        #      newname = 
        #      os.rename(path+oldname, path+newname)

def del_blank_dir(dir):
    try:
        os.rmdir(dir)  #os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
        print("delete：", dir)
    except Exception as e:
        print('Exception',e)
    return True

def del_blank_dirs(dir):
    """逐级删除空白文件夹

    Args:
        dir (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        while len(os.listdir(dir)) == 0:
            del_blank_dir(dir)
            # pardir
            dir = os.path.abspath(os.path.join(os.path.dirname(dir),os.path.pardir))        

    except Exception as e:
        print('Exception',e)
    return True    

# ————————————————
# 版权声明：本文为CSDN博主「小呆丶」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/qq_41192383/article/details/86549906

def move_files(path ="", dst=""):
    if path =="" or dst=="":
        raise Exception("Error!path="" ")    
    # path = "./rename_Annotations/special_site_2d_06/"
    # dst  = "./rename_Annotations"
    # # path = "./Annotations/special_site_2d_06/"       # Annotations
    # # dst  = "./Annotations"
    # path = "./JPEGImages/special_site_2d_06/"       # JPEGImages
    # dst  = "./JPEGImages"

    # 获取该目录下所有文件，存入列表中
    f_dir = os.listdir(path)
    # f_dir[0].split("%")
    # ['172.31.1.112', '3A20101']

    print(len(f_dir))

    print(f_dir[0])


    # move files
    i = 0 
    for i_dir in f_dir:
        files_path = os.path.join(path, i_dir)
        if os.path.isdir(files_path):
            f_dir_files = os.listdir(files_path)
            for i_file in f_dir_files:
                src = os.path.join(files_path, i_file)
                # dst = path
                shutil.move(src, dst)
                i +=1
                if i %10 == 0:
                    print("deal file i:{}".format(i))
            # del blank dir 
            if len(os.listdir(files_path)) == 0:
                del_blank_dir(files_path)                    
        else:
            src = os.path.join(path, i_dir)
            # dst = path
            shutil.move(src, dst)
            i +=1
            if i %10 == 0:
                print("deal file i:{}".format(i))
    print("deal file i:{}".format(i))

    # del blank dir 
    # if len(os.listdir(path)) == 0:
    #     del_blank_dir(path)
    if len(os.listdir(path)) == 0:
        del_blank_dirs(path)
    # while len(os.listdir(path)) == 0:
    #     del_blank_dir(path)
    #     # pardir
    #     path = os.path.abspath(os.path.join(os.path.dirname(path),os.path.pardir))



def main():
    ## step1: rename dir
    # rename_dir()

    ## step2: rename files
    path_Annotations = "./Annotations/special_site_2d_06/"       # Annotations
    path_JPEGImages = "./JPEGImages/special_site_2d_06/"       # JPEGImages
    rename_files(path_Annotations)
    rename_files(path_JPEGImages)
    os.path.exists(path_Annotations)


    ## step3: mv files  and del blank dir
    # src = ""
    # dst = ""
    # shutil.move(src, dst)
    path_Annotations = "./Annotations/special_site_2d_06/"       # Annotations
    dst_Annotations  = "./Annotations"  
    move_files(path_Annotations, dst_Annotations)
    path_JPEGImages = "./JPEGImages/special_site_2d_06/"       # JPEGImages
    dst_path_JPEGImages  = "./JPEGImages"    
    move_files(path_JPEGImages, dst_path_JPEGImages)
    
    # 

if __name__ == '__main__':
    main()








# n = 0
# i = 0
# for i in f_dir:
#     # 设置旧文件名（就是路径+文件名）
#     oldname = f_dir[n]

#     # 设置新文件名
#     newname = str(n+1) + '.jpg'
#     # 用os模块中的rename方法对文件改名
#     os.rename(path+oldname, path+newname)
#     print(oldname, '======>', newname)

#     n += 1
