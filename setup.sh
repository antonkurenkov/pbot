sudo apt-get -y update

# INSTALL PYTHON
sudo apt install -y build-essential checkinstall
sudo apt install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
cd ..
wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tar.xz
tar xvf Python-3.6.8.tar.xz
cd Python-3.6.8
sudo ./configure --enable-optimizations
sudo make -j8
sudo make install

# INSTALL SCREEN LIBS
sudo apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
sudo apt-get -y upgrade

# INSTALL CHROME
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb
sudo apt-get install -fy

# INSTALL OPERA
wget https://download3.operacdn.com/pub/opera/desktop/72.0.3815.400/linux/opera-stable_72.0.3815.400_amd64.deb
sudo dpkg -i --force-depends opera-stable_72.0.3815.400_amd64.deb
sudo apt-get install -fy

# INSTALL FIREFOX
sudo apt install -y firefox

# UPDATE PYTHON
sudo apt-get install -y python3-pip
sudo pip3 install testresources
sudo python3.6 -m pip install --upgrade pip setuptools wheel

# INSTALL DEPENDENCIES
cd pbot
sudo python3.6 -m pip install --no-deps --force-reinstall -r requirements.txt --no-cache-dir


# sudo apt-get install supervisor
# sudo vi /etc/supervisor/supervisord.conf
# sudo /etc/init.d/supervisor restart