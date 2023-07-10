import torch
import cv2 as cv
from PIL import Image
import numpy as np
from torchvision.transforms import transforms

transform = transforms.Compose([
    transforms.PILToTensor()
])

image="IMG_8112.JPG"
image=Image.open(image)
image= transform(image)
image = image.float()

def Conv2D(image):
    m = torch.nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False)
    input = image
    output = m(input)
    return output


def Max_Pooling(image):
    max_pooling=torch.nn.MaxPool2d(kernel_size=(2,2))
    input=image
    output_max_pooling= max_pooling(input)
    return output_max_pooling

convolutional=Conv2D(image=image)
max_pool=Max_Pooling(image=convolutional)
print(max_pool)


