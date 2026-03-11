1. Create an app
Go to the Dida365 developer platform and create a new application.
After creating the app, you will get:
client_id
client_secret

2. Register the redirect URL
In your Dida365 app settings, configure a redirect URL.
For local testing, you can use: http://localhost:8080/callback
Make sure the redirect_uri in your Python code is exactly the SAME as the one configured in the Dida365 developer console.

3. Install dependencies
pip install requests 
4. Configure your credentials

Edit the Python script and fill in:client_id client_secret redirect_uri

Example:
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "tasks:read tasks:write"

5. Run the program
Start the script: python main.py
The program will print an authorization URL.
Open that URL in your browsr, log in to Dida365, and approve the requested permissions.

6. Get the access token
After authorization, Dida365 will redirect back to your callback URL and you can get accessToken from that url.
