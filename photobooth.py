# import the necessary packages
import threading
import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import Queue

class PhotoBoothApp:
    def __init__(self, video_stream, output_path):
        self.video_stream = video_stream
        self.output_path = output_path

        # Properties for multi-threading
        self.run_event = True

        self.frame_video = None

        # Create the background window, and an empty panel for the live video
        self.window = tk.Tk()
        self.video_panel = None

        # Create the button to add under the video panel
        btnTakeImage = tk.Button(self.window, text="Take a Photo!",
            command=self.take_a_picture)
	btnTakeImage.pack(side="bottom", fill="both", expand="yes", padx="15",
            pady="15")

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.process_images, args=())
        self.thread.start()

        # Set title and close window callback
        self.window.wm_title("Photo Booth App")
        self.window.wm_protocol("WM_DELETE_WINDOW", self.on_close)


    def process_images(self):
        while self.run_event:
            self.show_image()
        self.stopEvent.set()
        self.video_stream.stop()
        self.window.quit()

    def on_close(self):
        # Stop the camera and quit
        print "[INFO] Exiting the Photo Booth..."
        self.run_event = False

    def show_image(self):
        self.frame = self.video_stream.read()
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # Crop the image to be square for Instagram
        height, width = image.shape[:2]
        x1 = (width-height)//2
        x2 = x1+height
        image = image[0:height, x1:x2]

        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        print "image size: %dx%d" % (image.width(), image.height())

        # if the panel is not None, we need to initialize it
        if self.video_panel is None:
            self.video_panel = tk.Label(image=image)
            self.video_panel.image = image
            self.video_panel.pack(side="left", padx="10", pady="10")
        else:
            self.video_panel.configure(image=image)
            self.video_panel.image = image

    def take_a_picture(self):
        print "Take a picture!"

from cv2 import cv
class WebcamStream:
    def __init__(self, src=0):
        # OpenCV to capture an image from device 0
        self.video = cv2.VideoCapture(src)

        self.video.set(5,30)
        self.video.set(3,1920)
        self.video.set(4,1080)

        w = self.video.get(3)
        h = self.video.get(4)
        print "[INFO] Starting video stream with resolution " + str(w) + "x" + str(h)
        (self.grabbed, self.frame) = self.video.read()

        self.running = True

    def start(self):
        threading.Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while self.running:
          (self.grabbed, self.frame) = self.video.read()

    def read(self):
        return self.frame

    def stop(self):
        self.running = False
        self.video.release()
        

video_camera = WebcamStream(0)
video_camera.start()

pb = PhotoBoothApp(video_camera, "output")
pb.window.mainloop()

cv2.destroyAllWindows()
