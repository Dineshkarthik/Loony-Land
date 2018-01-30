#!/usr/bin/env bash

command_exists() {
  command -v "$@" > /dev/null 2>&1
}

# Ensure that wget exists
if command_exists wget; then
  wget='wget -O'
else
  # TODO: handle yum installs
  apt-get install -y -q wget
  wget='wget -O'
fi

# update & upgrade
echo 'Hell yeah, Letz install everything'
sudo apt-get update
sudo apt-get -y upgrade

#Chrome
echo 'Hmm,, Chrome'
if command_exists google-chrome --version; then
  echo "Using existing $(google-chrome --version 2>&1)"
else
  sudo apt-get install -y libxss1 libappindicator1 libindicator7
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo dpkg -i google-chrome*.deb
fi

#Terminator
echo "Bored of normal terminal? Feel the power of TERMINATOR. Use 'terminator' command to open"
if command_exists terminator; then
  echo "Using existing $(terminator -v 2>&1)"
else
  echo "Installing terminator....."
  sudo apt-get -y install terminator
fi
 
#sublime
echo 'Hurray, Sublime'
if command_exists subl -v; then
  echo "Using existing $(subl -v 2>&1)"
else
  sudo add-apt-repository ppa:webupd8team/sublime-text-3
  sudo apt-get update
  sudo apt-get -y install sublime-text-installer
fi

#Anaconda
if command_exists conda; then
  echo "Using existing $(conda -V 2>&1)"
else
  # Install in $CONDAPATH, default to $HOME/anaconda
  export BASE=${CONDAPATH:-$HOME/anaconda}

  # Python 3 in Anaconda 2.4.1, 64-bit. From https://www.continuum.io/downloads#_unix
  echo "Downloading 64-bit Anaconda 4.0.0 for Python 3..."
  $wget anaconda.sh http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh
  bash anaconda.sh -b -p $BASE
  rm -rf anaconda.sh
  export PATH=$BASE/bin:$PATH
  printf "\n\n# Add Anaconda to PATH\nexport PATH=$BASE/bin:\$PATH" >> $HOME/.bashrc
fi

#vlc
echo 'Always need VLC for Anime'
if command_exists vlc; then
  echo "Using existing $(vlc --version 2>&1)"
else
  sudo apt-get -y install vlc
fi

#GIT
echo 'Need GIT or you cant use funny commit message'
if command_exists git; then
  echo "Using existing $(git --version 2>&1)"
else
  echo "Installing git..."
  sudo apt-get install -y -q git
fi

#pip
echo 'You ll be installing python packages, so installing pip for you'
if command_exists pip; then
  echo "Using existing $(pip --version 2>&1)"
else
  echo "Installing pip..."
  sudo apt-get -y install pip
fi

#Node
echo "May need node and bower"
if command_exists node; then
  echo "Using existing $(node --version)"
else
  echo "Installing node..."
  source <(wget -qO- https://deb.nodesource.com/setup_4.x)
  apt-get install -y -q nodejs
fi

#Bower
if command_exists bower; then
  echo "Using existing $(bower --version)"
else
  echo 'Installing bower...'
  npm install -g bower
fi