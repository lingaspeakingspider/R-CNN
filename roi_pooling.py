from keras.utils import img_to_array
import numpy as np
import tensorflow as tf
from pathlib import Path
from typing import Dict
from PIL import Image

#List of each region part
first = second = third = fourth = list()
first_matrix = second_matrix = third_matrix, fourth_matrix = list()
dictionary=Dict[str, list]
first_str = second_str = third_str = fourth_str = list()
arrays=[]

class RoIPooling2D:
    global first, second, third, fourth  

    def __init__(self, image: Path, bounding_box:np.array):
        self.image=image
        self.bounding_box=bounding_box

        #Array of Image
        image=Image.open(image)
        image_array=img_to_array(image)

        
        #Area parameters
        x1=bounding_box[0]
        y1=bounding_box[1]
        x2=bounding_box[2]
        y2=bounding_box[3]

        width=x2-x1
        height=y2-y1

        #Division
        half_of_width=width//2
        half_of_height=height//2
        
        remain_width=width-half_of_width
        remain_height=height-half_of_height

        region_width=(half_of_width+1)-x1
        region_height=(half_of_height+1)-y1
        
        self.specifying_and_adding_pixels(image_array, region_height, region_width, remain_height, remain_width)
        self.seperating_matrix_values_to_lists()

        the_biggest_values_list=self.max_pooling_phase()
        string_list=self.create_a_list_of_strings(the_biggest_values_list)

        b=0
        for i in string_list:
            if b==0:
                arrays.append(first[i])

            elif b==1:
                arrays.append(second[i])

            elif b==2:
                arrays.append(third[i])
                
            else:
                arrays.append(fourth[i])

            b+=1

        feature_map=np.array([[arrays[0], arrays[1]] , [arrays[2], arrays[3]]])
        feature_map_tensor=tf.convert_to_tensor(feature_map)

        return feature_map_tensor

    def specifying_and_adding_pixels(self, image_array, region_height, region_width, remain_height, remain_width):      
        
        for i2 in range(region_height): #First Part of Region Proposal
            for i in range(region_width):
                first.append(image_array[i][i2])
                first_str.append(f"[{i}][{i2}]")
            

        
        for i2 in range(region_height): #Second Part of Region Proposal
            for i in range(remain_width):
                second.append(image_array[i][i2])
                second_str.append(f"[{i}][{i2}]")
    
        
        for i2 in range(remain_height): #Third Part of Region Proposal
            for i in range(region_width):
                third.append(image_array[i][i2])
                third_str.append(f"[{i}][{i2}]")

        
        for i2 in range(remain_height): #Fourth Part of Region Proposal
            for i in range(remain_width):
                fourth.append(image_array[i][i2])
                fourth_str.append(f"[{i}][{i2}]")

    def calculation_determinant_of_matrix(self, array):
        if type(array)!=np.array:
            raise TypeError
        
        det = np.linalg.det(array)

        return det


    def seperating_matrix_values_to_lists(self):

        for i in first:
            matrix_value=self.calculation_determinant_of_matrix(i)
            first_matrix.append(matrix_value)

        for i in second:
            matrix_value=self.calculation_determinant_of_matrix(i)
            second_matrix.append(matrix_value)

        for i in third:
            matrix_value=self.calculation_determinant_of_matrix(i)
            third_matrix.append(matrix_value)

        for i in fourth:
            matrix_value=self.calculation_determinant_of_matrix(i)
            fourth_matrix.append(matrix_value)


    def max_pooling_phase(self) -> list:
        first_matrix.sort()
        second_matrix.sort()
        third_matrix.sort()
        fourth_matrix.sort()

        first_biggest=first_matrix[len(first_matrix)-1]
        second_biggest=first_matrix[len(second_matrix)-1]
        third_biggest=first_matrix[len(third_matrix)-1]
        fourth_biggest=first_matrix[len(fourth_matrix)-1]

        return [first_biggest, second_biggest, third_biggest, fourth_biggest]
    

    def create_a_list_of_strings(self, list_of_matrixes:list):
        string_list=[]

        a=0
        for i in list_of_matrixes:
            index=list_of_matrixes.index(i)
            if a==0:
                string=first.index(first_matrix.index(index))
                string_list.append(string)

            elif a==1:
                string=second.index(second_matrix.index(index))
                string_list.append(string)

            elif a==2:
                string=third.index(third_matrix.index(index))
                string_list.append(string)

            else:
                string=fourth.index(fourth_matrix.index(index))
                string_list.append(string)
            a+=1

            return string_list
