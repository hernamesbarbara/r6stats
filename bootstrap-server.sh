#!/usr/bin/env bash
# -*- coding: utf-8 -*- 

sudo apt-get update
sudo apt install python3-pip
pip3 install --upgrade pip
sudo apt install ipython3


curl https://raw.githubusercontent.com/hernamesbarbara/dotfiles/master/bash_aliases > ~/.bash_aliases
