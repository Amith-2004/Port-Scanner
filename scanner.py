import socket
import threading
import time
from datetime import datetime

print("🛠️ Ultra Port Scanner\n")

target = input("Enter IP address or domain: ")
start_port = int(input("Start port: "))
end_port = int(input("End port: "))
timeout = 1  # timeout in seconds

start_time = datetime.now()

# Try resolving domain and reverse DNS
try:
    ip = socket.gethostbyname(target)
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        hostname = "No reverse DNS"
    print(f"\n🎯 Target IP: {ip}")
    print(f"🔁 Reverse DNS: {hostname}")
except socket.gaierror:
    print("❌ Invalid IP or domain.")
    exit()

print(f"\n🔎 Scanning ports {start_port} to {end_port}...\n")

print_lock = threading.Lock()
open_ports = []
results = []

# Dictionary of banner clues
banner_tips = {
    "Apache": "📝 Web server (likely HTTP). Often found on Linux servers.",
    "nginx": "📝 Lightweight HTTP reverse proxy. Common on modern sites.",
    "OpenSSH": "🔐 SSH server for secure remote login.",
    "FTP": "📂 File Transfer Protocol server.",
    "SMTP": "📧 Mail server (Sendmail, Postfix, etc).",
    "MySQL": "🛢️ MySQL Database server.",
    "Microsoft-IIS": "💻 Microsoft's web server (IIS).",
}

def grab_banner(sock, port):
    try:
        sock.send(b'HEAD / HTTP/1.1\r\n\r\n')
        banner = sock.recv(1024).decode(errors='ignore').strip()
        first_line = banner.split("\n")[0]
        return first_line
    except:
        return "No banner received"

def explain_banner(banner):
    for key in banner_tips:
        if key.lower() in banner.lower():
            return banner_tips[key]
    return "ℹ️ Unknown service or custom application."

def scan_port(port):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            banner = grab_banner(s, port)
            banner_info = explain_banner(banner)

            with print_lock:
                msg = f"✅ Port {port} OPEN ({service}) → {banner}"
                print(msg)
                print(f"   ↳ {banner_info}")
                results.append(f"Port {port} OPEN ({service}) → {banner}\n   {banner_info}")
                open_ports.append(port)
        s.close()
    except:
        pass

# Create threads
threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

# Final output
if not open_ports:
    print("❌ No open ports or banners found.")

print(f"\n⏱️ Scan finished in {duration:.2f} seconds.")
print("✅ Scan Complete!")

# Save to file
filename = input("\n📁 Enter filename to save results (e.g., output.txt): ")
with open(filename, "w") as f:

    f.write(f"Scan Results for {target} ({ip})\n")
    f.write(f"Reverse DNS: {hostname}\n")
    f.write(f"Ports scanned: {start_port}–{end_port}\n\n")
    if results:
        for line in results:
            f.write(line + "\n")
    else:
        f.write("No open ports found.\n")
    f.write(f"\nScan completed in {duration:.2f} seconds.\n")

print(f"📁 Results saved to: {filename}")
