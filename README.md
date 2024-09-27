# HDWW
Note: This requires powerful CPU, GPU and a lot of RAM.
Requirements: CUDA 12.6, Python 3.12, Telegram Bot, torch, opencv-python, ultralytics, Windows 11 (I believe that Win 10 will work)...

To set this up
1. Download all the requirements
2. flet create hwdd | put the .py files in it
3. Open loader.py in any code editor
4. Copy file path of "n.py" and paste it to 20th line between the quotation marks
5. Save the loader.py and open n.py in any code editor
6. Paste your Telegram Bot Token between the apostrophes (25th line)
7. Paste your Chat ID (26th line)
8. Paste the path you want captured frames to be saved to (28th line)
(OPTIONAL) 9. Save n.py, customize lines: 27, 36, 86, 88, 91, 92 if you want.
(OPTIONAL) 10. Remove any debug code/text at:
loader.py, Lines 1-7 (ASCII Text)
n.py, Lines 15-17 (Debug code)
(OPTIONAL) 11. Build the app (flet build windows, you might need to install additional software and you might get some erros)

. Remove any debug features if you don't want them


This project uses [YOLOv10](https://github.com/THU-MIG/yolov10)n/x to detect Humans via your webcam/camera, then confirms that it's confidence, that the object it detected is above 0.65 (Customizable), then proceeds to save the frame, send a message via Telegram Bot with customizable text and the frame it captured. Consider modifying this project to use YOLOv5/YOLOv8 if your PC isn't strong enough.
