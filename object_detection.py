
import argparse
import sys
import time

import cv2
from picamera2 import Picamera2

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

class ObjectDetection: 

  def __init__(self):
    base_options = core.BaseOptions(file_name='efficientnet_lite0.tflite', use_coral=False, num_threads=4)

    classification_options = processor.ClassificationOptions( max_results=5, score_threshold=0.0)
    options = vision.ImageClassifierOptions( base_options=base_options, classification_options=classification_options)

    self.classifier = vision.ImageClassifier.create_from_options(options)

    self.camera = Picamera2()
    self.camera.configure(self.camera.create_preview_configuration(main={"format": 'XRGB8888' , 'size': ( 640, 480) } )  ) 
    self.camera.start()


  def run(self) -> tuple[str, bool]:
    image  = self.camera.capture_array()
    image = cv2.flip(image, 0)
    image = cv2.flip(image, 1)

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tensor_image = vision.TensorImage.create_from_array(rgb_image)

    categories = self.classifier.classify(tensor_image)

    for idx, category in enumerate(categories.classifications[0].categories):
      category_name = category.category_name
      score = round(category.score, 2)

      if score > 0.05 and category_name in ['traffic light', 'street sign'] :
        return "SIGN", True
      return category_name, False


  def __del__(self):
    cv2.destroyAllWindows()


 

if __name__ == '__main__':
  ob = ObjectDetection()
  while True: 
    print( ob.run() ) 

