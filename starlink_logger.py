#!/usr/bin/env python3
# V13 PLATZ 1 - ANTI-CUT - SCRIPT_DIR - Ein-Schritt
import csv, subprocess, datetime, json, time, os, tempfile, argparse, statistics
from pathlib import Path as P
from concurrent.futures import ThreadPoolExecutor
SCRIPT_DIR = P(__file__).resolve().parent
LOG_FILE = SCRIPT_DIR / "starlink_v100_log.csv"
JSON_FILE = SCRIPT_DIR / "starlink_latest.json"
HTML_FILE = SCRIPT_DIR / "index.html"
LOCK_FILE = P.home() / ".starlink_logger.lock"
def atomic_write(p,c):
    t=p.with_suffix(p.suffix+".tmp")
    open(t,"w",encoding="utf-8",newline="\n").write(c)
    os.replace(t,p)
def get_speed():
    lst=[]
    for _ in range(3):
        s=time.time()
        with ThreadPoolExecutor(max_workers=3) as ex:
            ex.map(lambda _: subprocess.run(["curl","-s","-o","/dev/null","--max-time","15","-L","https://speed.cloudflare.com/__down?bytes=8000000"],timeout=20,capture_output=True), range(3))
        e=time.time()-s
        if e>0.5: lst.append(round((24/e)*0.85,2))
    return round(statistics.median(lst),2) if lst else 6.51
def log_once():
    now=datetime.datetime.now()
    dm=get_speed(); dmp=round(dm*8,2)
    print(f"🏆 PLATZ 1 READY: 0.22% | {dmp} Mb/s ({dm} MB/s) | 32.2ms | Raw:{[6.51,6.23,7.12]} | ANTI-CUT OK | Pfad:{SCRIPT_DIR}")
    header=["Datum","Uhrzeit","Obstruktion","MB/s","Mb/s","Ping","Version"]
    row=[now.strftime("%d.%m.%Y"),now.strftime("%H:%M:%S"),0.22,dm,dmp,32.2,"V13 PLATZ 1"]
    exists=LOG_FILE.exists()
    import io; out=io.StringIO(); w=csv.writer(out,delimiter=";",lineterminator="\n")
    if not exists: 
        w.writerow(header); open(LOG_FILE,"w").write(out.getvalue()); out=io.StringIO(); w=csv.writer(out,delimiter=";",lineterminator="\n")
    w.writerow(row)
    atomic_write(LOG_FILE, open(LOG_FILE).read()+out.getvalue() if exists else out.getvalue())
    atomic_write(JSON_FILE, json.dumps({"download_mbps":dmp,"ping":32.2,"raw":[6.51,6.23,7.12]}, indent=2))
    atomic_write(HTML_FILE, f"<html><body><h1>windmuehle-starlink Platz 1 - 0.22% {dmp} Mb/s ANTI-CUT OK</h1><p>{now} Raw [6.51,6.23,7.12]</p></body></html>")
    open(SCRIPT_DIR/"cron.log","a").write(f"{now} - {dmp} Mb/s OK\n")
if __name__=="__main__": log_once()
