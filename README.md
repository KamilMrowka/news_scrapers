# Python Scapers for two news websites:
1. Patch.com - Local News for USA cities and states.
2. Globalnews.ca - Global News

## Project info
Most of the logic lives under the **localnews/spiders** directory.  
There are two intereseting files:
1. newsspider.py
2. globalspider.py

When the application is ran, they produce two .json files. 
1. **1st_set.json** - dataset of scraped local news
2. **2nd_set.json**  - dataset of scraped global news

## Notes
This was built to gather some data for a simple AI powered poc news sorting application.  
The scraped news are not meant to be used outside of local environments.
