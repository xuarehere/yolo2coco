'''
Author: xuarehere xuarehere@sutpc.com
Date: 2023-10-25 11:02:55
LastEditTime: 2023-11-01 17:24:21
LastEditors: xuarehere xuarehere@sutpc.com
Description: 
FilePath: /suiDaoShiJian/tools/write_a_image.py

yolo 格式中，写一个标签格式进行图片可视化显示

'''
import cv2
import numpy as np

# Load your image
image = cv2.imread('/workspace/dataset/suiDaoShiJian/check/000012.jpg')

# Define label information
label = "6 0.507 0.551051051051051 0.39 0.5195195195195195"

# Split the label into individual parts
parts = label.split()

# Extract the coordinates and other label information
class_id = int(parts[0])
x, y, w, h = map(float, parts[1:5]) # x-center, y-center, width, height
# Convert the coordinates to pixel values (assuming normalized coordinates)
image_height, image_width, _ = image.shape
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


# Draw a rectangle and label on the image
cv2.rectangle(image, (x1,y1), (x2,y2), (0, 255, 0), 2)
cv2.putText(image, str(class_id), (x1,y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Save the annotated image
cv2.imwrite('annotated_image.jpg', image)
