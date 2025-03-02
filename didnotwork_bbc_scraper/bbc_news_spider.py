import scrapy

class BBCNewsSpider(scrapy.Spider):
    name = "bbc_news"
    start_urls = ["https://www.bbc.com/news"]

    def parse(self, response):
        # Extract headlines (Modify based on actual page structure)
        headlines = response.css("h3::text").getall()

        print("\n📰 Latest BBC News Headlines:")
        for i, headline in enumerate(headlines[:10], start=1):
            print(f"{i}. {headline.strip()}")

# To run this scraper, use the command:
# scrapy runspider bbc_news_spider.py
