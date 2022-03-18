sudo apt update && sudo apt upgrade -y
sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y
sudo apt install xterm imagemagick -y

# default git settings
git config pull.rebase false
git config pull.rebase true
git config pull.ff only

# remove rpi starting wizard
# https://forums.raspberrypi.com/viewtopic.php?p=1675205&sid=b2bf7c8693d4a4cd64b2bb6c125a126c#p1675205
sudo apt purge piwiz -y

curl https://pyenv.run | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> .bashrc
echo 'eval "$(pyenv init --path)"' >> .bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> .bashrc
echo 'screen -dmS app ~/app/.venv/bin/python ~/app/main.py' >> .bashrc

# https://forums.raspberrypi.com/viewtopic.php?t=234879
sudo sed -i -- "s/#xserver-command=X/xserver-command=X -nocursor/" /etc/lightdm/lightdm.conf

source .bashrc

git clone https://github.com/momo-lab/xxenv-latest.git "$(pyenv root)"/plugins/xxenv-latest

pyenv latest install
pyenv latest global

pip install --upgrade pip

pip install poetry

poetry config virtualenvs.in-project true

git clone https://github.com/itsthejoker/swatchrig app/
sudo cp app/extras/swatchrig.service /etc/systemd/system/
sudo systemctl enable swatchrig

cd app
# required for rpi.gpio
# https://forums.raspberrypi.com/viewtopic.php?t=289084#p1747389
export CFLAGS=-fcommon
poetry install
sudo reboot
