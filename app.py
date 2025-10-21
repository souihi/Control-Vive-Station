import asyncio
import json
from flask import Flask, render_template, request, redirect, url_for
from bleak import BleakClient

# Initialisation de l'application Flask
app = Flask(__name__)

# Fichier pour stocker les adresses MAC
STATIONS_FILE = 'stations.json'

# UUID et commandes Bluetooth
POWER_CHARACTERISTIC_UUID = "00001525-1212-efde-1523-785feabcd124"
CMD_ON = b'\x01'
CMD_OFF = b'\x00'


# --- Fonctions pour gérer le fichier JSON ---

def load_stations():
    """Charge la liste des adresses MAC depuis le fichier JSON."""
    try:
        with open(STATIONS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si le fichier n'existe pas ou est vide/corrompu, on retourne une liste vide.
        return []


def save_stations(stations):
    """Sauvegarde la liste des adresses MAC dans le fichier JSON."""
    with open(STATIONS_FILE, 'w') as f:
        json.dump(stations, f, indent=4)


# --- Logique Bluetooth (notre fonction de contrôle) ---

async def control_station(address: str, command: bytes):
    """Se connecte à une station et envoie une commande d'alimentation."""
    action_str = "ON" if command == CMD_ON else "OFF"
    print(f"Tentative de connexion à {address} pour l'action {action_str}...")
    try:
        async with BleakClient(address, timeout=10.0) as client:
            if client.is_connected:
                await client.write_gatt_char(POWER_CHARACTERISTIC_UUID, command)
                print(f"✅ Commande {action_str} envoyée à {address}.")
                return True
    except Exception as e:
        print(f"❌ Erreur avec {address}: {e}")
    return False


# --- Les "Routes" de notre API / Site Web ---

@app.route('/')
def index():
    """Affiche la page principale."""
    stations = load_stations()
    return render_template('index.html', stations=stations)


@app.route('/add', methods=['POST'])
def add_station():
    """Ajoute une nouvelle adresse MAC à la liste."""
    mac = request.form.get('mac')
    if mac:
        stations = load_stations()
        if mac not in stations:
            stations.append(mac)
            save_stations(stations)
    return redirect(url_for('index'))


@app.route('/remove', methods=['POST'])
def remove_station():
    """Supprime une adresse MAC de la liste."""
    mac = request.form.get('mac')
    if mac:
        stations = load_stations()
        if mac in stations:
            stations.remove(mac)
            save_stations(stations)
    return redirect(url_for('index'))


@app.route('/control', methods=['POST'])
def control_all():
    """Allume ou éteint toutes les stations."""
    action = request.form.get('action')
    command = CMD_ON if action == 'on' else CMD_OFF

    stations = load_stations()

    # Exécute les commandes Bluetooth en mode séquentiel
    async def run_control_sequentially():
        print("Lancement du contrôle en mode séquentiel pour éviter la surcharge...")
        for mac in stations:
            await control_station(mac, command)
            print("--- Pause de 2 secondes ---")
            await asyncio.sleep(2)  # Pause pour laisser le temps au contrôleur de "respirer"

    asyncio.run(run_control_sequentially())

    return redirect(url_for('index'))


# --- Lancement de l'application ---

if __name__ == '__main__':
    # host='0.0.0.0' rend l'application accessible depuis d'autres appareils sur le réseau
    app.run(host='0.0.0.0', port=5000, debug=True)