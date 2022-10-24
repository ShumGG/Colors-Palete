from curses.ascii import isdigit
from pydoc import text
import tkinter as tk;
from tkinter import HORIZONTAL, Toplevel, messagebox;
from tkinter import ttk;
from tkinter import filedialog as fd;
from OpenCV import OpenCV;
import os;
import time;
import threading;

# opencv object
opencv = OpenCV();
      
padx = 10;
pady = 10;

# # # # # # # # # # # # # # # functions # # # # # # # # # # # # # # # # 

def chooseVideo():

    if (opencv.processing): 
        messagebox.showinfo(message = "A video processing is running");
        window.focus_force();
        return;

    file = fd.askopenfilename();
    if (len(file) > 0):
        route, format = os.path.splitext(file);
        if (format == ".mp4"):
            path.config(text = file);
         
            # remove focus
            window.focus_force();
            opencv.setPath(file);
            video_duration_int.config(text = opencv.getDurationVideo());

            # craete preview
            opencv.createPreview(window);
        else:
            messagebox.showinfo(message = "Invalid video format");
            chooseVideo();

def removeWidget(event):
    done.grid_remove();

def processVideo():

    if (opencv.processing):
        messagebox.showinfo(message = "A video processing is running");
        window.focus_force();
        return;

    if (start_time.get().isdigit() == False or finish_time.get().isdigit() == False):
        messagebox.showinfo(message = "Insert valid format in time");
        window.focus_force();
        return;

    video_duration = opencv.getDurationVideo();
    start_time_ = int(start_time.get());
    finish_time_ = int(finish_time.get());
    output_name = video_name.get();

    if (start_time_ < 0 or finish_time_ < 0):
        messagebox.showinfo(message = "Neither start time nor finish time can be less than zero");
        return;
      
    if (start_time_ > video_duration or finish_time_ > video_duration):
        messagebox.showinfo(message = "Neither start time nor finish time can be bigger than video duration");
        return;

    if (len(output_name) <= 0):
        messagebox.showinfo(message = "Insert output name for video");
        return;

    # creating threads for each function
    bar = threading.Thread(target = runBar, args= ());
    render = threading.Thread(target = opencv.start, args= (start_time_, finish_time_, output_name)); 
    process_time = threading.Thread(target = updateTime, args= ());
    finish = threading.Thread(target = finishVideo, args= ()); 
    
    bar.start();
    render.start();
    process_time.start();
    finish.start(); 
 
def runBar():
    done.grid_remove();
    progress_bar.grid();
    progress_time.grid();
    cancel_button.grid();
    progress_bar.start(10);

def updateTime():
    while (opencv.done == False and opencv.cancel == False):
        value = int((opencv.timing / opencv.getDurationVideo())*100);
        string = tk.StringVar();
        string.set(str(value) + "%");
        progress_time.config(text = string.get());
        time.sleep(1);
        
def finishVideo():
    
    time.sleep(5);
    if (opencv.done):
        # once video done, destroy progressbar
        progress_bar.grid_remove();
        progress_time.grid_remove();
        cancel_button.grid_remove();
    
    if (opencv.done and opencv.cancel == False):
        done.grid();
        return;
    
    finishVideo();

def cancelProcess():
    opencv.cancelProcess();
    progress_bar.grid_remove();
    progress_time.config(text="0%");
    progress_time.grid_remove();
    cancel_button.grid_remove();
    done.grid_remove();

# # # # # # # # # # # # # # #  Tkinter # # # # # # # # # # # # # # # # 

window = tk.Tk();
window.title("City pallete");
window.geometry("620x420");
window.resizable(False, False);

#enter information label
main_label = tk.LabelFrame(window, text = "Video");
main_label.grid(row = 0, column = 0, padx = 20, pady = 20);

#select video 
button_video = tk.Button(main_label, text = "Choose video", command = chooseVideo);
button_video.grid(row = 0, column = 0, padx = padx, pady = pady);
# <1> equals to <Button-1>
button_video.bind("<1>", removeWidget);

# video info
path = tk.Label(main_label, text = "./", fg = "black", borderwidth = 2 , relief= "ridge");
path.config(bg = "white", width = 45);
path.grid(row = 0, column = 1, padx = padx, pady = pady);

# video duration 
video_duration = tk.Label(main_label, text = "Duration:", fg = "white");
video_duration.grid(row = 1, column = 0, padx = padx, pady = pady);

video_duration_int = tk.Label(main_label, text = "0", fg = "black", width = 20, borderwidth = 2 , relief= "ridge");
video_duration_int.config(bg = "white", justify = "center");
video_duration_int.grid(row = 1, column = 1, padx = padx, pady = pady);

# start ime
start_label = tk.Label(main_label, text = "Start time", fg = "white");
start_label.grid(row = 2, column = 0, padx = padx, pady = pady);

start_time = tk.Entry(main_label);
start_time.config(bg = "white", fg = "black", justify = "center", borderwidth = 2 , relief= "ridge");
start_time.grid(row = 2, column = 1, padx = padx, pady = pady);

# finish time
finish_label = tk.Label(main_label, text = "Finish time", fg = "white");
finish_label.grid(row = 3, column = 0, padx = padx, pady = pady);

finish_time = tk.Entry(main_label);
finish_time.config(bg = "white", fg = "black", justify = "center", borderwidth = 2 , relief= "ridge");
finish_time.grid(row = 3, column = 1, padx = padx, pady = pady)

# video name
video_name_label = tk.Label(main_label, text = "Video name", fg = "white");
video_name_label.grid(row = 4, column = 0, padx = padx, pady = pady);

video_name = tk.Entry(main_label);
video_name.config(bg = "white", fg = "black", justify = "center", borderwidth = 2 , relief= "ridge");
video_name.grid(row = 4, column = 1, padx = padx, pady = pady)

# progress bar style
style = ttk.Style();
style.theme_use("alt");
style.configure("green.Horizontal.TProgressbar", background = "green");

# progress bar
progress_bar = ttk.Progressbar(window, orient = HORIZONTAL, length = 300, mode = "indeterminate", style = "green.Horizontal.TProgressbar");
progress_bar.grid(row = 4, column = 0);
progress_bar.grid_remove();

# progress time
progress_time = tk.Label(window, text = "0%", fg = "white");
progress_time.config(padx = 10);
progress_time.grid(row = 5, column = 0);
progress_time.grid_remove();

# done 
done = tk.Label(window, text = "Done!", fg = "green");
done.grid(row = 3, column = 0);
done.grid_remove();

# process video 
button = tk.Button(window, text = "Process video", command = processVideo);
button.grid(row = 6, column = 0, pady = 10);

# cancel process 
cancel_button = tk.Button(window, text = "Cancel process", command = cancelProcess);
cancel_button.grid(row = 7, column = 0);
cancel_button.grid_remove();

# button_video = tk.Button(window, text = "Play video", padx = 0, pady = 10, command = processVideo);
# button_video.place(x = 30, y = 500);

window.mainloop();