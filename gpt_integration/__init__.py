import requests
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
                "You are an expert in cybersecurity. You are analyzing a news article related to cybersecurity. "
                "I want you to summarize it and reformulate the news like a LinkedIn post. "
                "The user will provide you with the HTML content of the news and the source link. Be constructive and smart. "
                "The message should be in French, well-formulated, and precise for other cybersecurity experts. "
                "Make sure to include a suitable title that corresponds to the message."
            )
        },
        {
            "role": "user",
            "content": (
                f"Voici la news: {visible_text}\n\n"
                f"Source: {news_url}"
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
        return response_data['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erreur lors de la requête à l'API ChatGPT : {e}")
        return None
