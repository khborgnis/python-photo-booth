# import the necessary packages
import threading
import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import Queue
import datetime
import os
import time
from twitter_poster import TwitterPoster

class PhotoBoothApp:
    def __init__(self, video_stream, output_path):
        self.video_stream = video_stream
        self.output_path = output_path

        self.countdown = 0
        self.to_be_written = None

        # Properties for multi-threading
        self.run_event = True

        # Create the background window, and an empty panel for the live video
        self.window = tk.Tk()

        self.window.bind("<KeyRelease>", self.keyup)

        self.video_panel = None

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.process_images, args=())
        self.thread.start()

        # Set title and close window callback
        self.window.wm_title("Photo Booth App")
        self.window.wm_protocol("WM_DELETE_WINDOW", self.on_close)


    def keyup(self, e):
        if e.char == ' ':
            self.picture_taking_thread()
        elif e.char == 'g' and self.to_be_written != None:
            self.post_image()
        elif e.char == 'q':
            self.on_close()

    def process_images(self):
        while self.run_event:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.on_close()
                return
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

        if self.to_be_written == None:
            local_frame = self.frame
        else:
            local_frame = self.to_be_written

        image = cv2.cvtColor(local_frame, cv2.COLOR_BGR2RGB)

        font = font = cv2.FONT_HERSHEY_SIMPLEX
        if self.countdown > 0:
            cv2.putText(image,"Taking picture in {}...".format(self.countdown),(10,700), font, 1,(255,255,255),2)

        elif self.to_be_written != None:
            cv2.putText(image,"Press 'G' to post, or the Space Bar to retake...",(10,700), font, 1,(255,255,255),2)

        else:
            cv2.putText(image,"Press the Space Bar to take a picture...",(10,700), font, 1,(255,255,255),2)
            

        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        print "image size: %dx%d" % (image.width(), image.height())

        # if the panel is not None, we need to initialize it
        if self.video_panel is None:
            self.video_panel = tk.Label(image=image)
            self.video_panel.image = image
            self.video_panel.pack()
        else:
            self.video_panel.configure(image=image)
            self.video_panel.image = image

    def take_a_picture(self):
        print "[INFO] Taking a picture..."
        self.to_be_written = self.frame

    def post_image(self):
        timestamp = datetime.datetime.now()
        filename = "{}.png".format(timestamp.strftime("%Y-%m-%d_%H-%M-%S"))
        path = os.path.sep.join((self.output_path, filename))

        cv2.imwrite(path, self.to_be_written.copy())
        print "[INFO] saved {}".format(filename)
        self.to_be_written = None

        twitter = TwitterPoster("config.xml", path, "#AliceInWonderlandParty #AVeryMerryUnbirthday")
        twitter.start()

    def picture_taking_thread(self):
        self.to_be_written = None

        thread = threading.Thread(target=self.delayed_picture_taking, args=())
        thread.start()

    def delayed_picture_taking(self):
        self.countdown = 5
        while self.countdown > 0:
            time.sleep(1)
            self.countdown -= 1

        self.take_a_picture()

import webcam_stream

video_camera = webcam_stream.WebcamStream(0)
video_camera.start()

pb = PhotoBoothApp(video_camera, "output")
pb.window.mainloop()

cv2.destroyAllWindows()
