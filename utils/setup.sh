# INSTALL CHROME
sudo apt-get -y update
sudo apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
sudo apt-get -y upgrade

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb
sudo apt-get install -fy

wget https://download3.operacdn.com/pub/opera/desktop/72.0.3815.400/linux/opera-stable_72.0.3815.400_amd64.deb
sudo dpkg -i --force-depends opera-stable_72.0.3815.400_amd64.deb
sudo apt-get install -fy

# UPDATE PYTHON
sudo apt-get install -y python3-pip
sudo pip3 install testresources
sudo python3 -m pip install --upgrade pip setuptools wheel

# # INSTALL REPO
# git clone https://github.com/antonkurenkov/adbtc-single
# cd adbtc-single

# INSTALL DEPENDENCIES
sudo python3 -m pip install --no-deps --force-reinstall -r requirements.txt --no-cache-dir


# sudo apt-get install supervisor
# sudo vi /etc/supervisor/supervisord.conf
# sudo /etc/init.d/supervisor restart