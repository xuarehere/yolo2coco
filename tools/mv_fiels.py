'''
Author: xuarehere
Date: 2022-12-30 09:47:46
LastEditTime: 2023-10-25 12:52:45
LastEditors: xuarehere xuarehere@sutpc.com
Description: 
FilePath: /suiDaoShiJian/tools/mv_fiels.py

'''
import os 
import shutil

def check_mkdirs(dir_path):
    if not os.path.exists(path=dir_path):
        os.makedirs(dir_path)
        
def move_files():
    """_summary_
    把xml 对应 的图片、txt 文件，移动到新的文件目录
    """
    path = "/workspace/dataset/sutpc_object_detections_datasets/train/VOCdevkitszcity1_specialcar_sub1/rmBK/VOC2007/Annotations"

    files = sorted( os.listdir(path))

    old_path = "/workspace/dataset/sutpc_object_detections_datasets/train/VOCdevkitszcity1_specialcar_sub1/VOC2007"
    new_path = "/workspace/dataset/sutpc_object_detections_datasets/train/VOCdevkitszcity1_specialcar_sub1/rmBK/VOC2007"
    
    for file in files:
        file_id = file[:-4]
        
        old_JPEGImages_path = os.path.join( os.path.join(old_path, "JPEGImages"),  file_id + ".jpg")
        new_JPEGImages_path = os.path.join(new_path, "JPEGImages")
        check_mkdirs(new_JPEGImages_path)
        if os.path.exists(old_JPEGImages_path):
            shutil.move( old_JPEGImages_path, new_JPEGImages_path )
        
        old_labels_path = os.path.join( os.path.join(old_path, "labels"),  file_id + ".txt")
        new_labels_path = os.path.join(new_path, "labels")
        check_mkdirs(new_labels_path)
        if os.path.exists(old_labels_path):
            shutil.move( old_labels_path, new_labels_path )
    print("nums:", len(files))
    pass

def judge_blank_file(file_path= "/workspace/dataset/suiDaoShiJian/1.txt"):
    with open(file_path, 'r') as file:
        # Read the entire file content
        file_content = file.read().strip() 
    # if file_content == '':
    #     return True 
    return True if file_content == '' else False
    
    
    
def move_blank_files():
    """_summary_
    delete the blank labels files and its corresponding files
    """
    path = "/workspace/dataset/suiDaoShiJian/VOC2007/labels"

    files = sorted( os.listdir(path))

    # old_path = "./VOC2007"
    new_path = "./rmBK/VOC2007"
    new_JPEGImage_dir =   os.path.join(new_path, "JPEGImages")
    new_label_dir = os.path.join(new_path, "labels")  
    check_mkdirs(new_JPEGImage_dir)  
    check_mkdirs(new_label_dir)  
    count = 0
    
    for idx, file in enumerate( files):
        file_id = file.split('.')[0]
        old_JPEGImage_path =   os.path.join( os.path.join( os.path.dirname(path), "JPEGImages"),  file_id + ".jpeg")
        old_label_path = os.path.join(path, file )
        
        new_JPEGImage_dir =   os.path.join(new_path, "JPEGImages")
        new_label_dir = os.path.join(new_path, "labels")
        if judge_blank_file(os.path.join(path, file )):
            # print("---------->", file)
            count +=1
            
        
            if os.path.exists(old_JPEGImage_path):
                shutil.move( old_JPEGImage_path, new_JPEGImage_dir )            
                
            if os.path.exists(old_label_path):
                shutil.move( old_label_path, new_label_dir )                   
                
        
        # old_JPEGImages_path = os.path.join( os.path.join( os.path.dirname(path), "JPEGImages"),  file_id + ".jpg")
        # new_JPEGImages_path = os.path.join(new_path, "JPEGImages")
        # check_mkdirs(new_JPEGImages_path)
        # if os.path.exists(old_JPEGImages_path):
        #     shutil.move( old_JPEGImages_path, new_JPEGImages_path )
        
        # old_labels_path = os.path.join( os.path.join(old_path, "labels"),  file_id + ".txt")
        # new_labels_path = os.path.join(new_path, "labels")
        # check_mkdirs(new_labels_path)
        # if os.path.exists(old_labels_path):
        #     shutil.move( old_labels_path, new_labels_path )
    # print("nums:", len(files))
    
    print(count)
        # print(id )
    pass

def main():
    # move_files()
    move_blank_files()
    
    pass

if __name__ == "__main__":
    main()
    pass
