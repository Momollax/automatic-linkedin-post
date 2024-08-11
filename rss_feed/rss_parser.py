import os
import json
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime

HORO_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'horodatage.json')

DATE_FORMATS = [
    '%a, %d %b %Y %H:%M:%S %z',
    '%a, %d %b %Y %H:%M:%S GMT',
    '%a, %d %b %Y %H:%M:%S',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S%z',
]

def parse_pub_date(pub_date_str):
    for date_format in DATE_FORMATS:
        try:
            if 'GMT' in pub_date_str:
                pub_date_str = pub_date_str.replace('GMT', '+0000')
            return datetime.strptime(pub_date_str, date_format)
        except ValueError:
            continue
    raise ValueError(f"Format de date non reconnu : {pub_date_str}")

def get_items_from_url(url, force=False):
    print(f"Fetching items from {url}")
    
    try:
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        })
        
        page = urlopen(req).read()
    except HTTPError as e:
        print(f"Erreur HTTP lors de la requête à {url}: {e.code} {e.reason}")
        return []
    except URLError as e:
        print(f"Erreur de connexion lors de la requête à {url}: {e.reason}")
        return []
    except Exception as e:
        print(f"Erreur inattendue lors de la requête à {url}: {e}")
        return []

    try:
        root = ET.fromstring(page)
    except ET.ParseError as e:
        print(f"Erreur de parsing XML pour {url}: {e}")
        return []

    lastBuildList = {}
    if os.path.exists(HORO_PATH):
        try:
            with open(HORO_PATH, 'r') as f:
                lastBuildList = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Erreur lors de la lecture du fichier horodatage: {e}")

    date_min = lastBuildList.get(url, 0)
    items = []
    for item in root.iter('item'):
        temp = {}
        try:
            temp['title'] = item.find('title').text if item.find('title') is not None else 'Titre inconnu'
            temp['link'] = item.find('link').text if item.find('link') is not None else 'Lien indisponible'
            
            creator_element = item.find(r'{http://purl.org/dc/elements/1.1/}creator')
            temp['creator'] = creator_element.text if creator_element is not None else 'Auteur Inconnu'
            
            categories = [category.text for category in item.findall('category')]
            temp['categories'] = ', '.join(categories) if categories else 'Non spécifié'
            
            description_element = item.find('description')
            temp['description'] = description_element.text if description_element is not None else 'Pas de description disponible'
            
            comments_element = item.find('comments')
            temp['comments'] = comments_element.text if comments_element is not None else None

            temp['guid'] = item.find('guid').text if item.find('guid') is not None else 'GUID inconnu'

            pub_date_str = item.find('pubDate').text if item.find('pubDate') is not None else None
            if pub_date_str:
                try:
                    temp['pubDate'] = parse_pub_date(pub_date_str)
                except ValueError as e:
                    print(f"Erreur de format de date : {e}")
                    continue
            else:
                print(f"Aucune date de publication trouvée pour un item dans {url}")
                continue

            pubDate = int(temp['pubDate'].timestamp())

            if force or pubDate > date_min:
                items.append(temp)
        except Exception as e:
            print(f"Erreur lors du traitement d'un item du flux {url}: {e}")
            continue

    if items:
        lastBuildDate = max(int(item['pubDate'].timestamp()) for item in items)
        lastBuildList[url] = lastBuildDate

    try:
        with open(HORO_PATH, 'w') as f:
            json.dump(lastBuildList, f)
    except IOError as e:
        print(f"Erreur lors de la sauvegarde du fichier horodatage: {e}")

    return items
