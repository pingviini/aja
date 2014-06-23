#!/bin/sh
cd /var/buildout
aja init:plone,/vagrant/plone-4.3.cfg
aja -H plone deploy