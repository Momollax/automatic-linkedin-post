import json
from urllib import request
from urllib.error import HTTPError, URLError

def post_item_to_discord(item, title, webhook_url):
    embed = {
        'title': item['title'],
        'description': item['description'],
        'url': item['link'],
        'timestamp': item['pubDate'].isoformat(),
        'author': {
            'name': item['creator']
        },
        'fields': [
            {
                'name': 'Flux RSS',
                'value': title,
                'inline': True
            },
            {
                'name': 'Catégories',
                'value': item['categories'],
                'inline': True
            },
            {
                'name': 'Lien',
                'value': f"[Cliquez ici pour lire l'article]({item['link']})",
                'inline': True
            },
            {
                'name': 'Publié le',
                'value': item['pubDate'].strftime('%A %d %B %Y à %H:%M'),
                'inline': False
            }
        ]
    }
    
    if item.get('comments'):
        embed['fields'].append({
            'name': 'Commentaires',
            'value': f"[Voir les commentaires]({item['comments']})",
            'inline': False
        })
    
    payload = {
        'embeds': [embed]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    }
    
    try:
        req = request.Request(url=webhook_url,
                              data=json.dumps(payload).encode('utf-8'),
                              headers=headers,
                              method='POST')
        r = request.urlopen(req)
        print(f"Message envoyé avec succès à Discord: {r.status} {r.reason}")
    except HTTPError as e:
        print(f"Erreur HTTP lors de l'envoi à Discord: {e.code} {e.reason}")
    except URLError as e:
        print(f"Erreur de connexion lors de l'envoi à Discord: {e.reason}")
    except Exception as e:
        print(f"Erreur inattendue lors de l'envoi à Discord: {e}")
