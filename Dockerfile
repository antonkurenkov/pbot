FROM python:3.6.8

# Switch to the target folder
WORKDIR /usr/src/pbot

# Copy files to the target folder
COPY . .

# Install requirements

RUN apt-get -y update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

# Install chrome
RUN apt-get -y upgrade
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i --force-depends google-chrome-stable_current_amd64.deb
RUN apt-get install -fy

# Install opera
#RUN wget https://download3.operacdn.com/pub/opera/desktop/72.0.3815.400/linux/opera-stable_72.0.3815.400_amd64.deb
#RUN dpkg -i --force-depends opera-stable_72.0.3815.400_amd64.deb
#RUN apt-get install -fy

# Install firefox
#RUN apt install -y firefox

RUN python3.6 -m pip install --upgrade testresources pip setuptools wheel
RUN python3.6 -m pip install --force-reinstall -r requirements.txt --no-cache-dir

CMD ["sh", "-c", "python3.6 proxy_bot.py"]


# sudo docker build -t foo0 . && sudo docker run --rm -t foo0
# sudo docker build -t foo0 . && sudo docker run --rm -t -d foo0
# docker logs --follow <container>
# sudo docker build -t foo0 . && sudo docker run --rm -t -d foo0 && sudo docker logs --follow $(sudo docker ps -aq)
# sudo docker rm -f $(sudo docker ps -q) && sudo docker rmi -f $(sudo docker images -q) && sudo docker system prune -a -f
