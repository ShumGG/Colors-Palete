import cv2;
import numpy as np;
import os;
from Thread import RenderThread;
from pathlib import Path;
from VideoParams import VideoParams;
from Image import Image;
import time;
import tkinter as tk;

class OpenCV:

    HOME_DIRECTORY = Path.home();

    def __init__(self, file_path = ""):
        self.video_params = "";
        self.file_path = file_path;
        self.current_directory = "";
        self.width = "";
        self.height = "";
        self.output = "";
        self.video = "";
        self.fps = 0;
        self.each_frame_duration = 0;
        self.count = 0;
        self.start_time = 0;
        self.finish_time = 0;
        self.duration = 0;
        self.timing = 0;
        self.done = False;
        self.processing = False;
        self.loop = True;
        self.cancel = False;
        self.thread = RenderThread(self.render);
        self.output_name = "";
    
    def setPath(self, file_path):
        self.file_path = file_path;
        self.init();

    def getInfo(self):
        return self.file_path;

    def getDurationVideo(self):
        return self.duration;

    def init(self):
        self.video = cv2.VideoCapture(self.file_path);
        self.fps = self.video.get(cv2.CAP_PROP_FPS);
        self.frame_count = self.video.get(cv2.CAP_PROP_FRAME_COUNT);
        self.each_frame_duration = int(1000/self.fps);
        self.duration = int(self.frame_count / self.fps);
        self.timing = 0;

        # if thread is reset, create new instance
        if (self.thread == None):
            self.thread = RenderThread(self.render);
  
        # getting video properties
        if self.video.isOpened(): 
            self.width  = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
            self.height  = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `width`

    def createPreview(self, root):
        # create preview instance object
        self.video_params = VideoParams(root, self.file_path, self.width, self.height);

    def start(self, start, finish, output_name):
        
        # getting current directoy to save edited version and audio
        self.start_time = start;
        self.finish_time = finish;
        self.output_name = output_name;
        self.count = 0;
        self.done = False;
        self.loop = True;
        self.current_directory = os.getcwd();
    
        #extracting the audio from the video
        #-y to auto overwritte if exist
        os.system(f"ffmpeg -i '{self.file_path}' -vn -y {self.HOME_DIRECTORY}/Desktop/video_audio.mp3");

        #getting ready the writter
        # saving it with the same fps and resolution
        self.output = cv2.VideoWriter(f"{self.HOME_DIRECTORY}/Desktop/edited.mp4", cv2.VideoWriter_fourcc('m','p','4','v'), self.fps, (self.width, self.height));

        # processing to true
        self.processing = True;

        #creating thread
        self.thread.start();
    
    def getTopLevel(self):
        return tk.Toplevel.winfo_exists(self.video_params);

    def render(self):
        
        while self.loop:
            # print("seguimos render");
            grabbed, frame = self.video.read();

            if grabbed == True:

                self.count += 1;
                self.timing = int(self.count / self.fps);

                hh, ww = frame.shape[:2]
                w, h = (self.video_params.getNumberColors(), self.video_params.getNumberColors());

                result = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
             
                if (self.timing > 0 and self.timing >= self.start_time and self.timing < self.finish_time):
                    for i, row in enumerate(result):
                        my_array = np.array(result[i]);
                        max_values = my_array.max(0);
                        r, g, b = (int(max_values[0]),int(max_values[1]),int(max_values[2]));
                        cx, cy = self.video_params.getX(), int(self.height/2)-self.video_params.getY();
                        
                        # creating each rectangle of color
                        size = (self.video_params.getWidth(), self.video_params.getHeight());
                        # top_left = (30, cy + (i*size[1]));
                        top_left = (cx, cy + (i*size[1]));
                        bottom_right = (cx + size[0], cy + (size[1] * (i+1)));
                        cv2.rectangle(frame, top_left, bottom_right, (r, g, b), -1);
                
                video_output = cv2.resize(frame,(self.width,self.height));
                self.output.write(video_output);

            else:   
                self.loop = False;
                break;

        self.output.release();
        self.video.release();
        
        if (self.cancel): 
            self.done = True;
            cv2.destroyAllWindows();
            return;
        else:
            
            os.system(f"ffmpeg -i {self.HOME_DIRECTORY}/Desktop/edited.mp4 -i {self.HOME_DIRECTORY}/Desktop/video_audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -b:a 320k -y {self.HOME_DIRECTORY}/Desktop/{self.output_name}.mp4");

            # delete temporary files 
            os.remove(f"{self.HOME_DIRECTORY}/Desktop/edited.mp4");
            os.remove(f"{self.HOME_DIRECTORY}/Desktop/video_audio.mp3");
            
            time.sleep(3);
            self.done = True;
            self.processing = False;
            
            # stop thread
            self.thread.stop();
            # reset thread
            self.thread = None;

            cv2.destroyAllWindows();

    def cancelProcess(self):

        os.remove(f"{self.HOME_DIRECTORY}/Desktop/edited.mp4");
        os.remove(f"{self.HOME_DIRECTORY}/Desktop/video_audio.mp3");

        self.loop = False;
        self.cancel = True;
        self.processing = False;

        self.thread.stop();
        # reset thread
        self.thread = None;