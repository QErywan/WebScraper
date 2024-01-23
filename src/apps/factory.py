from apps.brightnetwork import BrightNetworkScraper
from apps.linkedin import LinkedInScraper

class ScraperFactory():
    
    def __init__(self, scraper):
        self.scraper = scraper
    
    def get_scraper(self):
        scraper_map = {
            "1": BrightNetworkScraper,
            "2": LinkedInScraper,
        }

        try:
            scraper = scraper_map[self.scraper]()
            return scraper
        except KeyError:
            raise ValueError(f"Scraper {self.scraper} not found")