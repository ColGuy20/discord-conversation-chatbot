# Steps to creating a new bot
## Install python
To install python run: `winget install -e --id Python.Python.3`\n
You can check the version with: `py --version`
## Install discord.py
To install discord python run: `pip install -U discord.py`
## Install .env
To install python dotenv run: `pip install python-dotenv`
## Discord Dev Portal
Click on the link and sign in [Discord Dev Portal Link](https://discord.com/developers/applications)
Create a new app and name it (This is your bot)
### Getting the token
Go to your app, if not already on the page. On the right side you should see the `bot` category (4th Down). Click it and under the username you will see a section named "Token". Reset the token and keep it somewhere safe. This will be your 'secret code' to use your bot.
### Adding the bot to your server
Now, above the `bot` category click on the `OAuth2` category. Scroll down to the `OAuth2 URL Generator` and select `applications.commands` and `bot`. Scroll down to the `bot permissions` that just popped up and select the permissions you want to give your bot. If you are unsure give it `Administrator` which gives it all the permissions. Use the URL at the bottom to add your bot to your server.
## Set TOKEN in .env
Make `.env` file and set: `BOT_TOKEN={YOUR_TOKEN_GOES_HERE}`
(The token is not a String)