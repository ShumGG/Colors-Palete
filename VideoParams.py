import tkinter as tk;
from Thread import RenderThread;
from VideoPreview import VideoPreview;
from tkinter import messagebox;

class VideoParams(tk.Toplevel):

    def __init__(self, parent, file_path, video_width, video_height):
        
        super().__init__(parent)
        
        self.title("Video Params");
        self.resizable(False, False);
        self.padx = 20;
        self.pady = 20;
        self.fg = "white";  
     
        # main label
        main_label = tk.LabelFrame(self, text = "Video Params");
        main_label.grid(row = 0, column = 0, padx = self.padx, pady = self.pady);

        # x position
        x_label = tk.Label(main_label, text = "X:", fg = self.fg);
        x_label.grid(row = 0, column = 0, padx = self.padx, pady = self.pady);

     
        self.x_entry = tk.Entry(main_label, fg = self.fg);
        self.x_entry.insert(0, "30");
        self.x_entry.grid(row = 0, column = 1, padx = self.padx, pady = self.pady);

        # y position
        y_label = tk.Label(main_label, text = "Y: ", fg = self.fg);
        y_label.grid(row = 1, column = 0, padx = self.padx, pady = self.pady);

        self.y_entry = tk.Entry(main_label);
        self.y_entry.insert(0, "300");
        self.y_entry.grid(row = 1, column = 1, padx = self.padx, pady = self.pady);

        # color width
        color_width_label = tk.Label(main_label, text = "Width:", fg = self.fg);
        color_width_label.grid(row = 2, column = 0, padx = self.padx, pady = self.pady);

        self.color_width_entry = tk.Entry(main_label, textvariable = "15");
        self.color_width_entry.insert(0, "15");
        self.color_width_entry.grid(row = 2, column = 1, padx = self.padx, pady = self.pady);

        # color height
        color_height_label = tk.Label(main_label, text = "Height:", fg = self.fg);
        color_height_label.grid(row = 3, column = 0, padx = self.padx, pady = self.pady);

        self.color_height_entry = tk.Entry(main_label);
        self.color_height_entry.insert(0, "100");
        self.color_height_entry.grid(row = 3, column = 1, padx = self.padx, pady = self.pady);

        # number colors
        number_colors = tk.Label(main_label, text = "Number colors", fg = self.fg);
        number_colors.grid(row = 4, column = 0, padx = self.padx, pady = self.pady);

        self.number_colors_entry = tk.Entry(main_label);
        self.number_colors_entry.insert(0, "6");
        self.number_colors_entry.grid(row = 4, column = 1, padx = self.padx, pady = self.pady);

        # preview
        self.render_button = tk.Button(main_label, text = "Preview", width = 15, command = self.showPreview);
        self.render_button.grid(row = 5, column = 0, padx = self.padx, pady = self.pady);

        # preview
        self.render_button = tk.Button(main_label, text = "Done", width = 15, command = self.done);
        self.render_button.grid(row = 5, column = 1, padx = self.padx, pady = self.pady);

        self.video = VideoPreview(parent, file_path, video_width, video_height);
        self.thread = RenderThread(self.video.run);

        self.runPreview();


    def getX(self):
        return self.video.x;
    
    def getY(self):
        return self.video.y;
    
    def getWidth(self):
        return self.video.color_width;
    
    def getHeight(self):
        return self.video.color_height;
    
    def getNumberColors(self):
        return self.video.number_colors;

    def showPreview(self):  

        if (not self.x_entry.get().isnumeric() or not self.y_entry.get().isnumeric()):
            messagebox.showinfo(message = "Wrong value in x or y");
            return;

        if (not self.color_width_entry.get().isnumeric() or not self.color_height_entry.get().isnumeric()):
            messagebox.showinfo(message = "Wrong value in width color or height color");
            return;

        if (not self.number_colors_entry.get().isnumeric()):
            messagebox.showinfo(message = "Wrong value in number colors");
            return;

        x = int(self.x_entry.get());
        y = int(self.y_entry.get());
        color_width_entry = int(self.color_width_entry.get());
        color_height_entry = int(self.color_height_entry.get());
        number_colors = int(self.number_colors_entry.get());

        self.video.setValues(x, y, color_width_entry, color_height_entry, number_colors);
    
    def runPreview(self):
        self.video.start();
  
    def done(self):
        self.video.stop();
        self.destroy();