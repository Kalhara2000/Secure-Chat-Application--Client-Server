import socket
import ssl
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

clients = []
server_socket = None
server_thread_running = False

def handle_client(conn, addr, text_area):
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode().strip()
                log_entry = f"{addr}: {message}"
                text_area.insert(tk.END, log_entry + "\n")
                text_area.see(tk.END)
                for c in clients:
                    if c != conn:
                        c.sendall((message + "\n").encode())
            except:
                break
        if conn in clients:
            clients.remove(conn)

def start_server(port_entry, text_area, start_btn, stop_btn):
    global server_socket, server_thread_running

    port = int(port_entry.get())
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")

    def server_thread():
        global server_socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', port))
            s.listen()
            text_area.insert(tk.END, f"🚀 Server running on port {port}...\n")
            text_area.see(tk.END)
            with context.wrap_socket(s, server_side=True) as ssock:
                server_socket = ssock
                while server_thread_running:
                    try:
                        ssock.settimeout(1.0)
                        conn, addr = ssock.accept()
                        clients.append(conn)
                        threading.Thread(target=handle_client, args=(conn, addr, text_area), daemon=True).start()
                    except socket.timeout:
                        continue
                    except Exception as e:
                        break

    server_thread_running = True
    threading.Thread(target=server_thread, daemon=True).start()
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)

def stop_server(text_area, start_btn, stop_btn):
    global server_socket, server_thread_running

    server_thread_running = False

    # Close all client connections
    for c in clients:
        try:
            c.shutdown(socket.SHUT_RDWR)
            c.close()
        except:
            pass
    clients.clear()

    # Close server socket
    if server_socket:
        try:
            server_socket.close()
        except:
            pass
        server_socket = None

    text_area.insert(tk.END, "🛑 Server stopped.\n")
    text_area.see(tk.END)

    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)

def gui():
    window = tk.Tk()
    window.title("🔐 SSL Chat Server")

    tk.Label(window, text="Port:").pack(pady=(10, 0))
    port_entry = tk.Entry(window)
    port_entry.pack()
    port_entry.insert(0, "12345")

    chat_log = ScrolledText(window, state='normal', width=60, height=25)
    chat_log.pack(padx=10, pady=10)

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=(0, 10))

    start_btn = tk.Button(btn_frame, text="Start Server")
    stop_btn = tk.Button(btn_frame, text="Stop Server")

    start_btn.config(command=lambda: start_server(port_entry, chat_log, start_btn, stop_btn))
    stop_btn.config(command=lambda: stop_server(chat_log, start_btn, stop_btn), state=tk.DISABLED)

    start_btn.pack(side=tk.LEFT, padx=5)
    stop_btn.pack(side=tk.LEFT, padx=5)

    window.protocol("WM_DELETE_WINDOW", lambda: (stop_server(chat_log, start_btn, stop_btn), window.destroy()))
    window.mainloop()

if __name__ == "__main__":
    gui()
