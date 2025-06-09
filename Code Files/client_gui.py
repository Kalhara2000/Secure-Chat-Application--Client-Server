import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import ssl
import threading
import logging

# Center any Tkinter window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Custom Username Dialog
class UsernameDialog(tk.Toplevel):
    def __init__(self, parent, width=40):
        super().__init__(parent)
        self.title("Username")
        self.username = None

        dialog_width = 350
        dialog_height = 120
        center_window(self, dialog_width, dialog_height)

        tk.Label(self, text="Enter your username:").pack(pady=10)
        self.entry = tk.Entry(self, width=width)
        self.entry.pack(pady=5)
        self.entry.focus()

        tk.Button(self, text="OK", command=self.submit).pack(pady=5)
        self.bind("<Return>", lambda event: self.submit())

        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def submit(self):
        self.username = self.entry.get().strip() or "Anonymous"
        self.destroy()

# Logging handler for chat log
class LogHandler(logging.Handler):
    def __init__(self, chat_client):
        super().__init__()
        self.chat_client = chat_client

    def emit(self, record):
        msg = self.format(record)
        self.chat_client.display_message(msg)

# Main Secure Chat Client
class SecureChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure LAN Chat Client")

        window_width = 750
        window_height = 500
        center_window(self.root, window_width, window_height)

        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        try:
            self.context.load_verify_locations('certs/server.crt')
        except Exception as e:
            messagebox.showerror("Certificate Error", f"Could not load certificate: {e}")
            root.destroy()
            return

        self.connected = False
        self.client_socket = None

        dialog = UsernameDialog(self.root, width=40)
        self.username = dialog.username or "Anonymous"

        self.setup_ui()
        self.setup_logging()

    def setup_ui(self):
        top = tk.Frame(self.root)
        top.pack(pady=10)

        tk.Label(top, text="Server IP:").pack(side=tk.LEFT)
        self.ip_entry = tk.Entry(top, width=15)
        self.ip_entry.insert(0, "localhost")
        self.ip_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(top, text="Port:").pack(side=tk.LEFT)
        self.port_entry = tk.Entry(top, width=7)
        self.port_entry.insert(0, "12345")
        self.port_entry.pack(side=tk.LEFT, padx=5)

        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side=tk.LEFT, padx=5)

        self.chat_text = scrolledtext.ScrolledText(self.root, height=20, width=80, state='disabled')
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        bottom = tk.Frame(self.root)
        bottom.pack(fill=tk.X, padx=10, pady=5)

        self.msg_entry = tk.Entry(bottom)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(bottom, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT, padx=5)

        self.status_var = tk.StringVar(value="Not connected")
        tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)

        self.msg_entry.config(state='disabled')

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[LogHandler(self)]
        )

    def toggle_connection(self):
        if not self.connected:
            self.connect_to_server()
        else:
            self.disconnect()

    def connect_to_server(self):
        try:
            host = self.ip_entry.get().strip()
            port = int(self.port_entry.get())

            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket = self.context.wrap_socket(raw_sock, server_hostname=host)
            self.client_socket.settimeout(1.0)  # Set timeout to allow safe exit

            self.client_socket.connect((host, port))
            self.connected = True
            self.status_var.set(f"Connected to {host}:{port}")
            self.connect_btn.config(text="Disconnect")
            self.msg_entry.config(state='normal')

            self.safe_send(f"username:{self.username} joined..!")

            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()

        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            self.client_socket = None
            self.connected = False

    def disconnect(self):
        if not self.connected:
            return
        self.connected = False  # Stop recv loop
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None

        self.connect_btn.config(text="Connect")
        self.status_var.set("Disconnected")
        self.msg_entry.config(state='disabled')
        logging.info("Disconnected")

    def safe_send(self, message):
        if self.connected and self.client_socket:
            try:
                if not message.endswith('\n'):
                    message += '\n'
                self.client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                logging.error(f"Send failed: {e}")
                self.disconnect()

    def send_message(self, event=None):
        if not self.connected:
            return
        msg = self.msg_entry.get().strip()
        if msg:
            full_msg = f"{self.username}: {msg}"
            self.display_message(f"You: {msg}")
            self.safe_send(full_msg)
            self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        buffer = ""
        try:
            while self.connected:
                try:
                    data = self.client_socket.recv(1024)
                    if not data:
                        break
                    buffer += data.decode('utf-8')
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        msg = line.strip()
                        if not msg.startswith(f"{self.username}:"):
                            self.display_message(msg)
                except socket.timeout:
                    continue  # Timeout allows checking self.connected
                except OSError:
                    break
        except Exception as e:
            logging.error(f"Connection lost: {e}")
        finally:
            self.root.after(0, self.disconnect)

    def display_message(self, msg):
        self.chat_text.config(state='normal')
        self.chat_text.insert(tk.END, msg + "\n")
        self.chat_text.config(state='disabled')
        self.chat_text.see(tk.END)

    def on_closing(self):
        self.disconnect()
        self.root.destroy()

# Entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = SecureChatClient(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
