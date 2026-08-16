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
        monitor = sct.monitors[1]
        width = monitor["width"]
        height = monitor["height"]

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            "test_execution.mp4",
            fourcc,
            8.0,
            (width, height)
        )

        while recording:
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            out.write(frame)


def before_scenario(context, scenario):
    global recording

    is_ci = os.getenv("CI", "").lower() == "true"

    # Start screen recording only when running locally
    if not is_ci:
        recording = True

        thread = threading.Thread(
            target=record_screen,
            daemon=True
        )
        thread.start()

    # Configure Chrome
    if is_ci:
        options = webdriver.ChromeOptions()

        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        context.driver = webdriver.Chrome(options=options)

    else:
        context.driver = webdriver.Chrome()
        context.driver.maximize_window()

    context.driver.implicitly_wait(5)


def after_scenario(context, scenario):
    global recording, out

    is_ci = os.getenv("CI", "").lower() == "true"

    # Stop recording only when running locally
    if not is_ci:
        recording = False

    # Close browser
    if hasattr(context, "driver"):
        context.driver.quit()

    # Finalize recording only when running locally
    if not is_ci and out is not None:
        out.release()
        out = None

        print(
            "\n🎥 Screen recording saved clean as "
            "'test_execution.mp4'"
        )