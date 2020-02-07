#! /bin/bash

function check_ubuntu_package() {
    cmd=`dpkg -l | grep $1`
    if [${cmd} -n ]; then
        echo "NOT INSTALLED"
    else
        echo "OK"
    fi
}

function check_python_package() {
    cmd=`pip3 list | grep $1`
    if [${cmd} -n ]; then
        echo "NOT INSTALLED"
    else
        echo "OK"
    fi
}

function get_ip_address() {
    ip=`ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
    if [ ${ip} -z]; then
        echo "No eth0 network"
    else
        echo $ip
    fi
}

function get_opencv_version() {
   cmd=`pkg-config --modversion opencv`
   if [${cmd} -n]; then
       echo "Not Installed"
   else
       echo $cmd
   fi
}

#sudo apt-get update
#sudo apt-get upgrade
#sudo apt-get install pkg-config


echo ""
echo -e "Client Ip Address\t$(get_ip_address)"
echo "========================================"
echo -e "Open CV\t$(get_opencv_version)"
echo "========================================"
echo " Python Packages"

for package in "RPi.GPIO" "json-rpc" "opencv-contrib-python" "requests"
do
    echo -e "$package\t$(check_python_package $package)"
done

echo ""


