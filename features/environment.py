import os
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
        out = cv2.VideoWriter(
            "test_execution.mp4",
            fourcc,
            8.0,
            (width, height)
        )

        while recording:
            # Capture screen frame
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)

            # Convert BGRA to BGR for OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            out.write(frame)


def before_scenario(context, scenario):
    global recording

    # GitHub Actions provides CI=true.
    # Screen recording is only required when running locally.
    if not os.getenv("CI"):
        recording = True
        thread = threading.Thread(
            target=record_screen,
            daemon=True
        )
        thread.start()

    # Configure Chrome
    if os.getenv("CI"):
        # GitHub Actions / CI environment
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        context.driver = webdriver.Chrome(options=options)

    else:
        # Local Windows execution
        context.driver = webdriver.Chrome()
        context.driver.maximize_window()

    context.driver.implicitly_wait(5)


def after_scenario(context, scenario):
    global recording, out

    # Stop recording only when running locally
    if not os.getenv("CI"):
        recording = False

    # Close browser
    if hasattr(context, "driver"):
        context.driver.quit()

    # Finalize recording only when running locally
    if not os.getenv("CI") and out is not None:
        out.release()
        out = None

        print(
            "\n🎥 Screen recording saved clean as "
            "'test_execution.mp4'"
        )