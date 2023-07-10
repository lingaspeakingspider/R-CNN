import os
import cv2 as cv
import skimage
import imghdr
import selective_search

image="car_IMG_8112.jpg"
src_path=os.getcwd()
dst_path="C:/Users/Oğuz Kağan/Desktop/destination"
label_dst="C:/Users/Oğuz Kağan/Desktop/labels"

#Schreiben Sie den Klassenamen des Fotos an den Anfang des Dokumentnamens. Vergessen Sie das Unterstreichen nicht!

class Selective_Search:
   def __init__(self, image, src_path: str , dst_path: str, label_dst):
      self.image=image
      self.src_path=src_path
      self.dst_path=dst_path
      self.label_dst=label_dst

   def labeling(self, file, class_idx, x1, x2, y1, y2):
      os.chdir(label_dst)
      with open(file, "a") as fp:
         fp.write("{}   {} {} {} {}\n".format(class_idx, x1, x2, y1, y2))

   def selective(self):
      valid_image_extensions=['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'jpg', 'bmp', 'png', 'webp', 'exr']
      class_names=[]
      
      os.chdir(self.src_path)
      extension=imghdr.what(self.image)
      
      if valid_image_extensions.count(extension)==0:
         raise IOError

      if os.path.isdir(self.src_path)==False or os.path.isdir(self.label_dst)==False or os.path.isdir(self.dst_path)==False:
         raise NotADirectoryError
      

      #Selective Search
      os.chdir(self.src_path)
      img = skimage.io.imread(image)
      boxes = selective_search.selective_search(img, mode='single')

      #Labels
      os.chdir(self.label_dst)
      liste=os.listdir(self.label_dst)
      if liste.count("classes.txt")==0:
         with open("classes.txt", "w") as f:
            pass
         
      list1=image.split("_")
      class_name=list1[0]
      class_names.append(class_name)
      
      if class_names.count(class_names)==0:
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

      #Drawing bounding boxes
      os.chdir(self.src_path)
      img = cv.imread(image)
      with open(self.image + ".txt", "w") as f:
            pass
      for x1, y1, x2, y2 in boxes:
         Selective_Search.labeling(self, file=self.image + ".txt", class_idx=class_idx, x1=x1, x2=x2, y1=y1,y2=y2)
         img = cv.rectangle(img, (x1, y1), (x2, y2), color=(0,255,0), thickness=1)

      #Sending the image to destination path
      os.chdir(self.dst_path)
      cv.imwrite(image + "(selective).png", img)

      #Controlling
      src_list=os.listdir(self.src_path)
      if src_list.count(image + ".txt")!=0:
         os.remove(os.path.join(self.src_path, image + ".txt"))


model=Selective_Search(image=image, src_path=src_path, dst_path=dst_path, label_dst=label_dst)
model.selective()
