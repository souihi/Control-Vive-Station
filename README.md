# Contrôleur de Stations de Base HTC Vive 🕹️

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Bluetooth](https://img.shields.io/badge/Bluetooth-0082FC?style=for-the-badge&logo=bluetooth&logoColor=white)

Une application web simple, hébergée sur un Raspberry Pi, pour allumer et éteindre à distance vos stations de base HTC Vive 1.0 ou 2.0 via Bluetooth Low Energy (BLE).

Fini le bruit constant ou le besoin de débrancher manuellement vos stations ! Gérez tout depuis une interface web accessible sur votre téléphone ou votre PC.



## ## Fonctionnalités ✨

* **Interface Web Simple :** Accédez à un panneau de contrôle épuré depuis n'importe quel appareil sur votre réseau local.
* **Contrôle Global :** Allumez ou éteignez toutes vos stations enregistrées en un seul clic.
* **Gestion des Stations :** Ajoutez ou supprimez facilement des stations de base en utilisant leur adresse MAC.
* **Léger et Efficace :** Conçu pour tourner 24/7 sur un Raspberry Pi sans consommer beaucoup de ressources.

---

## ## Prérequis Matériels  हार्डवेयर

* Un **Raspberry Pi** (modèle 3, 4, ou 5 recommandé) avec connectivité Bluetooth.
* Une ou plusieurs **stations de base HTC Vive** (version 1.0 ou 2.0).
* Une alimentation pour le Raspberry Pi.

---

## ## Guide d'Installation (De A à Z) 🚀

Suivez ces étapes pour installer et configurer l'application sur votre Raspberry Pi.

### ### Étape 1 : Préparation du Système

1.  **Mettez à jour votre système** pour vous assurer que tout est à jour :
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2.  **Installez les paquets nécessaires** (Git pour cloner le projet et `venv` pour l'environnement Python) :
    ```bash
    sudo apt install git python3-venv -y
    ```

3.  **Vérifiez que le Bluetooth est activé.** Normalement, il l'est par défaut. Vous pouvez vérifier son état avec :
    ```bash
    sudo systemctl status bluetooth
    ```
    S'il n'est pas actif, activez-le avec `sudo systemctl enable --now bluetooth`.

### ### Étape 2 : Cloner et Préparer l'Application

1.  **Clonez ce dépôt** dans le dossier de votre choix (par exemple, le dossier `Documents`) :
    ```bash
    cd ~/Documents
    git clone [https://github.com/souihi/Control-Vive-Station-CaM-X-IA-.git](https://github.com/souihi/Control-Vive-Station-CaM-X-IA-.git)
    ```

2.  **Accédez au dossier du projet :**
    ```bash
    cd Control-Vive-Station-CaM-X-IA-
    ```

3.  **Créez un environnement virtuel Python :**
    ```bash
    python3 -m venv vive_env
    ```

4.  **Activez l'environnement.** La commande dépend de votre shell :
    * Pour le shell par défaut (**bash**) :
        ```bash
        source vive_env/bin/activate
        ```
    * Pour le shell **Fish** :
        ```fish
        source vive_env/bin/activate.fish
        ```
    Votre invite de commande devrait maintenant commencer par `(vive_env)`.

5.  **Installez les dépendances Python :**
    ```bash
    pip install -r requirements.txt
    ```

### ### Étape 3 : Configuration Initiale

1.  **Trouvez les adresses MAC de vos stations.** C'est l'étape la plus importante. Avec l'environnement activé, lancez un scan Bluetooth :
    ```bash
    sudo bluetoothctl scan on
    ```
    Laissez tourner le scan. Vos stations de base devraient apparaître avec un nom commençant par `LHB-`. Notez leurs adresses MAC (format `XX:XX:XX:XX:XX:XX`). Une fois terminé, quittez le scan avec `Ctrl+C`.

2.  **Créez le fichier de configuration des stations.** L'application stocke les adresses MAC dans un fichier `stations.json`. Vous pouvez le créer vide, puis ajouter les stations via l'interface web.
    ```bash
    touch stations.json
    ```

---

## ## Utilisation de l'Application 💡

1.  **Lancez le serveur web.** Assurez-vous que votre environnement virtuel est toujours activé, puis lancez :
    ```bash
    python3 app.py
    ```
    Le serveur va démarrer. Ne fermez pas ce terminal.

2.  **Trouvez l'adresse IP de votre Raspberry Pi.** Dans un *autre* terminal, tapez :
    ```bash
    hostname -I
    ```
    Cela vous donnera une adresse comme `192.168.1.XX`.

3.  **Accédez à l'interface.** Ouvrez un navigateur web sur votre téléphone ou PC et allez à l'adresse :
    ```
    http://<VOTRE_IP_RASPBERRY_PI>:5000
    ```

4.  **Gérez vos stations :**
    * Utilisez le formulaire "Ajouter une Station" pour entrer les adresses MAC que vous avez notées.
    * Une fois ajoutées, utilisez les boutons "Tout Allumer" et "Tout Éteindre" pour les contrôler.

---

## ## Dépannage (Troubleshooting)

* **Erreur `ModuleNotFoundError`**: Assurez-vous que votre environnement virtuel est bien activé avant de lancer `python3 app.py`. Votre terminal doit afficher `(vive_env)` au début de la ligne.
* **Les stations ne réagissent pas**:
    * Vérifiez que les adresses MAC dans `stations.json` sont correctes.
    * Assurez-vous que le Raspberry Pi est à une distance raisonnable des stations (le signal Bluetooth a une portée limitée).
    * Redémarrez le Raspberry Pi.

---

## ## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une "issue" pour signaler un bug ou proposer une nouvelle fonctionnalité.

## ## Licence

Ce projet est distribué sous la licence MIT. Voir le fichier `LICENSE` pour plus de détails.
