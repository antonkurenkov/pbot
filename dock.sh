# sudo apt-get -y update
# sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
# sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
# sudo apt-get -y update
# apt-cache policy docker-engine
# sudo apt-get install -y docker-engine
# sudo systemctl status docker
# sudo usermod -aG docker $(whoami)

sudo apt-get update
sudo apt-get install \
	apt-transport-https \
	ca-certificates \
	curl \
	gnupg-agent \
	software-properties-common
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
	"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
	$(lsb_release -cs) \
	stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io