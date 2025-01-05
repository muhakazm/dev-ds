import scrapy

class ZidaneSpider(scrapy.Spider):
    name = "zidane"
    start_urls = ["https://id.wikipedia.org/wiki/Zin%C3%A9dine_Zidane"]

    def parse(self, response):
        # Extract the infobox using XPath or CSS selectors
        infobox = response.css("table.infobox.vcard").get()
        
        # Save the infobox as HTML or print it
        if infobox:
            self.log("Infobox found!")
            with open("infobox.html", "w", encoding="utf-8") as f:
                f.write(infobox)
        else:
            self.log("Infobox not found.")

#[BEGIN][NOTE]
# cmd: scrapy runspider zidane_spider.py
# this script produces infobox.html
#[END][NOTE]