import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import signal
import time

def get_color_mask(image, color_bgr):
    lower_color = np.array(color_bgr) - 20
    upper_color = np.array(color_bgr) + 20
    mask = cv2.inRange(image, lower_color, upper_color)
    return mask

def find_color_location(image, mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)
        return (x, y, w, h)
    return None

def move_mouse_to_location(x, y):
    pyautogui.moveTo(x, y, duration=0.5)

def exit_program(signum=None, frame=None):
    print("程序已退出.")
    cv2.destroyAllWindows()
    exit(0)

def main():
    signal.signal(signal.SIGINT, exit_program)
    target_color_bgr = [255, 255, 255]
    ctrl_pressed = False

    while True:
        # 截图
        screen = ImageGrab.grab()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        mask = get_color_mask(frame, target_color_bgr)
        location = find_color_location(frame, mask)

        if location:
            x, y, w, h = location
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            move_mouse_to_location(x + w // 2, y + h // 2)

        cv2.imshow("Screen", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 17:  # 检测 Ctrl 键
            ctrl_pressed = True
        elif key == ord('+') and ctrl_pressed:  # 检测 + 键
            exit_program()
        elif key != 17:  # 如果其他键被按下，重置 Ctrl 状态
            ctrl_pressed = False

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()