from datetime import datetime
import os
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MESSAGE_UTILISATEUR = os.environ.get("USER_MESSAGE", "Rapport standard")


def generer_rapport():
    date_du_jour = datetime.now().strftime("%d/%m/%Y")
    longueur = len(MESSAGE_UTILISATEUR)

    description_elements = [
        f"• Date du rapport : {date_du_jour}",
        f"• Message reçu : « {MESSAGE_UTILISATEUR} »",
        f"• Caractères analysés : {longueur}",
        f"• Statut : Généré via GitHub Actions 100% gratuit.",
    ]

    return (
        f"📊 *Rapport automatique (GitHub)*\n\n"
        + "\n".join(description_elements)
    )


def envoyer():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": generer_rapport(),
        "parse_mode": "Markdown",
    }
    requests.post(url, json=payload)


if __name__ == "__main__":
    envoyer()
