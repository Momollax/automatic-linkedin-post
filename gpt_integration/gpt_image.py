import requests
import time
import uuid
import os

def ask_gpt_prompt_image(prompt, openai_api_key):
    print("[+] Génération du prompt pour l'image")
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    messages = [
        {
            "role": "system",
            "content": (
               "Je vais te fournir un texte. Analyse ce texte pour identifier les entités importantes comme "
               "les pays, les entreprises, les personnes, etc. Ensuite, crée une description détaillée d'une "
               "image qui correspondrait au contenu du texte, en prenant en compte les entités extraites et le"
               "contexte global du texte. La description de l'image doit inclure des éléments visuels clés qui "
               "reflètent les informations essentielles du texte comme les drapeau des pays, les entreprise "
               "la cible des attaquant, les logiciels"
               "la formulation doit etre pour dale-3, donc relativement courte. ecrit juste le prompt pour dale-3"
               )
        },
        {
            "role": "user",
            "content": (
                f"Voici le text : {prompt}"
            )
        }
    ]

    payload = {
        "model": "gpt-4o-mini",
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        chatgpt_message = response_data['choices'][0]['message']['content']
        return chatgpt_message

    except Exception as e:
        print(f"Erreur lors de la requête à l'API ChatGPT : {e}")
        return None
    
def generer_image_via_dalle(prompt, openai_api_key):
    print("[+] Génération de l'image")
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model":"dall-e-3",
        "prompt": prompt,
        "n": 1,  # Nombre d'images à générer
        "size": "1024x1024"  # Taille de l'image
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Gère les erreurs HTTP
        response_data = response.json()
        image_url = response_data['data'][0]['url'] if 'data' in response_data and len(response_data['data']) > 0 else None
        if image_url:
            print(f"[+] Image générée avec succès!")
        else:
            print("[-] Aucune URL d'image retournée.")
        return image_url

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête POST : {e}")
        return None

def sauvegarder_image(image_url, nom_fichier):
    if not image_url:
        print("URL d'image non valide. Aucune image ne sera téléchargée.")
        return

    try:
        # Crée le répertoire s'il n'existe pas
        os.makedirs(os.path.dirname(nom_fichier), exist_ok=True)
        
        image_response = requests.get(image_url)
        image_response.raise_for_status()  # Gère les erreurs HTTP
        with open(nom_fichier, 'wb') as file:
            file.write(image_response.content)
        print(f"[+] Image enregistrée sous le nom : {nom_fichier}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")


def ask_gpt_image(prompt, openai_api_key):
    prompt = ask_gpt_prompt_image(prompt, openai_api_key)
    image_url = generer_image_via_dalle(prompt, openai_api_key)
    
    if image_url:
        nom_fichier = f"./images/{uuid.uuid4().hex}.png"
        sauvegarder_image(image_url, nom_fichier)
        return nom_fichier