# UQ Degree Information Scraper

## Overview

A collection of python scripts I wrote to scrape the UQ website for information about UQ programs, plans, and courses; read the function documentation in main.py for some more detail as to the data that can be scraped. 
 
Intended for use generating data for the the attached schema that is currently in use for UQDegreePlanner, but is possibly reusable in other contexts with a few modifications.

## Dependencies

* A mysql database

The program currently scrapes data directly into a mySQL database; this will require a mySQL database on the local machine. See:
https://www.mysql.com/downloads/

* Requests library:

pip3 install requests

* mySQL Connector:

Only tested with Ubuntu Linux 20.10 (x86, 64-bit), DEB  but is likely to work on other distributions. See main.py for an example of the connector object that is required.

* BeautifulSoup:

pip3 install beautifulsoup4

* Selenium:

pip3 install selenium

You will also need a webdriver: I used the firefox for linux64 release found here https://github.com/mozilla/geckodriver/releases/tag/v0.29.0

## Credit

Based on Lilac Kapul's uqinfo found here:
https://github.com/liilac/uqinfo
