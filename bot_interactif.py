from datetime import datetime
import time
import requests

# Configuration
TOKEN = "8618917135:AAGBH_JvXs8KedQJfTJb3x93xMpUM0tH-yE"
URL_BASE = f"https://api.telegram.org/bot{TOKEN}"


def obtenir_mises_a_jour(offset=None):
    """Récupère les nouveaux messages envoyés au bot"""
    url = f"{URL_BASE}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()


def envoyer_message(chat_id, texte):
    """Envoie un message sur Telegram"""
    url = f"{URL_BASE}/sendMessage"
    payload = {"chat_id": chat_id, "text": texte, "parse_mode": "Markdown"}
    requests.post(url, json=payload)


def generer_rapport_sur_mesure(texte_utilisateur):
    """Génère le rapport en fonction de ce qu'a écrit l'utilisateur"""
    date_du_jour = datetime.now().strftime("%d/%m/%Y")
    longueur_message = len(texte_utilisateur)
    mots_cles = (
        "Urgent"
        if "urgent" in texte_utilisateur.lower()
        else "Standard"
    )

    # Affichage de tous les éléments du rapport (conformément à vos consignes)
    description_elements = [
        f"• Date du rapport : {date_du_jour}",
        f"• Message analysé : « {texte_utilisateur} »",
        f"• Nombre de caractères : {longueur_message}",
        f"• Niveau de priorité : {mots_cles}",
        f"• Statut du traitement : Rapport généré avec succès.",
    ]

    rapport_texte = (
        f"📊 *Rapport d'analyse personnalisé*\n\n"
        + "\n".join(description_elements)
    )
    return rapport_texte


def lancer_bot():
    print(
        "Bot démarré et à l'écoute des messages... (Appuyez sur Ctrl+C pour arrêter)"
    )
    dernier_id_message = None

    while True:
        try:
            mises_a_jour = obtenir_mises_a_jour(dernier_id_message)

            if mises_a_jour.get("ok") and mises_a_jour.get("result"):
                for update in mises_a_jour["result"]:
                    dernier_id_message = update["update_id"] + 1

                    # Vérifie si le message contient du texte
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        texte_recu = update["message"]["text"]

                        print(f"Message reçu de {chat_id} : {texte_recu}")

                        # Génération du rapport basé sur le message
                        rapport = generer_rapport_sur_mesure(texte_recu)

                        # Envoi de la réponse à l'utilisateur
                        envoyer_message(chat_id, rapport)

        except Exception as e:
            print(f"Erreur : {e}")
            time.sleep(3)


if __name__ == "__main__":
    lancer_bot()