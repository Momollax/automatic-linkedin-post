import requests
import time
from bs4 import BeautifulSoup

def ask_gpt(news_url, openai_api_key):
    response = requests.get(news_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        visible_text = soup.get_text(separator='\n', strip=True)
    else:
        print(f"Erreur lors de la requête GET : {response.status_code}")
        return None

    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    messages = [
        {
            "role": "system",
            "content": (
                "Tu es un expert en cybersécurité, et ta tâche est d'analyser un article d'actualité pour déterminer s'il est suffisamment intéressant pour être partagé avec une audience de professionnels de la cybersécurité sur LinkedIn. "
                "L'article doit répondre à plusieurs critères : "
                "1. Représente-t-il une menace ou un développement significatif dans le domaine de la cybersécurité ? "
                "2. Est-il pertinent pour les experts en cybersécurité, avec des informations techniques ou stratégiques utiles ? "
                "3. L'article provient-il d'une source crédible et bien établie dans le domaine ? "
                "4. La nouvelle est-elle récente et a-t-elle un impact potentiel sur les entreprises ou les pratiques en cybersécurité ? "
                "Si l'article ne remplit pas ces critères, conclut simplement que 'Cet article n'est pas suffisamment intéressant pour être publié'. "
                "Sinon, rédige un post LinkedIn professionnel et engageant qui inclut : "
                "1. Un titre percutant et informatif. "
                "2. Un résumé concis qui met en avant les éléments clés de l'article, en évitant les détails superflus. "
                "3. Des hashtags pertinents pour maximiser la portée auprès de l'audience cible. "
                "4. ajoute la source url. "
                "N'inclut pas d'évaluation ou de commentaire sur la décision de publier. Limite ta réponse à ce qui doit être publié sur LinkedIn, en français."
                "Voici un exemple de post linkedin:"
                "🚨 ALERTE CYBERSÉCURITÉ : VULNÉRABILITÉ CRITIQUE DÉCOUVERTE DANS LOG4J 🚨"
                ""
                "Une nouvelle faille de sécurité, surnommée Log4Shell, a été découverte dans la bibliothèque de journalisation Log4j, largement utilisée dans des milliers d'applications et services à travers le monde. Cette vulnérabilité critique (CVE-2021-44228) permettrait à des attaquants de prendre le contrôle de serveurs sans authentification, simplement en envoyant des requêtes malveillantes."
                ""
                "🎯 Pourquoi est-ce si grave ?"
                "Log4j est un composant essentiel dans de nombreuses infrastructures IT, ce qui signifie que cette faille touche un grand nombre d’organisations, grandes ou petites. Les cybercriminels exploitent déjà cette vulnérabilité pour mener des attaques massives, incluant le déploiement de ransomwares."
                ""
                "🔧 Que faire ?"
                ""
                "Patch immédiat : Assurez-vous que vos systèmes utilisent la version la plus récente de Log4j, où la vulnérabilité est corrigée."
                "Surveillance accrue : Renforcez la surveillance de votre trafic réseau pour détecter toute activité suspecte."
                "Communication : Informez immédiatement vos équipes IT et de sécurité pour qu’elles prennent les mesures nécessaires."
                "C'est un rappel brutal de l'importance de maintenir une vigilance constante en matière de sécurité. Nous devons rester proactifs pour protéger nos systèmes contre de telles menaces."

            )
        },
        {
            "role": "user",
            "content": (
                f"Voici l'article : {visible_text}\n\n"
                f"Source : {news_url}"
            )
        }
    ]

    payload = {
        "model": "gpt-4",
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        chatgpt_message = response_data['choices'][0]['message']['content']
        time.sleep(20)
        if "Cet article n'est pas suffisamment intéressant pour être publié" in chatgpt_message:
            print("La nouvelle n'est pas jugée intéressante pour être publiée.")
            return None
        else:
            return chatgpt_message

    except Exception as e:
        print(f"Erreur lors de la requête à l'API ChatGPT : {e}")
        return None