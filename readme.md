# Automatic LinkedIn and Discord Posting via RSS Feeds

This project enables automatic retrieval of articles from RSS feeds, generates summaries of these articles using the OpenAI API, and posts them automatically on LinkedIn and Discord.

## Features

- **Automatic Article Retrieval**: Fetches articles from configured RSS feeds at regular intervals.
- **AI-Powered Summarization**: Uses the OpenAI GPT API to generate concise summaries of the articles.
- **LinkedIn Posting**: Automatically posts the generated summaries on LinkedIn.
- **Discord Posting**: Automatically posts the original articles on Discord via a webhook.

## Prerequisites

Before using this project, ensure that the following are installed and configured:

- **Python 3.x**
- **LinkedIn Developer Account**: You need a LinkedIn Developer account with an application configured to get the necessary API keys.
- **Discord Account**: You need a Discord account with a webhook configured for posting messages.
- **Required Python Libraries**:
  - `requests`
  - `beautifulsoup4`
  - `python-dotenv`
  - `linkedin`
  - `xml.etree.ElementTree`

## Setup

1. **Clone this Repository:**

   ```bash
   git clone https://github.com/Momollax/automatic-linkedin-post
   cd automatic-linkedin-post

2. **Create a .env File:**
   Create a .env file in the root directory to store your API keys and other environment variables:
   WEBHOOK_URL=https://discord.com/api/webhooks/xxx
   OPENAI_API_KEY=xxxxxxx
   LINKEDIN_CLIENT_ID=xxxxxxx
   LINKEDIN_CLIENT_SECRET=xxxxxxx
   REDIRECT_URI=http://localhost:8080
   ORG_NAME=xxxxxxx

3. **Install Python Dependencies:**
   Use pip to install the necessary dependencies:
   ```
   pip install -r requirements.txt
   ```
4. **Create and configure Linkedin app product**
   Create a linkedin app on https://www.linkedin.com/developers/apps.
   Make sure your app have 'Share on LinkedIn: Default Tier' AND 'Advertising API: Development Tier'
   you will be asked to fill a form to access the api.

4. **Configure LinkedIn Permissions:**

   Ensure that the following permissions are configured in your LinkedIn application:

   r_liteprofile: To read basic profile information.
   r_emailaddress: To read the user's email address (if needed).
   w_member_social: To post content on behalf of the user.

## Usage
   Run the Script:

   Once everything is configured, you can run the main script:
   ```python main.py```
   This will open a browser window for you to authorize access to your LinkedIn account.

## Configure RSS Feeds:

   RSS feeds are configured in the script as a list of dictionaries. You can modify the FLUX variable in the script to add or remove feeds according to your needs.

## Generation and Posting:

   The script retrieves articles from the configured RSS feeds.
   It uses the OpenAI API to generate a summary of each article in French.
   The generated summary is then automatically posted on LinkedIn.
   The original article is posted on Discord via a webhook.

## Troubleshooting
   LinkedIn Permission Errors
   If you encounter LinkedIn permission errors such as ACCESS_DENIED or Not enough permissions to access,    ensure that:

   The required permissions (r_liteprofile, r_emailaddress, w_member_social) are correctly configured in your LinkedIn Developer application.
   The user has granted these permissions during the OAuth authorization process.
   Configuration Issues
   Environment Variables: Ensure that your .env file is correctly configured with valid API keys and secrets.
   Dependencies: Make sure all the required Python libraries are installed and up to date by running pip    install -r requirements.txt.

## Common Errors

  403 Forbidden: This usually indicates insufficient permissions. Double-check your LinkedIn application   settings and ensure that the user has granted the necessary permissions.
  Connection Errors: If the script fails to connect to LinkedIn or Discord, check your internet connection and ensure the URLs are correct in the .env file.

## Contributing
  Contributions are welcome! If you'd like to improve this project, feel free to fork the repository and   submit a pull request. Please ensure your contributions adhere to the coding standards used in this project.
