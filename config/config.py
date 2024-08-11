import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'WEBHOOK_URL': os.getenv('WEBHOOK_URL'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'LINKEDIN_CLIENT_ID': os.getenv('LINKEDIN_CLIENT_ID'),
        'LINKEDIN_CLIENT_SECRET': os.getenv('LINKEDIN_CLIENT_SECRET'),
        'REDIRECT_URI': os.getenv('REDIRECT_URI'),
        'ORG_NAME': os.getenv('ORG_NAME'),
        'FLUX': [
            {'url': 'https://www.infosecurity-magazine.com/rss/news/', 'title': 'Nouveau flux RSS depuis InfoSecurity Magazine', 'refresh_rate': 60},
            {'url': 'https://www.darknet.org.uk/feed/', 'title': 'Nouveau flux RSS depuis darknet.org.uk', 'refresh_rate': 60},
            {'url': 'https://news.ycombinator.com/rss', 'title': 'Nouveau flux RSS depuis Hacker News', 'refresh_rate': 60},
            {'url': 'https://www.zataz.com/feed/', 'title': 'Nouveau flux RSS depuis Zataz', 'refresh_rate': 60},
            {'url': 'https://www.cert.ssi.gouv.fr/feed/', 'title': 'Nouveau flux RSS depuis l"ANSSI', 'refresh_rate': 60}
        ]
    }
