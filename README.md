# Discordbot

#### Deployment in production
1. Install `docker.io` and `docker-compose`.
2. Edit `docker-compose.yml` and fill in your Discord secret key.
3. Run `docker-compose up` in the project's root directory.

#### Development
When developing this application, you can run it with `python3 discord_bot.py`. If you want to experiment with the docker files, you will need to rebuild the image by running `docker-compose up --build`.