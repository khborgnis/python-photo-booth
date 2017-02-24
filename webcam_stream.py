import threading
import cv2

class WebcamStream:
    def __init__(self, src=0):
        # OpenCV to capture an image from device 0
        self.webcam = cv2.VideoCapture(src)

        self.webcam.set(cv2.cv.CV_CAP_PROP_FOURCC, cv2.cv.CV_FOURCC('M', 'J', 'P', 'G') );
        self.webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ,1280);
        self.webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ,720);
#        self.webcam.set(5,30)

        w = self.webcam.get(3)
        h = self.webcam.get(4)
#        fps = self.webcam.get(8)
#        fourcc = self.webcam.get(cv2.cv.CV_CAP_PROP_FOURCC)

        print "[INFO] Starting video stream with resolution " + str(w) + "x" + str(h)
        (self.grabbed, self.frame) = self.webcam.read()

        self.running = True

    def start(self):
        threading.Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while self.running:
          (self.grabbed, self.frame) = self.webcam.read()

    def read(self):
        return self.frame

    def stop(self):
        self.running = False
        self.webcam.release()


if __name__ == "__main__":
    stream = WebcamStream()

    while(True):
        (ret, frame) = stream.webcam.read()

        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    stream.stop()
    cv2.destroyAllWindows()
