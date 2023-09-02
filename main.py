import requests
from bs4 import BeautifulSoup
import pygame

pygame.init
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
url = "https://www.google.com/search?q=python+web+scraping&oq=python+web+scraping&aqs=chrome..69i57j0l7.2875j0j7&sourceid=chrome&ie=UTF-8"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")





while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    clock.tick(60)




# for link in soup.find_all("a"):
#     print(link.get("href"))

