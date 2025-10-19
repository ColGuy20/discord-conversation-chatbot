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
### Message Content Intent
Keep scrolling, and you will see `Privileged Gateway Intents`. Toggle on `Message Content Intent` to allow the bot to receive messages.
### Adding the bot to your server
Now, above the `bot` category click on the `OAuth2` category. Scroll down to the `OAuth2 URL Generator` and select `applications.commands` and `bot`. Scroll down to the `bot permissions` that just popped up and select the permissions you want to give your bot. If you are unsure give it `Administrator` which gives it all the permissions. Use the URL at the bottom to add your bot to your server.
## Set TOKEN in .env
Make `.env` file and set: `BOT_TOKEN={YOUR_TOKEN_GOES_HERE}`
(The token is not a String)
# Steps to using chatGPT API
## Install OpenAI
To install openai run: `pip install openai`
## Set KEY in .env
In `.env` file set: `API_KEY=(YOUR_KEY_GOES_HERE)`
# Containers with Docker
## Download Docker
### Windows:
Click on this link: [Docker Windows Install Link](https://docs.docker.com/desktop/setup/install/windows-install/)
Click `Docker Desktop for Windows - x86_64` to download and run it.
### Mac:
Click on this link: [Docker Mac Install Link](https://docs.docker.com/desktop/setup/install/mac-install/)
Click `Docker Desktop for Mac with Apple silicon` or `Docker Desktop for Mac with Intel chip` depending on your computer to download Docker.
## Run Docker
Run the download file, follow any download procedures, and wait for it to finish. Accept the terms and services. You do not need to sign in; at the top, there is a skip button to avoid putting in your information. At the bottom there is a bar that allows you to run, pause, and stop docker.
## Run Container
Run `docker build -t (IMAGE_NAME) .` (change `(IMAGE_NAME)` depending on the image name that you want). This will build the image for the container. An image is the 'blueprint' for the containers that contains the instructions.
Run `docker run -d -p (PORT) (IMAGE_NAME)` (change `(PORT)` to the one you want to use and `(IMAGE_NAME)` depending on the image name that you chose). This runs the program on the chosen port using the chosen image. For now, I am using the 8080:8080 port for development.
## Useful Docker Commands
### Container Commands
`docker ps -a` - List all containers (Remove `-a` to only show running ones)
`docker stop <container_id>` - Stop a container
`docker restart <container_id` - Restart a container
`docker rm <container_id>` - Remove a container
`docker container prune` - Remove all containers
### Image Commands
`docker images -a` - List all images
`docker rmi <image_name>` - Remove an image
`docker image prune -a` - Remove all images
### Powerful Commands
`docker builder prune` - Reclaim disk space
`docker system prune -a` - Remove everything
