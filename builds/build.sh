#!/bin/bash

home=`pwd`

cd ../extension
zip -r CofeeInspector-`date +\%Y\%m\%d`.oex *
mv CofeeInspector-`date +\%Y\%m\%d`.oex $home
