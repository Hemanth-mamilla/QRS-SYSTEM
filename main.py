# DOCUMENTATION SECTION
''' 
   DATE : 06/07/2024
   NAME : VARIKALA ANIL, VALA KARTHIK
   PROJECT-TITLE : QRS (QUICK REVIEW SYSTEM)
   LANGUAGE : PYTHON
'''

# Importing necessary modules
import tkinter as tk
from tkinter.ttk import Style
import cv2
import PIL.Image, PIL.ImageTk  # pip install pillow
from functools import partial
import threading
import imutils
import time

# Adjusting widths and heights of the images
SET_WIDTH = 650
SET_HEIGHT = 380

# Create main window
window = tk.Tk()
window.title("QUICK REVIEW SYSTEM")

# Load and display initial image
cv_img = cv2.cvtColor(cv2.imread("drs.png"), cv2.COLOR_BGR2RGB)
cv_img = imutils.resize(cv_img, width=SET_WIDTH, height=SET_HEIGHT)

canvas = tk.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tk.NW, image=photo)
canvas.pack()

# Load video stream
stream = cv2.VideoCapture("match.mp4")

# Flag to toggle "Decision Pending" display
flag = True

# Function to control video playback
def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")

    # Move frame pointer
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        return

    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

    if flag:
        canvas.create_text(120, 25, fill="black", font="Times 20 italic bold", text="Decision Pending")
    flag = not flag

# Function to show pending -> decision (out/not out)
def pending(decision):
    # Show "Decision Pending" image
    frame = cv2.cvtColor(cv2.imread("decision_pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

    time.sleep(2)

    # Show "Out" or "Not Out"
    decision_image = "out.png" if decision == "out" else "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decision_image), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

    print(f"Displayed decision: {decision.upper()}")

# Button functions
def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = True
    thread.start()
    print("Player is OUT")

def not_out():
    thread = threading.Thread(target=pending, args=("not_out",))
    thread.daemon = True
    thread.start()
    print("Player is NOT OUT")

# Buttons for video control and decisions
buttons = [
    ("<< Previous (fast)", -3),
    ("<< Previous (slow)", -1),
    ("Next (slow) >>", 1),
    ("Next (fast) >>", 3),
]

for (text, speed) in buttons:
    btn = tk.Button(window, text=text, width=50, command=partial(play, speed))
    btn.pack()

# Decision buttons
tk.Button(window, text="Give OUT", width=50, command=out).pack()
tk.Button(window, text="Give NOT OUT", width=50, command=not_out).pack()

# Start the GUI event loop
window.mainloop()
