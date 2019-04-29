import scrapy
import os


class Spider(scrapy.Spider):
    name = "operr"
    start_urls = ["http://www.city-data.com/accidents/acc-Cincinnati-Ohio.html"]

    def parse(self, response):
        SET_SELECTOR = 'tbody > tr'
        try:
            os.remove("scraper_output.txt")
        except OSError:
            pass
        with open("scraper_output.txt", "w") as log:
            for dataSet in response.css(SET_SELECTOR):
                NAME_SELECTOR = 'td ::text'
                extracted = dataSet.css(NAME_SELECTOR).extract()
                if len(extracted) == 8:
                    result = '{{\'Date\':{}, \'Location\':{}, \'Vehicles\':{}, \'Drunken persons\':{}, \'Fatalites\':{}, \'Persons\':{}, \'Pedestrians\':{}}}\n'.format(
                        extracted[1],extracted[2],extracted[3],extracted[4],extracted[5],extracted[6],extracted[7])
                    log.write(result)