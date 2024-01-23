""" Job Board Aggregator """

from apps.factory import ScraperFactory

if __name__ == "__main__":
    web = input("Enter the job board you want to scrape: \n1. Bright Network\n2. LinkedIn\n ")
    scraper = ScraperFactory(web).get_scraper()
    scraper.scrape()