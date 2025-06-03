#!/usr/bin/env python3
"""
logger.py
Append chat logs with vector tags to JSON file per session.
"""

import json
import datetime
from pathlib import Path

class SessionLogger:
    def __init__(self, base_dir="logs"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.path = self.base_dir / f"session_{ts}.json"
        self.data = []

    def add(self, role, text, vectors):
        self.data.append({
            "time": datetime.datetime.now().isoformat(),
            "role": role,
            "text": text,
            "vectors": vectors
        })

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        return self.path

if __name__ == "__main__":
    # Example usage
    log = SessionLogger()
    log.add("user", "こんにちは", {"意味ベクトル": [0.1, 0.2], "方向": "遊び系"})
    log.add("assistant", "こんにちは！", {"意味ベクトル": [0.3, 0.1], "方向": "応答"})
    path = log.save()
    print("Saved", path)
