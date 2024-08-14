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
            {'url': 'https://www.infosecurity-magazine.com/rss/news/', 'title': 'Nouveau flux RSS depuis InfoSecurity Magazine', 'refresh_rate': 300},
            {'url': 'https://www.darknet.org.uk/feed/', 'title': 'Nouveau flux RSS depuis darknet.org.uk', 'refresh_rate': 300},
            #{'url': 'https://www.kb.cert.org/vuls/atomfeed/', 'title': 'Nouveau flux RSS depuis kb.cert.org', 'refresh_rate': 300},
            {'url': 'https://www.zataz.com/feed/', 'title': 'Nouveau flux RSS depuis Zataz', 'refresh_rate': 300},
            {'url': 'https://www.cert.ssi.gouv.fr/feed/', 'title': 'Nouveau flux RSS depuis l"ANSSI', 'refresh_rate': 300},
            {'url': 'https://blog.rapid7.com/rss/', 'title': 'Nouveau flux RSS depuis l"rapid7', 'refresh_rate': 300},
            {'url': 'https://feeds.feedburner.com/TheHackersNews', 'title': 'Nouveau flux RSS depuis TheHackerNews', 'refresh_rate': 300},
            {'url': 'https://www.nist.gov/blogs/cybersecurity-insights/rss.xml', 'title': 'Nouveau flux RSS depuis le NIST', 'refresh_rate':300},
            {'url': 'https://www.cisa.gov/news.xml', 'title': 'Nouveau flux RSS depuis le CISA', 'refresh_rate': 300},
            #{'url': '', 'title': '', 'refresh_rate': },
        ]
    }
