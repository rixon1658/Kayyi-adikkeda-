import sounddevice as sd
import numpy as np
import tkinter as tk
from queue import Queue
import time, threading, random, os, sys
import pygame
import pyttsx3
from scipy.signal import butter, lfilter

# ----------------- CONFIG -----------------
SAMPLE_RATE = 44100
BLOCK_DURATION = 0.03
BLOCKSIZE = int(SAMPLE_RATE * BLOCK_DURATION)
SENSITIVITY = 15.0
ABSOLUTE_THRESHOLD = 0.025
PEAK_THRESHOLD = 0.4
MAX_SPIKE_BLOCKS = 2
CLAP_MAX_INTERVAL = 0.8
IGNORE_PROBABILITY = 0.20
MUSIC_FILE = "gangam style.mp3"

audio_queue = Queue()

_noise_level = 1e-4
_noise_alpha = 0.01
_spike_blocks = 0

last_clap_time = 0.0
clap_count = 0
seq_after_id = None
bulb_on = False
_party_animation_id = None  

pygame.mixer.init()


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


b, a = butter_bandpass(500, 4000, SAMPLE_RATE, order=3)


def audio_callback(indata, frames, time_info, status):
    global _noise_level, _spike_blocks
    if status:
        print("Audio status:", status, file=sys.stderr)

    data = np.squeeze(indata).astype(np.float32)
    if data.size == 0:
        return

  
    data = lfilter(b, a, data)

   
    rms = np.sqrt(np.mean(data ** 2))
    peak = float(np.max(np.abs(data)))

    
    _noise_level = (1 - _noise_alpha) * _noise_level + _noise_alpha * rms
    threshold = max(ABSOLUTE_THRESHOLD, _noise_level * SENSITIVITY)

    if rms > threshold and peak > PEAK_THRESHOLD:
        _spike_blocks += 1
    else:
        if _spike_blocks > 0:
            if _spike_blocks <= MAX_SPIKE_BLOCKS:
                audio_queue.put(time.time())
            _spike_blocks = 0


def speak_async(text):
    def _worker(msg):
        try:
            engine = pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
        except Exception as e:
            print("TTS error:", e, file=sys.stderr)
    threading.Thread(target=_worker, args=(text,), daemon=True).start()

def start_music():
    if not os.path.exists(MUSIC_FILE):
        speak_async("Music file not found.")
        return
    try:
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play()
    except Exception as e:
        print("Music play error:", e, file=sys.stderr)
        speak_async("Couldn't play the music.")

def stop_music():
    try:
        pygame.mixer.music.stop()
    except:
        pass


root = None
canvas = None
bulb_item = None
status_label = None

def update_bulb_visual(color=None):
    global bulb_on
    fill = "yellow" if bulb_on else "gray20" if color is None else color
    canvas.itemconfig(bulb_item, fill=fill)

def set_status(text):
    status_label.config(text=text)


def party_step():
    global _party_animation_id
    if pygame.mixer.music.get_busy():
        r = random.randint(150, 255)
        g = random.randint(80, 255)
        b = random.randint(0, 200)
        color = f"#{r:02x}{g:02x}{b:02x}"
        update_bulb_visual(color)
        _party_animation_id = root.after(150, party_step)
    else:
        update_bulb_visual(None)
        _party_animation_id = None

def stop_party_animation():
    global _party_animation_id
    if _party_animation_id is not None:
        root.after_cancel(_party_animation_id)
        _party_animation_id = None


def handle_claps(n):
    global bulb_on
    phrases_ignore = [
        "Ineechu poda.",
        "I'm on a break.",
        "Ask me later.",
        "Nope, too lazy."
    ]
    if random.random() < IGNORE_PROBABILITY:
        set_status("Ignored (sassy).")
        speak_async(random.choice(phrases_ignore))
        return

    if n == 1:
        bulb_on = True
        update_bulb_visual(None)
        set_status("1 clap: Light ON")
        speak_async("Light on")
        stop_music()
        stop_party_animation()
    elif n == 2:
        bulb_on = False
        update_bulb_visual(None)
        set_status("2 claps: Light OFF")
        speak_async("Light off")
        stop_music()
        stop_party_animation()
    else:
        bulb_on = True
        update_bulb_visual(None)
        set_status(f"{n} claps: Party mode!")
        speak_async("Party mode on")
        start_music()
        stop_party_animation()
        party_step()

def process_audio_queue():
    global last_clap_time, clap_count, seq_after_id
    while not audio_queue.empty():
        t = audio_queue.get()
        if last_clap_time == 0 or (t - last_clap_time) > CLAP_MAX_INTERVAL:
            clap_count = 1
        else:
            clap_count += 1
        last_clap_time = t
        set_status(f"Detected clap — sequence count {clap_count}")

        if seq_after_id is not None:
            root.after_cancel(seq_after_id)
        seq_after_id = root.after(int(CLAP_MAX_INTERVAL * 1000) + 50, on_clap_sequence_timeout)

    root.after(20, process_audio_queue)

def on_clap_sequence_timeout():
    global clap_count, last_clap_time, seq_after_id
    cnt = clap_count
    clap_count = 0
    last_clap_time = 0.0
    seq_after_id = None
    set_status(f"Processing {cnt} clap(s)...")
    handle_claps(cnt)


def on_closing():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
    root.destroy()

def main():
    global root, canvas, bulb_item, status_label
    root = tk.Tk()
    root.title("Kayyi adikeda!!!")
    root.geometry("360x420")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=320, height=320, bg="black", highlightthickness=0)
    canvas.pack(padx=10, pady=10)
    bulb_item = canvas.create_oval(60, 60, 260, 260, fill="gray20", outline="white", width=2)

    status_label = tk.Label(root, text="Waiting for claps...", font=("Helvetica", 12))
    status_label.pack(pady=6)

    try:
        stream = sd.InputStream(callback=audio_callback, channels=1,
                                samplerate=SAMPLE_RATE, blocksize=BLOCKSIZE)
        stream.start()
    except Exception as e:
        set_status("Could not open microphone. Check device & drivers.")
        print("Failed to start audio stream:", e, file=sys.stderr)

    root.after(20, process_audio_queue)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
