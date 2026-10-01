import os
import sys
import subprocess
import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
ASSETS_DIR = os.path.join(WEB_DIR, "assets")

def check_and_generate_assets():
    required_assets = [
        "p1_i_campo_instantaneo.png",
        "p1_i_trayectorias.png",
        "p1_i_trayectoria_vs_linea.png",
        "p1_ii_betas.png",
        "p1_iii_omegas.png",
        "p2_ref.png",
        "p2_base_loss.png",
        "p3_burgers_fit.png",
    ]
    missing = [a for a in required_assets if not os.path.exists(os.path.join(ASSETS_DIR, a))]
    
    if missing or "--regenerate" in sys.argv:
        print("Generando activos gráficos y animaciones...")
        export_script = os.path.join(BASE_DIR, "export_assets.py")
        res = subprocess.run([sys.executable, export_script], check=True)
        if res.returncode != 0:
            print("Error al generar activos.")
            sys.exit(1)
    else:
        print("Todos los activos gráficos están listos.")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

def start_server():
    global PORT
    check_and_generate_assets()
    
    while PORT < 8020:
        try:
            with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
                url = f"http://localhost:{PORT}/web/index.html"
                print(f"\n========================================================")
                print(f" Servidor Web Activo: {url}")
                print(f" Servidor ligero de bajo consumo de memoria RAM")
                print(f" Presiona Ctrl+C para detener el servidor")
                print(f"========================================================\n")
                
                # Open web browser after 0.8s
                threading.Timer(0.8, lambda: webbrowser.open(url)).start()
                httpd.serve_forever()
                break
        except OSError:
            PORT += 1

if __name__ == "__main__":
    start_server()
