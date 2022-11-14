#!/usr/bin/env bash

set -ex

EXPERIMENT="ctf-resilient-g3"
PROJECT="offtech"

ssh server.${EXPERIMENT}.${PROJECT} "sudo apt-get update; sudo apt-get install -y apache2"

ssh server.${EXPERIMENT}.${PROJECT} "echo '1' | sudo tee /var/www/html/1.html;
echo '2' | sudo tee /var/www/html/2.html;
echo '3' | sudo tee /var/www/html/3.html;
echo '4' | sudo tee /var/www/html/4.html;
echo '5' | sudo tee /var/www/html/5.html;
echo '6' | sudo tee /var/www/html/6.html;
echo '7' | sudo tee /var/www/html/7.html;
echo '8' | sudo tee /var/www/html/8.html;
echo '9' | sudo tee /var/www/html/9.html;
echo '10' | sudo tee /var/www/html/10.html;
sudo rm -f /var/www/html/index.html"


