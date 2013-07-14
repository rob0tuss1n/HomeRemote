# /bin/sh

while true; do
    read -p "Do you wish to install HomeRemote?" yn
    case $yn in
        [Yy]* )
            apt-get -y install python nginx motion python-pip python-psutil python-smbus mysql-server python-mysql php5-fpm
            service nginx start
            service mysqld start
            pip install rpi-gpio
        [Nn]* )
            exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
