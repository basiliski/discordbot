# Dockerfile for discordbot
# Takes care of automatic dependency installing
# and ENV variable management

FROM python:3
ADD discord_bot.py /
RUN pip install discord.py
RUN pip install jikanpy

CMD [ "python", "./discord_bot.py" ]
