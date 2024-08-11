from config.config import load_config
from linkedin_integration.linkedin_auth import authenticate_linkedin
from linkedin_integration.linkedin_post import post_to_linkedin
from rss_feed.rss_parser import get_items_from_url
from rss_feed.discord_post import post_item_to_discord
from gpt_integration.gpt_prompt import ask_gpt
import time

def main():
    config = load_config()
    access_token = authenticate_linkedin(config)
    last_checked = {flux['url']: 0 for flux in config['FLUX']}
    
    try:
        while True:
            current_time = time.time()

            for flux in config['FLUX']:
                url = flux['url']
                title = flux['title']
                refresh_rate = flux['refresh_rate']

                if current_time - last_checked[url] >= refresh_rate:
                    items = get_items_from_url(url)
                    for item in items:
                        chatgpt_message = ask_gpt(item['link'], config['OPENAI_API_KEY'])
                        if chatgpt_message:
                            post_to_linkedin(chatgpt_message, access_token, config['ORG_NAME'])
                            post_item_to_discord(item, title, config['WEBHOOK_URL'])
                        else:
                            print("L'article n'a pas été publié car il n'a pas été jugé intéressant.")
                        time.sleep(2)  # Pause entre les envois pour éviter de dépasser les limites de taux

                    last_checked[url] = current_time

            time.sleep(1)

    except KeyboardInterrupt:
        print("Script interrompu par l'utilisateur. Fermeture propre du script.")

if __name__ == '__main__':
    main()
