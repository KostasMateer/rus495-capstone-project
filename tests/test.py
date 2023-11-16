# Example using Beautiful Soup
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'https://novayagazeta.ru/'

# Initiate a browser instance (make sure you have the appropriate driver installed, e.g., chromedriver)
driver = webdriver.Edge()

# Navigate to the URL
keyword = "путин"
search_url = f"https://novayagazeta.ru/search?q={keyword}"
driver.get(search_url)

# Wait for the page to fully load (you may need to adjust the time)
driver.implicitly_wait(10)  # wait 10 seconds

# Get the rendered HTML
html = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Now you can use BeautifulSoup to find elements in the rendered HTML
print(soup.prettify())
test = soup.find_all('article')
for article in soup.find_all('article'):
    title = article.find('h2', class_='your_class_here').text
    link = article.find('a', class_='your_class_here')['href']
    print(f'Title: {title}')
    print(f'Link: {link}')

# Don't forget to close the browser once you're done
driver.quit()



