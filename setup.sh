# /bin/sh

while true; do
    read -p "Do you wish to install HomeRemote? " yn
    case $yn in
        [Yy]* )
            read -p "Please enter your name: " name
            read -sp "Please enter a root password: " password
            read -sp "Please confirm your root password: " confirmpass
            if [ "$password" -nt "$confirmpass" ]; then
				echo "Passwords do not match! Please restart install script!"
				exit
			fi
            sudo apt-get update
            sudo apt-get -y install python nginx motion python-pip python-psutil python-rpi.gpio python-tornado python-smbus php5-fpm
            sudo service nginx start
            mkdir /etc/homeremote
            cp -r ./Server/* /etc/homeremote
            cp -r ./Web/* /usr/share/nginx/www/
            echo "Thank you for installing HomeRemote!\n"
            echo "To start in GUI mode, simply execute the command:\n"
            echo "sudo python /etc/homeremote/start.py\n"
            echo "For more info, visit http://github.com/kilker12/HomeRemote/wiki"
            ;;
        [Nn]* )
            exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
