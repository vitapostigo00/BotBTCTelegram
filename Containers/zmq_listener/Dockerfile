FROM python:3.10-slim
RUN apt-get update && apt-get install -y build-essential libgmp-dev git
WORKDIR /home/vita/containers/bot_telegram_btc/BotBTCTelegram/
RUN git clone https://github.com/Vitapostigo/BotBTCTelegram /home/vita/containers/bot_telegram_btc/BotBTCTelegram
COPY ApiToken.py /home/vita/containers/bot_telegram_btc/BotBTCTelegram/Utiles/ApiToken.py
RUN pip install --no-cache-dir -r /home/vita/containers/bot_telegram_btc/BotBTCTelegram/requirements.txt
CMD ["python3.10", "-u" ,"Utiles/subscriptions.py"]