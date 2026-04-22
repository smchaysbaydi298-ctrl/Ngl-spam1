#!/usr/bin/env python3
import threading
import requests
import time
import random
import sys
import os
from uuid import uuid4

def clear():
    os.system('clear')

def show_header():
    print("\033[1;32m" + """
   ███╗   ██╗ ██████╗ ██╗         ███████╗██████╗  █████╗ ███╗   ███╗
   ████╗  ██║██╔════╝ ██║         ██╔════╝██╔══██╗██╔══██╗████╗ ████║
   ██╔██╗ ██║██║  ███╗██║         ███████╗██████╔╝███████║██╔████╔██║
   ██║╚██╗██║██║   ██║██║         ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║
   ██║ ╚████║╚██████╔╝███████╗    ███████║██║     ██║  ██║██║ ╚═╝ ██║
   ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝
""" + "\033[0m")
    print("\033[1;36mมันไม่ร้องเราไม่หยุด!\033[0m")
    print("\033[1;33m" + "="*40 + "\033[0m\n")

def send_spam(username, messages, max_bombs, threads):
    success = 0
    fail = 0
    running = True

    def worker():
        nonlocal success, fail, running
        while running:
            if max_bombs > 0 and (success + fail) >= max_bombs:
                running = False
                break
            url = "https://ngl.link/api/submit"
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 14)",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "username": username,
                "question": random.choice(messages),
                "deviceId": str(uuid4()),
                "gameSlug": "",
                "referrer": ""
            }
            try:
                r = requests.post(url, data=data, headers=headers, timeout=5)
                if r.status_code == 200:
                    success += 1
                else:
                    fail += 1
            except:
                fail += 1
            time.sleep(random.uniform(0.5, 1.2))

    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    print(f"\n\033[36m[+] เริ่มสแปม @{username}\033[0m")
    if max_bombs > 0:
        print(f"[🎯] เป้าหมาย: {max_bombs} ครั้ง, เธรด: {threads}")
    else:
        print("[🎯] โหมดไม่จำกัด (กด Ctrl+C เพื่อหยุด)\n")

    try:
        while running:
            total = success + fail
            if max_bombs > 0 and total >= max_bombs:
                running = False
                break
            sys.stdout.write(f"\r\033[36m▶ สำเร็จ: {success} | ล้มเหลว: {fail} | รวม: {total}" + (f"/{max_bombs}" if max_bombs>0 else "") + "\033[0m")
            sys.stdout.flush()
            time.sleep(0.8)
    except KeyboardInterrupt:
        running = False
        print("\n\033[33m[!] หยุดด้วย Ctrl+C\033[0m")

    time.sleep(0.5)
    print(f"\n\033[32m[✓] สแปมหยุดแล้ว ส่งสำเร็จ {success} ครั้ง, ล้มเหลว {fail} ครั้ง\033[0m")

def main_loop():
    while True:
        clear()
        show_header()
        print("\033[1;33m--- เมนูหลัก ---\033[0m")
        print("[1] .เริ่มใช้งาน💣")
        print("[2] .ออกจากโปรแกรม👋")
        choice = input("\033[36mเลือก (1/2): \033[0m").strip()
        if choice == "2":
            clear()
            print("\033[31m[✗] ออกจากโปรแกรม ตามคำสั่ง El manco\033[0m")
            sys.exit(0)
        elif choice != "1":
            print("\033[31m[!] กรุณาเลือก 1 หรือ 2\033[0m")
            time.sleep(1)
            continue

        username = input("\033[33m[?] ชื่อผู้ใช้ (ไม่ใส่ @): \033[0m").strip()
        if not username:
            print("\033[31m[!] ต้องใส่ชื่อ\033[0m")
            time.sleep(1)
            continue

        mode = input("\033[33m[?] โหมด (1=ข้อความเดียว, 2=สุ่มจากไฟล์) [Enter=1]: \033[0m").strip()
        messages = []
        if mode == "2":
            try:
                with open("messages.txt", "r", encoding="utf-8") as f:
                    messages = [l.strip() for l in f if l.strip()]
                if not messages:
                    raise Exception
                print(f"\033[32m[✓] โหลด {len(messages)} ข้อความ\033[0m")
            except:
                print("\033[31m[!] ไม่มี messages.txt ใช้ข้อความตัวอย่าง\033[0m")
                messages = ["สวัสดี", "ว่าไง", "เทส"]
        else:
            msg = input("\033[33m[?] ข้อความที่ใช้สแปม: \033[0m").strip()
            if not msg:
                print("\033[31m[!] ต้องใส่ข้อความ\033[0m")
                time.sleep(1)
                continue
            messages = [msg]

        limit = input("\033[33m[?] จำนวนครั้งที่ต้องการส่ง (0 หรือ Enter = ไม่จำกัด): \033[0m").strip()
        max_bombs = int(limit) if limit.isdigit() and int(limit) > 0 else 0
        threads = max_bombs if max_bombs > 0 else 30
        if max_bombs > 0:
            print(f"\033[32m[✓] จะส่ง {max_bombs} ครั้ง ใช้ {threads} เธรด\033[0m")
        else:
            print("\033[32m[✓] โหมดไม่จำกัด ใช้ 30 เธรด (กด Ctrl+C หยุด)\033[0m")

        send_spam(username, messages, max_bombs, threads)
        input("\n\033[36mกด Enter เพื่อกลับไปเมนูหลัก...\033[0m")

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        clear()
        print("\033[31m[✗] ตรวจจับ Ctrl+C รวม ออกจากโปรแกรม\033[0m")
        sys.exit(0)
