# /bin/sh

while true; do
    read -p "Do you wish to install HomeRemote?" yn
    case $yn in
        [Yy]* )
            read -p "Please enter your name: " name
            read -p "Please enter a root password: " password
            apt-get -y install python nginx motion python-pip python-psutil python-rpi.gpio python-tornado python-smbus mysql-server python-mysql php5-fpm
            service nginx start
            service mysqld start
            mysqladmin -u root password $password
            pip install rpi-gpio
            md5 = $password | md5sum
            echo -n $md5
            mysql -u root -p$password "INSERT INTO `accounts` VALUES ('1', '$name', 'root', '$md5', '');"
        [Nn]* )
            exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
