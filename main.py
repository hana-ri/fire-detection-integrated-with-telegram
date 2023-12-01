import cv2
import requests
import numpy as np
from telegram import Bot
import threading
import asyncio
import queue
from datetime import datetime
import os

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')

TELEGRAM_BOT_TOKEN = '#'
TELEGRAM_CHAT_ID = '#'

pesan_teks = '[Peringatan] \n Api terdeteksi \n Periksa Dapur Anda Sekarang Juga!!!'

# Queue for passing messages between threads
message_queue = queue.Queue()

async def send_telegram_message_async(message, image_path):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        # mengirimkan pesan peringatan
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

        # Mengirimkan foto
        with open(image_path, "rb") as photo:
            await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)

        # Hapus image
        os.remove(image_path)
            
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

async def telegram_message_handler():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        if not message_queue.empty():
            message, image_path = message_queue.get()
            await send_telegram_message_async(message, image_path)

def object_detection(video_source):
    if video_source == '1':
        cap = cv2.VideoCapture(0)  # Use webcam
    elif video_source == '2':
        url = 'https://d907-114-124-210-229.ngrok-free.app/mjpeg/1'  # Replace with your MJPEG stream URL
        cap = cv2.VideoCapture(url)  # Use webcam

    else:
        print("Invalid video source. Exiting.")
        return


    async def display_frame():
        print("Started")
        while True:
            ret, frame = cap.read()

            fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

            # threshold jika 0 tidak terdeteksi api, jika 1 terdeteksi api
            if len(fire) > 0:
                # Simpan foto
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = f"fire_detection_{timestamp}.jpg"
                cv2.imwrite(image_path, frame)

                # Menghandle pesan yang ingin dikirim ke tele cuy
                # print("API")
                data = (pesan_teks, image_path)
                message_queue.put(data)

            # bertugas memunculkan kotak biru pada windows jika api terdeteksi
            # bisa di dimatikan dengan cara kasih komentar aja biar satu blok program for
            for (x, y, w, h) in fire:
                cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)

                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (x-20, y-40)
                font_scale = 0.5
                font_color = (255, 0, 0)
                font_thickness = 1
                line_type = cv2.LINE_AA
                text = "Api"
                cv2.putText(frame, text, org, font, font_scale, font_color, font_thickness, line_type)

            cv2.imshow('Fire detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if video_source == '1':
            cap.release()
        cv2.destroyAllWindows()

    # Start the thread for handling Telegram messages
    telegram_thread = threading.Thread(target=lambda: asyncio.run(telegram_message_handler()), daemon=True)
    telegram_thread.start()

    # Run the display_frame function in the main thread
    asyncio.run(display_frame())

if __name__ == '__main__':
    video_source = input("Select video source (1 for webcam, 2 for MJPEG streaming URL): ")
    object_detection(video_source)