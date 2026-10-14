#!/usr/bin/env python3
import random, datetime
from pathlib import Path
ideen_file = Path.home() / "windmuehle-starlink/bot_ideen.txt"
log_file = Path.home() / "starlink_bot_training.csv"

ideen = ideen_file.read_text(encoding="utf-8").splitlines()
idee = random.choice([i for i in ideen if i.strip()])

now = datetime.datetime.now()
exists = log_file.exists()
import csv
with open(log_file, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    if not exists:
        w.writerow(["Datum","Uhrzeit","Idee","Quelle"])
    w.writerow([now.strftime("%d.%m.%Y"), now.strftime("%H:%M:%S"), idee, "Gitterrost Windmuehle FINAL 6.96 MB/s"])

print(f"BOT TRAINING {now.strftime('%H:%M:%S')}: {idee} -> {log_file}")

# Hier kannst du spaeter deinen echten Bot API Call einfuegen:
# import subprocess; subprocess.run(["curl","-X","POST","http://dein-bot/api/train","-d",idee])
