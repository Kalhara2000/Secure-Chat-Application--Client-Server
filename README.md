<h1>🔐 Encrypted Local Communication System</h1>
<p>A lightweight, secure, and encrypted chat system built using <strong>Python</strong>, <strong>SSL/TLS encryption</strong>, <strong>multithreading</strong>, and a GUI monitor. It enables secure messaging over local networks without internet dependency.</p>

<blockquote>✨ Developed by <strong>Thamindu Kalhara</strong></blockquote>

<hr/>

<h2>🚀 Key Features</h2>
<ul>
  <li>✅ End-to-End SSL Encryption</li>
  <li>✅ Real-Time Messaging</li>
  <li>✅ Multi-client Communication</li>
  <li>✅ GUI-Based Server Monitoring</li>
  <li>✅ Lightweight & Local Network-based</li>
</ul>

<h2>📁 Folder Structure</h2>
<pre><code>
SecureCom/
├── certs/
│   ├── server.crt
│   └── server.key
├── dist/
│   ├── SecureServer.exe
│   └── SecureClient.exe
├── README.html
</code></pre>

<hr/>

<h2>🖥️ Server Setup</h2>

<h3>1️⃣ Clone the Repo</h3>
<pre><code>https://github.com/Kalhara2000/Secure-Chat-Application--Client-Server.git
cd Secure-Chat-Application--Client-Server</code></pre>

<h3>2️⃣ Generate SSL Certificate (if missing)</h3>
<pre><code>mkdir certs
openssl req -new -x509 -days 365 -nodes -out certs/server.crt -keyout certs/server.key</code></pre>

<h3>3️⃣ Run the Server</h3>
<pre><code>python secure_server.py</code></pre>
<p>🪟 A Tkinter GUI will open. Input a port number (e.g., <code>12345</code>) and click "Start Server".</p>

<hr/>

<h2>👨‍💻 Client Setup</h2>

<h3>1️⃣ Copy the <code>secure_client.py</code> file to the client machine</h3>

<h3>2️⃣ Make sure the <code>server.crt</code> file is available on the client</h3>
<p>This is used to verify the server's identity.</p>

<h3>3️⃣ Run the Client</h3>
<pre><code>python secure_client.py</code></pre>

<h3>4️⃣ Input Required Details</h3>
<ul>
  <li>Server IP (use the server’s LAN IP, e.g., <code>192.168.1.10</code>)</li>
  <li>Port number (same as server, e.g., <code>12345</code>)</li>
  <li>Your name (used in chat)</li>
</ul>

<p>✅ The client connects to the server using <strong>SSL encryption</strong>, enabling real-time secure messaging between all connected users.</p>

<hr/>

<h2>🖥️ Server Setup (EXE)</h2>

<h3>1️⃣ Requirements</h3>
<ul>
  <li>Windows OS</li>
  <li>Python NOT required to be installed</li>
  <li>EXE built using PyInstaller</li>
</ul>

<h3>2️⃣ Run the Server</h3>
<ol>
  <li>Navigate to the <code>dist</code> folder.</li>
  <li>Double-click <code>SecureServer.exe</code>.</li>
  <li>Allow access if Windows Firewall prompts.</li>
</ol>

<h3>3️⃣ Start Server</h3>
<p>A GUI window will appear:</p>
<ul>
  <li>Enter a port number (e.g., <code>12345</code>).</li>
  <li>Click "Start Server".</li>
</ul>

<p>💡 Keep the <code>certs</code> folder in the same directory as the EXE file.</p>

<hr/>

<h2>👨‍💻 Client Setup (EXE)</h2>

<h3>1️⃣ Run the Client</h3>
<ol>
  <li>Copy <code>SecureClient.exe</code> and <code>server.crt</code> to the client PC.</li>
  <li>Double-click <code>SecureClient.exe</code>.</li>
</ol>

<h3>2️⃣ Connect to Server</h3>
<p>Input the following:</p>
<ul>
  <li>🔢 Server IP (e.g., <code>192.168.1.10</code>)</li>
  <li>📍 Port Number (must match the server, e.g., <code>12345</code>)</li>
  <li>👤 Your Name (for chat identification)</li>
</ul>

<p>✅ You are now securely connected!</p>

<hr/>

<h2>🧰 Tech Stack</h2>
<ul>
  <li>🐍 Python</li>
  <li><code>socket</code> - Network communication</li>
  <li><code>ssl</code> - SSL/TLS encryption</li>
  <li><code>threading</code> - Multi-client support</li>
  <li><code>tkinter</code> - GUI (server)</li>
  <li><code>ScrolledText</code> - Message logs</li>
</ul>

<hr/>

<h2>🔮 Future Upgrades</h2>
<ul>
  <li>🔐 User login with authentication</li>
  <li>📂 Secure file transfer</li>
  <li>📱 Flutter-based mobile client</li>
  <li>🎙 Voice communication via VoIP</li>
  <li>🛰️ Mesh Wi-Fi deployment support</li>
</ul>

<hr/>

<h2>📬 Contact & Credits</h2>
<p>Created by <strong>Thamindu Kalhara</strong></p>
<p>
LinkedIn: <a href="https://www.linkedin.com/in/ktdt-kalhara/">Thamindu Kalhara</a><br/>
GitHub: <a href="https://github.com/Kalhara2000">Kalhara2000</a>
</p>

<p>#Python #SSL #SecureCommunication #LANChat #Tkinter #Networking #LocalNetwork #CyberSecurity #SocketProgramming</p>
