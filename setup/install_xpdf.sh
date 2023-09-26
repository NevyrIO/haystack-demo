#! /bin/bash
# install pdftotext for pdf conversion

wget https://dl.xpdfreader.com/xpdf-tools-linux-4.04.tar.gz 
tar -xvf xpdf-tools-linux-4.04.tar.gz 
sudo cp xpdf-tools-linux-4.04/bin64/pdftotext /usr/local/bin
rm -rf xpdf-tools-linux-4.04.tar.gz
rm -rf xpdf-tools-linux-4.04

