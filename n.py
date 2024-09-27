import cv2
import torch
from ultralytics import YOLO
import requests
import os
import threading
import time
import sys
from concurrent.futures import ThreadPoolExecutor

model_name = sys.argv[1] if len(sys.argv) > 1 else "yolov10n.pt"
slow_mode = sys.argv[2].lower() == 'true' if len(sys.argv) > 2 else False

print(f"Loading model: {model_name} (Slow Mode: {slow_mode})")
print(torch.cuda.is_available())  #debug feature, should return "True" if CUDA is available, remove if not needed
print(torch.cuda.current_device())  #debug feature, print the current device ID, remove if not needed
print(torch.cuda.get_device_name(0))  #debug feature, prints your GPU name, remove if not needed

model = YOLO(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

#telegram bot setup
TOKEN = 'TelegramBotTokenHere' #put your telegram bot token here
CHAT_ID = 'ChatIDHere' #put your chat id here
MESSAGE = '🚨Human detected🚨' #message, that it sends, can be customized
SAVE_PATH = r'PATH' #put the path you want to save the photos to

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

detection_enabled = True

last_detection_time = 0
slow_mode_delay = 2 #customize the delay when "slow mode" checkbox was checked before launching, don't recommend going under 2 or it's gonna spam really quick and will gate rate-limited

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, json=payload)

def send_telegram_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    with open(photo_path, 'rb') as photo_file:
        payload = {'chat_id': CHAT_ID, 'caption': caption}
        files = {'photo': photo_file}
        requests.post(url, data=payload, files=files)

def process_detection(frame, screenshot_counter):
    resized_frame = cv2.resize(frame, (640, 480))
    
    screenshot_filename = f"screenshot_{screenshot_counter}.jpg"
    screenshot_path = os.path.join(SAVE_PATH, screenshot_filename)
    cv2.imwrite(screenshot_path, resized_frame)

    send_telegram_message(MESSAGE)
    send_telegram_photo(screenshot_path, MESSAGE)

executor = ThreadPoolExecutor(max_workers=5)

cap = cv2.VideoCapture(0)
screenshot_counter = 0

def check_for_telegram_commands():
    global detection_enabled, slow_mode
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    last_update_id = None

    initial_response = requests.get(url).json()
    if initial_response['ok'] and initial_response['result']:
        last_update_id = initial_response['result'][-1]['update_id']

    while True:
        response = requests.get(url).json()
        if response['ok']:
            for update in response['result']:
                if 'message' in update:
                    message = update['message']
                    text = message.get('text', '')
                    update_id = update['update_id']

                    if update_id > last_update_id:
                        last_update_id = update_id

                        if text == '/toggle': #customize command if needed
                            detection_enabled = not detection_enabled
                            status_message = "Detection Enabled" if detection_enabled else "Detection Disabled" #customize the response message if needed
                            send_telegram_message(status_message)

                        elif text == '/check': #customize command if needed
                            status_message = "Detection Status: Enabled" if detection_enabled else "Detection Status: Disabled" #customize the response message if needed
                            send_telegram_message(status_message)

threading.Thread(target=check_for_telegram_commands, daemon=True).start()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if detection_enabled:
        input_frame = cv2.resize(frame, (640, 480))
        input_tensor = torch.from_numpy(input_frame).permute(2, 0, 1).float().to(device)
        input_tensor = input_tensor.unsqueeze(0) / 255.0

        results = model(input_tensor)
        
        current_time = time.time()

        if not slow_mode or (current_time - last_detection_time) >= slow_mode_delay:
            detected_human = False
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = box.cls.cpu().numpy()
                    conf = box.conf.cpu().numpy()

                    if cls == 0 and conf > 0.65:
                        print(f"Human detected with confidence: {conf}")
                        detected_human = True
                        executor.submit(process_detection, frame.copy(), screenshot_counter)
                        screenshot_counter += 1

            if detected_human:
                last_detection_time = current_time

    window_title = f"HDWW - Model {model_name.split('.')[0][-1].upper()} - {'Ticking ON' if slow_mode else 'Ticking OFF'}"
    cv2.imshow(window_title, frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  #q to quit
        break

cap.release()
cv2.destroyAllWindows()
executor.shutdown()
