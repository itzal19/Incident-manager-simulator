from typing import List

history_file = "logs/events.log"

def save_history(history: List[str]):
    with open(history_file, "w", encoding="utf-8") as f:
        for line in history:
            f.write(line + "\n")