import os
import cv2 as cv
import skimage
#import imghdr
import selective_search

image="car_IMG_8112.JPG"
src_path=os.getcwd()
dst_path="C:/Users/Oğuz Kağan/Desktop/destination"
label_ds="C:/Users/Oğuz Kağan/Desktop/labels"

#Schreiben Sie den Klassenamen des Fotos an den Anfang des Dokumentnamens. Vergessen Sie das Unterstreichen nicht!

def selective(image, src_path: str , dst_path: str, label_dst: str):
  valid_image_extensions=['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'jpg', 'bmp', 'png', 'webp', 'exr']

  if os.path.isdir(src_path)==False or os.path.isdir(label_dst)==False or os.path.isdir(dst_path)==False:
     raise NotADirectoryError

#   if valid_image_extensions.count(imghdr.what(image))==0:
#      raise IOError

  os.chdir(src_path)
  img = skimage.io.imread(image)

  boxes = selective_search.selective_search(img, mode='single')

  # drawing rectangles on the original image
  img = cv.imread(image)
  for x1, y1, x2, y2 in boxes:
      img = cv.rectangle(img, (x1, y1), (x2, y2), color=(0,255,0), thickness=1)

  #Labels
  os.chdir(label_dst)
  liste=os.listdir(label_dst)
  if liste.count("classes.txt")==0:
     with open("classes.txt", "w") as f:
        pass
     
  list1=image.split("_")
  class_name=list1[0]

  with open("classes.txt", "a") as file:
     file.write(class_name + "\n")
     
  with open("classes.txt", "r") as f:
    list_oguz=f.readlines()

  length=len(list_oguz)-1
  for i in list_oguz:
    if i!=length:
        index=list_oguz.index(i)
        list_oguz[index]=list_oguz[index].replace("\n", "")

  class_idx=list_oguz.index(class_name)

  with open(image + ".txt", "w") as fp:
     fp.write("{}   {} {} {} {}".format(class_idx, x1, x2, y1, y2))

  #Printing the image
  os.chdir(dst_path)
  cv.imwrite(image + "(selective).png", img)

selective(image=image, src_path=src_path, dst_path=dst_path, label_dst=label_ds)

