# LPSE Parser
LPSE Parser - as reflected by its name - is a data parser for LPSE websites

Developed for KPP Pratama Kotabumi.

#### Requirements

* Python3.5.3+
* urllib
* requests
* ssl
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

#### Configuration

In `vars.py`, several parameters need to be configured
* `govName` is the name of the website (without the trailing go.id or any subdomain)
* `staticCode` is the last 3 numbers in `Kode` column of `/eproc4/lelang`
* `lowNum` and  `highNum` is the lower and upper bounds for the iteration.

#### Running

Use `python main.py` to scrape several information from `pengumumanlelang` page.
The result will be recorded in `results` folder in csv format.

#### NOTE

I am not responsible to any damage to the server due to the excessive requests sent from the script.


#### PROJECT STATUS

The project is under development where other pages will be scraped in addition to the existing ones.
A database might also be needed to manage complex data structure, rather than the current mechanism 
of storing the data to csv format.

#### TODO

* Create other pages' scrapers
* Build a database system
* Build a reporting system ([POD](http://appyframework.org/pod.html) might be interesting)
* Auto update for new data