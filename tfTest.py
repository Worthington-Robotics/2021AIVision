import os
import cv2

MODELS_DIR = '/home/worbotsai/TensorflowTest/Expanded_50K/saved_model'
import tensorflow as tf

import numpy as np

from cscore import CameraServer

cs = CameraServer.getInstance()
output = cs.putVideo("bboxes", 720, 360)

detect_fn = tf.saved_model.load(MODELS_DIR)
print("hi")

cap = cv2.VideoCapture(0)

while True:

    tfBoxes = []

    ret, image_np = cap.read()

    image_np_expanded = np.expand_dims(image_np, axis=0)

    # image_np = np.array(np.random.random_sample((3, 300, 300)), dtype=np.float32)

    input_tensor = tf.convert_to_tensor(image_np_expanded, name='input_0')

    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # input_tensor = np.expand_dims(image_np, 0)
    detections = detect_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
    detections['num_detections'] = num_detections
    #print("Detection num " + str(detections['num_detections']))

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    for j in range(len(detections['detection_scores'])):
        if(detections['detection_scores'][j] > .98):
            (ymin, xmin, ymax, xmax) = tuple(detections['detection_boxes'][j])
            tfBoxes.append((xmin, xmax, ymin, ymax))

    cv2.rectangle(image_np, (xmin, ymin), (xmax, ymax), (255, 255, 255), 5)

    output.putFrame(image_np)