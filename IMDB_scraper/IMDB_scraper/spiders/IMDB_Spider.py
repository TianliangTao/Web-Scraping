import scrapy

class ImdbSpider(scrapy.Spider):
    # define an unique name for spider class 
    name = 'imdb_spider'
    # start scraping from
    start_urls = ['https://www.imdb.com/title/tt0241527/']

    # needs a parse method to know what to do with the response object
    def parse(self, response):
        '''
        This method is to start on a movie page, and then navigate to the Cast page.
        And call the parse_full_credits(self, response).
        '''
        url = response.url + "fullcredits/"
        yield scrapy.Request(url, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
        '''
        This method is to yield a scrapy.Request for the page of each actor listed on the page.
        And call the method parse_actor_page(self, response)
        '''
        # this command mimics the process of clicking on the headshots on this page
        cast = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        for actor in cast: 
            url = "https://www.imdb.com" + actor
            yield scrapy.Request(url, callback = self.parse_actor_page)


    def parse_actor_page(self, response):
        '''
        This method is to yield a dictionary with two key-value pairs.
        It should yield one such dictionary for each of the movies or TV shows.
        '''
        for movie_or_tv in response.css("div.filmo-row"):
            # extract actor's name
            actor = response.css("span.itemprop::text").get()
            # extract movie or tv's name
            Movie_or_TV = movie_or_tv.css("div.filmo-row b a::text").get()
            yield{
                "actor":actor,
                "Movie_or_TV":Movie_or_TV
            }