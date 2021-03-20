import jetson.inference
import jetson.utils
import math
import cv2
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

from SocketTables.python.socketTableClient import SocketTableClient
from constants import Constants

net = jetson.inference.detectNet(argv=['--model=torch_200_powercell.onnx', '--input_blob=input_0', '--labels=labels.txt', '--output-cvg=scores', '--output-bbox=boxes'], threshold=0.5)
camera = jetson.utils.videoSource("/dev/video0")
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file


number_frames = 0
fps = 30
duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                'caps=video/x-raw,format=BGR,width=640,height=480,framerate={}/1 ' \
                '! videoconvert ! video/x-raw,format=I420 ' \
                '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                '! rtph264pay config-interval=1 name=pay0 pt=96'.format(fps)

def detectBalls():
    img = camera.Capture()
    detections = net.Detect(img)

    ball_info = ''

    # print("This is the center data: {}".format(centerXY))
    # print("This is the width data: {}".format(width))
    # print("This is the height data: {}".format(height))

    if detections:
        for detection in detections:
            centerXY = detection.Center

            (x, y) = centerXY

            # x_formated = Constants.HEIGHT * math.tan(90 - ((360 - y) / 720) * Constants.FOV_V + Constants.THETA)
            # y_formated = x_formated * math.tan(Constants.FOV_H * ((x - 640) / 1280))

            theta_ball = (((y - 360) * (Constants.FOV_V / 720)) + Constants.THETA) * math.pi / 180
            x_formated = (Constants.HEIGHT - .083)/math.tan(theta_ball)
            theta_h = (640 - x) * (Constants.FOV_H / 1280) * math.pi / 180
            y_formated = (x_formated * theta_h)

            print(str(x) + "," + str(y))
            ball_info += '{}x{}y'.format(x_formated, y_formated)

    return ball_info

def sendData(client, value):
    client.update('balls', value)

def main():
    

    client = SocketTableClient(Constants.HOST, Constants.PORT)

    while True:
        sendData(client, detectBalls())
        print(detectBalls())




if __name__ == '__main__':
    main()
    
 
