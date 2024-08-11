import json
import os
import webbrowser
from linkedin import linkedin
from http.server import BaseHTTPRequestHandler, HTTPServer

def authenticate_linkedin(config):
    authentication = linkedin.LinkedInAuthentication(
        config['LINKEDIN_CLIENT_ID'],
        config['LINKEDIN_CLIENT_SECRET'],
        config['REDIRECT_URI'],
        permissions=['rw_organization_admin', 'w_member_social', 'w_organization_social', 'r_basicprofile']
    )

    webbrowser.open(authentication.authorization_url)

    class LinkedInHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = self.path.split('?', 1)[-1]
            params = dict(qc.split('=') for qc in query.split('&'))
            if 'code' in params:
                authentication.authorization_code = params['code']
                access_token = authentication.get_access_token()
                with open('linkedin_access_token.json', 'w') as f:
                    json.dump(access_token, f)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'You can close this window now.')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No code found in the response.')

    server_address = ('', 8080)
    httpd = HTTPServer(server_address, LinkedInHandler)
    print('Server started on port 8080, waiting for the authorization code...')
    httpd.handle_request()

    with open('linkedin_access_token.json', 'r') as f:
        access_token_data = json.load(f)
        if isinstance(access_token_data, list) and len(access_token_data) > 0:
            return access_token_data[0]
        else:
            raise ValueError("Le fichier linkedin_access_token.json n'a pas le format attendu.")
