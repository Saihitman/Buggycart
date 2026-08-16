import cv2
import numpy as np
import threading
from mss import mss
from selenium import webdriver

# Global variables to control recording
recording = False
out = None

def record_screen():
    global recording, out
    
    with mss() as sct:
        # Get primary monitor resolution
        monitor = sct.monitors[1]
        width = monitor["width"]
        height = monitor["height"]
        
        # Define codec and VideoWriter (MP4 format)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter("test_execution.mp4", fourcc, 8.0, (width, height))

        while recording:
            # Capture fast screenshot frame
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            
            # Convert BGRA (MSS default) to BGR for OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            out.write(frame)

def before_scenario(context, scenario):
    global recording
    
    # 1. Start background recording thread
    recording = True
    thread = threading.Thread(target=record_screen, daemon=True)
    thread.start()

    # 2. Launch Google Chrome
    context.driver = webdriver.Chrome()
    context.driver.implicitly_wait(5)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    global recording, out
    
    # 1. Stop recording loop first
    recording = False
    
    # 2. Close browser
    if hasattr(context, "driver"):
        context.driver.quit()

    # 3. Finalize and close video file properly to prevent corruption
    if out is not None:
        out.release()
        out = None
        print("\n🎥 Screen recording saved clean as 'test_execution.mp4'")