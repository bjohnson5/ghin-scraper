# ghin-scraper
In order to scrape the GHIN website for scores, install the following dependencies:
=============

Windows:
--------
- python3: https://www.python.org/downloads/release/python-394/
- firefox: https://www.mozilla.org/en-US/firefox/new/
- beautiful soup: py -m pip install bs4
- selenium: py -m pip install selenium

Linux:
------
- python3: sudo apt-get install python3.6
- firefox: https://www.mozilla.org/en-US/firefox/new/
- beautiful soup: python3 -m pip install bs4
- selenium: python3 -m pip install selenium

To run the scraper on Windows:
==============================
run.bat

To run the scraper on Linux:
============================
run.sh

Tips
====
If the scores you want to export have a "Load More" button on the bottom of the page, click that before running the script.
If the "New login info" banner is showing on the page, close that before running the script.