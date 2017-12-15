#!/bin/bash
echo "BASE SETUP START"
# debian frontend noninteractive disables user interaction
DEBIAN_FRONTEND=noninteractive sudo apt-get -qqy update
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy git
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy bridge-utils
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy ebtables
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy python-pip
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy python-dev
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy build-essential
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy curl
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy tcpdump
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy x-window-system
DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy gnome-core
sudo pip install -U pbr
echo export LC_ALL=en_US.UTF-8 >> ~/.bash_profile
echo export LANG=en_US.UTF-8 >> ~/.bash_profile
sudo pip install --upgrade pipo
git clone git://github.com/robbyrussell/oh-my-zsh.git /home/vagrant/.oh-my-zsh
apt-get -y install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
chsh -s /bin/zsh vagrant
echo "BASE SETUP DONE"
