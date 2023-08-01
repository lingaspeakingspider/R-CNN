import numpy as np
import cv2 as cv
import os
from pathlib import Path
import logging

class_names=[]


class Selective_Search:
    def __init__(self, image: str, src_path: Path, dst_path: Path, label_dst: Path, log_file: Path):
        self.image=image
        self.src_path=src_path
        self.log_file=log_file
        self.dst_path=dst_path
        self.label_dst=label_dst

    def logger(self, log_message: str, propagation: bool = True):
        logger = logging.getLogger("biocally")
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(level=logging.DEBUG)
        logger.addHandler(file_handler)

        logging.info(log_message)

        if propagation==False:
            logger.propagate=False

    def labeling(self, file, class_idx, x, y ,w, h):
      os.chdir(self.label_dst)
      with open(file, "a") as fp:
         fp.write("{}   {} {} {} {}\n".format(class_idx, x, y, w, h))


    def selective(self, method: str = "fast"):

        os.chdir(self.src_path)
        img=cv.imread(self.image)
        ss = cv.ximgproc.segmentation.createSelectiveSearchSegmentation()
        ss.setBaseImage(img)

        image=self.image
        
        if method=="fast":
            ss.switchToSelectiveSearchFast()
            self.logger(log_message=" The method was selected as fast.")

        elif method=="quality":
            ss.switchToSelectiveSearchQuality()
            self.logger(log_message=" The method was selected as quality.")


        rects = ss.process()
        self.logger(log_message=" Selective search has processed.")

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
        os.chdir(self.label_dst)
        name=image.replace(".jpg", "")
        name=name+".txt"
        with open(name + ".txt", "w") as file_oguz:
                pass
        
        for i, rect in enumerate(rects):
            if (i < len(rects)):
                x, y, w, h = rect
                self.labeling(file=name, class_idx=class_idx, x=x, y=y, w=w, h=h)
                color = (0,255,0)
                cv.rectangle(img, (x, y), (x+w, y+h), color, cv.LINE_AA)

            else:
                break

        self.logger(log_message=" The rectangles have drawen and labels have created.")

        #Sending the image to destination path
        os.chdir(self.dst_path)
        cv.imwrite(name + "_(selective).jpg", img)
        self.logger(log_message=" The image has sent to the destination path.")

        #Controlling
        label_list=os.listdir(self.label_dst)
        dst_list=os.listdir(self.dst_path)

        for i in label_list:
          liste=i.split(".")
          if liste.count("txt")==2:
            os.remove(os.remove(os.path.join(self.label_dst, i)))

        self.logger(log_message=" Selective search process has finished succesfully.", propagation=False)


        if dst_list.count(self.log_file)!=0 and label_list.count(self.log_file)!=0:
            os.chdir(self.dst_path)
            os.remove(os.path.join(self.dst_path, self.log_file))

            os.chdir(self.label_dst)
            os.remove(os.path.join(self.label_dst, self.log_file))




model = Selective_Search(image="/content/car_IMG_8112.jpg", src_path=os.getcwd(), dst_path="/content/destination", label_dst="/content/labels", log_file="/content/logbey.log")
model.selective()
