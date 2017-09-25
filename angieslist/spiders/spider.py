import scrapy, re
from bs4 import BeautifulSoup

MainURL = "https://www.angieslist.com/companylist/us/"
BaseURL = "https://www.angieslist.com"

class AngiesList(scrapy.Spider):
    name = "angies"
    allowed_domains = ["angieslist.com"]
    start_urls = [MainURL]

    def parse(self, response):
        Soup = BeautifulSoup(response.body, "lxml")
        for State in Soup.find("ul", attrs={"class", "geocat-cities-list"}).find_all("a"):
            StateName = State.text
            StateHref = State['href']
            MetaData = {
                'StateName' : StateName,
                'StateHref' : StateHref
            }
            yield scrapy.Request(StateHref, meta=MetaData, dont_filter=True, callback=self.grabcities)
            break
    
    def grabcities(self, response):
        Soup = BeautifulSoup(response.body, "lxml")
        for City in Soup.find_all("li", attrs={"class", re.compile(r"-list__item")}):
            CityName = City.find("a").text
            CityHref = City.find("a")['href']
            MetaData = {
                'StateName' :   response.meta['StateName'],
                'StateHref' :   response.meta['StateHref'],
                'CityName'  : CityName,
                'CityHref'  : CityHref
            }
            yield scrapy.Request(CityHref, meta=MetaData, dont_filter=True, callback=self.subcategory)
            break
    
    def subcategory(self, response):
        Soup = BeautifulSoup(response.body, "lxml")
        for SubCat in Soup.find_all("li", attrs={"class", re.compile(r"category__dropdown-list-item")}):
            CategName = SubCat.find("a").text
            CategHref = SubCat.find("a")['href']
            MetaData = {
                'StateName'     :   response.meta['StateName'],
                'StateHref'     :   response.meta['StateHref'],
                'CityName'      :   response.meta['CityName'],
                'CityHref'      :   response.meta['CityHref'],
                'Category'      :   CategName,
                'Category Url'  :   CategHref
            }
            yield scrapy.Request(CategHref, meta=MetaData, dont_filter=True, callback=self.indexpage)
            #break
    
    def indexpage(self, response):
        Soup = BeautifulSoup(response.body, "lxml")
        for Record in Soup.find_all("li", attrs={"class", re.compile(r"list__sp-list-item")}):
            CompanyName = Record.find("h3").text
            CompanyAddr = Record.find("span").text
            yield {
                'State'             :   response.meta['StateName'],
                'State URL'         :   response.meta['StateHref'],
                'City'              :   response.meta['CityName'],
                'City URL'          :   response.meta['CityHref'],
                'Category'          :   response.meta['Category'],
                'Category Url'      :   response.meta['Category Url'],
                'Company Name'      :   CompanyName,
                'Company Address'   :   CompanyAddr
            }
        try:
            RwNextPage = Soup.find("a", re.compile(r"list__pagination-link-next"))
            NextPage = BaseURL + RwNextPage['href']
            if NextPage:
                yield scrapy.Request(NextPage, meta=response.meta, dont_filter=True, callback=self.indexpage)
        except:
            pass
        
