#!/usr/bin/env python
#title           :WeoGeoAPI_Library_Groups.py
#description     :Connect to WeoGeo and get a JSON list of all your groups
#author          :jfee
#date            :20121219
#version         :0.1
#usage           :python WeoGeoAPI_Library_Groups.py
#notes           :
#python_version  :2.7.0
#==============================================================================

print "\nConnecting to WeoGeo\n"

# Import Needed Libraries

import WeoGeoAPI
import getpass

# Get Library Name

wgLibrary = raw_input("WeoGeo Library URL (mylibrary.weogeo.com): ")

# Get User Login

wgLogin = raw_input("User email: ")

# Get Password Without Echoing
PASSWORD = getpass.getpass()

# Build WeoGeo Connection with Library URL, Username and Password

weos = WeoGeoAPI.weoSession(wgLibrary,wgLogin,PASSWORD)

# Connect

weos.connect()

# If connection fails, then quit and tell the user.

if weos.connect() != True:

  print "\nConnection to " + wgLibrary + " failed."
  print "\nCheck your login details.\n"
  print weos

else:

  print "\nLogged in to WeoGeo\n"

  # Get List of Groups

  wgGroups = weos.getGroups()

  print "\nJSON list of Groups in your Library\n"
  print wgGroups