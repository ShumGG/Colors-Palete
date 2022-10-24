import cv2;
from Thread import RenderThread;
import copy;

class VideoPreview():

    COLORS = [
        (0,255,255), 
        (0,255,0), 
        (238,173,14),
        (205,102,0), 
        (255,0,0), 
        (113,113,198),
        (0,205,102), 
        (154,50,205),
        (205,50,120),
        (176,23,31)
    ]

    def __init__(self, parent, path, video_width, video_height):

        self.thread = RenderThread(self.run);
        self.keep = False;
        self.frame = None;
        self.original_frame = None;
        self.root = parent;
        self.video = cv2.VideoCapture(path);
        self.video_width = video_width;
        self.video_height = video_height;
        self.x = 30;
        self.y = 300;
        self.color_width = 15;
        self.color_height = 100;
        self.number_colors = 6;
    
    def show_image(self):
        if self.frame is not None:  
            
            # need to use copy because this way wont edit the original frame that is saved in a memory address
            frame = copy.copy(self.frame);

            for i in range(self.number_colors):
                
                size = (self.color_width, self.color_height);
                cx, cy = self.x, int(self.video_height/2) - self.y;
                       
                top_left = (cx, cy + (i*size[1]));
                bottom_right = (cx + size[0], cy + (size[1] * (i+1)));
                
                cv2.rectangle(frame, top_left, bottom_right, self.COLORS[i], -1);
                
            cv2.imshow("Video", frame);
      
        if not self.keep:
            self.root.after(1000, self.show_image)

    def setValues(self, x, y, color_width, color_height, number_colors):
        self.x = x;
        self.y = y;
        self.color_width = color_width;
        self.color_height = color_height;
        self.number_colors = number_colors;

    def start(self):    
        self.keep = False;
        self.thread.start();
        self.root.after(1000, self.show_image);

    def stop(self):
        self.keep = True;
        self.frame = None;
        self.thread.stop();
        cv2.destroyAllWindows();
    
    def run(self):  
        
        if (self.keep):
            return;

        grabbed, self.frame = self.video.read();

        self.video.release();
        
        cv2.waitKey(0);