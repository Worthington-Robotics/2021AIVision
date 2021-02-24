import cv2, time, numpy as np, os
import json
from cscore import CameraServer, UsbCamera, VideoSource
import tflite_runtime.interpreter as tflite

scriptLoc = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(scriptLoc, "200k_odd_converted.tflite")

start = time.time()

interpreter = tflite.Interpreter(model_path = model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

end = time.time()

print('Model loaded in: ' + str(end - start) + 's\n')

cs = CameraServer.getInstance()

camera1 = UsbCamera("Vision", 0)

frame = cs.getVideo(camera=camera1)

print("Started Looping\n")

while True:

    start = time.time()

    (frame_time, input_img) = frame.grabFrame(None)


    if(input_img is not None):
        
        input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

        input_data = np.expand_dims(input_img, axis=0)

        print(input_data.shape)

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
        scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects

        imH = 640
        imW = 320

        for i in range(len(scores)):
            if ((scores[i] > .1) and (scores[i] <= 1.0)):

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))

                print("Top Left ({}, {})\n".format(xmin, ymax))
                print("Top Right ({}, {})\n".format(xmax, ymax))
                print("Bottom Left ({}, {})\n".format(xmin, ymin))
                print("Bottom Right ({}, {})\n".format(xmax, ymin))

    end = time.time()

    print("Processed frame in: {}".format(str(end - start)) + "s\n")