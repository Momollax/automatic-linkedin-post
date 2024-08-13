import requests
import json

def get_organization_urn(access_token, org_name):
    url = f'https://api.linkedin.com/v2/organizations?q=vanityName&vanityName={org_name}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['elements']:
            return data['elements'][0]['id']
        else:
            print("Aucune organisation trouvée avec ce nom.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP lors de la récupération de l'URN de l'organisation : {http_err}")
    except Exception as e:
        print(f"Erreur inattendue lors de la récupération de l'URN de l'organisation : {e}")
    return None

def upload_image_to_linkedin(access_token, image_path, org_urn):
    upload_url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }
    payload = {
        "registerUploadRequest": {
            "owner": org_urn,
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "serviceRelationships": [
                {
                    "identifier": "urn:li:userGeneratedContent",
                    "relationshipType": "OWNER"
                }
            ],
            "supportedUploadMechanism": ["SYNCHRONOUS_UPLOAD"]
        }
    }

    try:
        response = requests.post(upload_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        upload_response = response.json()
        upload_url = upload_response['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset_urn = upload_response['value']['asset']

        # Upload the image file
        with open(image_path, 'rb') as image_file:
            image_response = requests.post(upload_url, headers={'Authorization': f'Bearer {access_token}'}, files={'file': image_file})
            image_response.raise_for_status()

        return asset_urn

    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP lors du téléchargement de l'image : {http_err}")
        print(f"Code d'état : {http_err.response.status_code}")
    except Exception as e:
        print(f"Erreur inattendue lors du téléchargement de l'image : {e}")
    
    return None

def post_to_linkedin(message, access_token, org_name, image_path):
    urn_id = get_organization_urn(access_token, org_name)
    if not urn_id:
        print("Impossible d'obtenir l'URN de l'organisation.")
        return

    org_urn = f"urn:li:organization:{urn_id}"
    image_urn = upload_image_to_linkedin(access_token, image_path, org_urn)
    if not image_urn:
        print("Impossible d'uploader l'image.")
        return

    post_url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }
    payload = {
        "author": org_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "media": image_urn,
                        "title": {
                            "attributes": [],
                            "text": "Image Title Here"
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        response = requests.post(post_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print("Message posté avec succès sur LinkedIn au nom de l'organisation.")
    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP lors de la publication sur LinkedIn : {http_err}")
        print(f"Code d'état : {http_err.response.status_code}")
        print(f"Contenu de la réponse : {response.text}")
    except Exception as e:
        print(f"Erreur inattendue lors de la publication sur LinkedIn : {e}")
