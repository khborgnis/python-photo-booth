# import the necessary packages
import threading
import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import Queue

class PhotoBoothApp:
    def __init__(self, video_camera, output_path):
        self.video_camera = video_camera
        self.output_path = output_path

        # Properties for multi-threading
#        self.queue = Queue.Queue()
#        self.run_event = True

        self.frame_video = None

        # Create the background window, and an empty panel for the live video
        self.window = tk.Tk()
        self.video_panel = None

        # Create the button to add under the video panel
#        btnTakeImage = tk.Button(self.window, "Take a Photo!",
#            command=self.take_a_picture)
#	btnTakeImage.pack(side="bottom", fill="both", expand="yes", padx="15",
#            pady="15")

        # if the panel is not None, we need to initialize it

        # Set title and close window callback
        self.window.wm_title("Photo Booth App")
        self.window.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        self.show_image()
        #self.queue.put(CameraTask(self.queue, self.window, self.video_camera))

    def process_queue(self):
        while self.run_event:
            try:
                task = self.queue.get(block=False)
            except Empty:
                self.window.after(100, self.process_queue)
            else:
                self.after_idle(task)

    def on_close(self):
        # Stop the camera and quit
        print "[INFO] Exiting the Photo Booth..."
        self.run_event = False
        #self.video_camera.release()
        self.window.quit()

    def show_image(self):
        image = self.video_camera.capture_frame()
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        if self.video_panel is None:
            self.video_panel = tk.Label(image=image)
            self.video_panel.image = image
            self.video_panel.pack(side="left", padx="10", pady="10")

    def take_a_picture(self):
        return None

class VideoCamera(object):
    def __init__(self):
        # OpenCV to capture an image from device 0
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def capture_frame(self):
        rc, image = self.video.read()

        # OpenCV defaults to raw images. Do we need to conver these?
        return image

class CameraTask(threading.Thread):
    def __init__(self, queue, app, camera):
        threading.Thread.__init__(self)
        self.queue = queue
        self.camera = camera
        self.window = app

    def run(self):
        image = self.camera.capture_frame()

        if self.window.video_panel is None:
            self.window.video_panel = tk.Label(image=image)
            self.window.video_panel.image = image
            self.window.video_panel.pack(side="left", padx="10", pady="10")
        else:
            self.window.video_panel.configure(image=image)
            self.window.video_panel.image = image
video_camera = VideoCamera()

pb = PhotoBoothApp(video_camera, "output")
pb.window.mainloop()
