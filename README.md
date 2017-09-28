## Angieslist.com Scraper

Scrap `Company Name` & `Address` of all **USA based** companies.

How to use the script:<br>
    `scrapy crawl angies -o mylist.csv -t csv`

- [x] Basic bugs fixed
- [x] Verified on Windows / Linux machines
- [ ] SQL dump included
- [ ] Captcha resistant

Installation guide for Windows:<br>
1. Install visual c dependencies for Python
    * https://www.microsoft.com/en-us/download/details.aspx?id=44266
2. Download and install Python 2.7
    * https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi
3. Download this repository and unzip it
4. Execute "install.bat" file and will will install scrapy along with it dependencies
5. Execute "execute.bat" file and it will save data in a csv file in same folder
