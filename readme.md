🔍 Ultra Port Scanner (Python)

An advanced, multithreaded port scanner built with Python. Scans a user-defined port range, detects open ports, grabs service banners, and gives human-readable service hints

📦 Features

- 🌐 Accepts domain or IP address as input
- 🔁 Reverse DNS lookup
- 🔍 Custom port range scan
- ⚡ Multithreaded scanning for speed
- ✅ Identifies open ports only
- 📄 Grabs service banners from ports
- 🧠 Explains common banners (e.g., Apache, OpenSSH, MySQL)
- 💾 Saves results to a file
- ⏱️ Displays scan duration
- ❌ Informs if no open ports are found

🛠️ Requirements

- Python 3.x  
No third-party modules needed — only built-in libraries used:
- `socket`
- `threading`
- `datetime`

🚀 How to Run

1. Clone or download this repo
2. Open terminal in the project folder
3. Run:

```bash
python scanner.py
