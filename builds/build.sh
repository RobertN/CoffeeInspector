#!/bin/bash

home=`pwd`
date=`date +\%Y\%m\%d`
fileName="CoffeeInspector-$date.oex"

cd ../extension

zip -r $fileName *
cp $fileName /var/www/kaffe
mv $fileName $home

cd $home
cd ../server

cat checkUpdate.xml | sed -e "s/FILENAME/$fileName/" > /var/www/kaffe/checkUpdate.xml
