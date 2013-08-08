#!/bin/bash

while true; do
    if [[ $EUID -ne 0 ]]; then
        echo "This script must be run as root!"
        echo "Please execute using the following command:"
        echo " sudo ./setup.sh"
        exit 1
    fi
    if [ -d "/etc/homeremote" ]; then
        echo "RemoteHome installation directory has been found!"
        read -p "Do you wish to uninstall HomeRemote? " ynuninstall
        case $ynuninstall in
            [Yy]* )
                pkill python
                rm -rf /etc/homeremote
                rm -rf /var/www/*
                echo "HomeRemote has been sucessfully uninstalled from your system."
                echo "Please be aware that all dependencies still remain."
                echo "Have a nice day"
                exit;;
            [Nn]* )
                exit;;
            * )
                exit;;
        esac
    fi
    read -p "Do you wish to install HomeRemote? " yn
    case $yn in
        [Yy]* )
            BASEDIR=$(pwd)
            read -sp "Please enter a root password: " password
            echo
            read -sp "Please confirm your root password: " confirmpass
            echo
            if [ $password != $confirmpass ]; then
                echo "Passwords do not match! Please restart install script!"
                exit
            fi
            echo "Updating apt repositories to make sure we get the latest packages"
            # apt-get update > /dev/null
            
            echo "Installing all required packages"
            apt-get -y install python lighttpd php5-common php5-cgi php5 motion sqlite3 python-pip python-psutil python-rpi.gpio git python-tornado python-smbus > /dev/null
            echo "Enabling fastcgi for PHP"
            lighty-enable-mod fastcgi-php > /dev/null
            echo "Reloading webserver"
            service lighttpd force-reload > /dev/null
            echo "Creating installation directories"
            mkdir /etc/homeremote > /dev/null
            echo "Copying server files to installation directory"
            cp -r ./Server/* /etc/homeremote/ > /dev/null
            echo "Copying web interface files to webserver root"
            rm /var/www/index.html > /dev/null
            cp -r ./Web/* /var/www/ > /dev/null
            echo "Enabling I2C and SPI devices"
            rm -f /etc/modprobe.d/raspi-blacklist.conf > /dev/null
            cp ./raspi-blacklist.conf /etc/modprobe.d/
            echo "Downloading RF24 library"
            git clone https://github.com/stanleyseow/RF24 > /dev/null
            cd RF24/librf24-rpi/librf24
            echo "Installing RF24 library"
            make > /dev/null
            make install > /dev/null
            cd /etc/homeremote/RF-Test
            chmod +x ./build.sh > /dev/null
            sh ./build.sh > /dev/null
            cd $BASEDIR
            rm -rf ./RF24
            echo
            echo "Successfully installed files for HomeRemote. Please provide a few details about yourself and your home!"
            echo "WE DO NOT COLLECT OR RECORD ANY DATA. ALL DATA IS STORED ON *YOUR* RASPBERRY PI"
            echo "Please enter the following data:"
            read -p "Please enter your name: " name
            read -p "Street Address e.g. 3285 Orlando Ave: " streetadd
            read -p "City: " city
            read -p "State: " state
            read -p "Zip: " zip
            echo "Downloading city ID for weather API. Weather API services provided by OpenWeatherMap.org. Weather data provided by Weather.gov"
            wget -q -O weather.json "http://api.openweathermap.org/data/2.5/weather?q=$city" > /dev/null
            cid=$(grep -Po '(?<="id":)[^,]*' weather.json | tail -1) > /dev/null
            echo "Storing user information into database"
            sqlite3 /etc/homeremote/database.db "INSERT INTO "main"."settings" ("id", "field", "value") VALUES (1, 'city_id', '$cid');"
            sqlite3 /etc/homeremote/database.db "INSERT INTO "main"."settings" ("id", "field", "value") VALUES (2, 'owner_name', '$name');"
            sqlite3 /etc/homeremote/database.db "INSERT INTO "main"."settings" ("id", "field", "value") VALUES (3, 'street_address', '$streetadd');"
            sqlite3 /etc/homeremote/database.db "INSERT INTO "main"."settings" ("id", "field", "value") VALUES (4, 'city', '$city');"
            sqlite3 /etc/homeremote/database.db "INSERT INTO "main"."settings" ("id", "field", "value") VALUES (5, 'state', '$state');"
            sqlite3 /etc/homeremote/database.db "INSERT INTO "main"."settings" ("id", "field", "value") VALUES (6, 'zip', '$zip');"
            echo
            echo "Thank you for installing HomeRemote!"
            echo "We have to reboot your Raspberry Pi to put some system changes into effect"
            echo "Once we have rebooted, to start HomeRemote in GUI mode, use:"
            echo " python /etc/homeremote/start.py"
            echo "For more info, visit http://github.com/kilker12/HomeRemote/wiki"
            read -p "Press enter to reboot system"
            reboot
            exit
            ;;
        [Nn]* )
            exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
