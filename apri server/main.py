from mcstatus import JavaServer
import requests
from dotenv import load_dotenv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

server_ip = "localhost"  # metti qui l'IP o dominio del server

def accendi():
    requests.post(os.getenv("DISCORD_WEBHOOK"), json={"content": f"Apertura server da {os.getenv("USER")}"})
    os.system("run.bat")

try:
    server = JavaServer.lookup(server_ip)
    status = server.status()
    print(f"✅ Server online!")
    print(f"Giocatori online: {status.players.online}")
except Exception as e:
    print(f"❌ Server offline o non raggiungibile: {e}")
    accendi()