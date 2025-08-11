from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/get_ip', methods=['POST'])
def get_ip():
    data = request.get_json()
    domain = data.get('domain')
    port = data.get('port')

    try:
        ip = socket.gethostbyname(domain)
        if port:
            return jsonify({'ip': f"{ip}:{port}"})
        else:
            return jsonify({'ip': ip})
    except socket.gaierror:
        return jsonify({'error': 'Invalid domain'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Domain to IP:Port Converter</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(to right, #8360c3, #2ebf91);
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }

    .container {
      background-color: #fff;
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
      text-align: center;
      width: 90%;
      max-width: 450px;
      transition: 0.3s ease;
    }

    h2 {
      margin-bottom: 20px;
      color: #333;
    }

    input {
      width: 100%;
      padding: 12px;
      border: 2px solid #ddd;
      border-radius: 10px;
      margin-bottom: 15px;
      font-size: 16px;
    }

    button {
      padding: 12px 20px;
      margin: 5px;
      border: none;
      border-radius: 10px;
      font-size: 16px;
      cursor: pointer;
      transition: 0.2s ease;
    }

    .get-btn {
      background-color: #2ebf91;
      color: white;
    }

    .get-btn:hover {
      background-color: #24a076;
    }

    .copy-btn {
      background-color: #ddd;
    }

    .copy-btn:hover {
      background-color: #bbb;
    }

    #ipResult {
      margin-top: 15px;
      font-size: 18px;
      font-weight: bold;
      color: #444;
      word-break: break-word;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>🌐 Domain to IP:Port</h2>
    <input type="text" id="domain" placeholder="e.g. your link:21557" />
    <button class="get-btn" onclick="getIP()">Get IP</button>
    <div id="ipResult"></div>
    <button class="copy-btn" id="copyBtn" style="display: none;" onclick="copyIP()">Copy</button>
  </div>

  <script>
    async function getIP() {
      const input = document.getElementById("domain").value.trim();
      const result = document.getElementById("ipResult");
      const copyBtn = document.getElementById("copyBtn");

      if (!input.includes(".")) {
        result.textContent = "Please enter a valid domain.";
        copyBtn.style.display = "none";
        return;
      }

      result.textContent = "Fetching...";
      copyBtn.style.display = "none";

      let domain = input;
      let port = "";

      if (input.includes(":")) {
        const parts = input.split(":");
        domain = parts[0];
        port = parts[1];
      }

      try {
        const response = await fetch(`https://dns.google/resolve?name=${domain}&type=A`);
        const data = await response.json();

        if (data.Answer && data.Answer.length > 0) {
          const ip = data.Answer[0].data;
          const full = port ? `${ip}:${port}` : ip;
          result.textContent = `Resolved: ${full}`;
          copyBtn.setAttribute("data-ip", full);
          copyBtn.style.display = "inline-block";
        } else {
          result.textContent = "No IP found or invalid domain.";
        }
      } catch (error) {
        result.textContent = "Error fetching IP.";
      }
    }

    function copyIP() {
      const ip = document.getElementById("copyBtn").getAttribute("data-ip");
      navigator.clipboard.writeText(ip).then(() => {
        alert("Copied: " + ip);
      }).catch(() => {
        alert("Failed to copy.");
      });
    }
  </script>
</body>
</html>