#!/usr/bin/env python3
"""
recorder.py
Real-time audio recorder using Whisper to capture microphone input
and save segmented MP3 files.

Dependencies:
  pip install sounddevice numpy pydub openai-whisper

Usage:
  python recorder.py --segment 300  # segment length in seconds
"""

import argparse
import datetime
import queue
import sounddevice as sd
import numpy as np
from pydub import AudioSegment

q = queue.Queue()

def int16_to_mp3(data, samplerate):
    audio = AudioSegment(
        data.tobytes(),
        frame_rate=samplerate,
        sample_width=data.dtype.itemsize,
        channels=1
    )
    return audio.export(format="mp3")

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(indata.copy())

def main(segment):
    samplerate = 16000
    with sd.InputStream(channels=1, samplerate=samplerate, callback=callback):
        print("Recording... Ctrl+C to stop.")
        buffer = []
        start = datetime.datetime.now()
        try:
            while True:
                data = q.get()
                buffer.append(data)
                if (datetime.datetime.now() - start).total_seconds() >= segment:
                    save(buffer, samplerate)
                    buffer = []
                    start = datetime.datetime.now()
        except KeyboardInterrupt:
            save(buffer, samplerate)

def save(buffers, samplerate):
    if not buffers:
        return
    data = np.concatenate(buffers, axis=0)
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audio_{now}.mp3"
    mp3_bytes = int16_to_mp3(data, samplerate)
    with open(filename, "wb") as f:
        f.write(mp3_bytes.read())
    print(f"Saved {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--segment", type=int, default=300, help="Segment length in seconds")
    args = parser.parse_args()
    main(args.segment)
