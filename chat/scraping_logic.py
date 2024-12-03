
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from urllib.parse import urljoin, urlparse
class ScrapeData():
    def __init__(self, base_url, site_name) -> None:
        self.visited_links = set()
        self.base_url = base_url
        self.output_file = f"{site_name}.txt"
        self.content_buffer = ""  
        self.crawl_website(self.base_url)


    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") 
        self.driver = webdriver.Chrome(options=options)
        return self.driver
    
    def normalize_domain(self, url):
        """Normalize domain by stripping 'www.' prefix if present."""
        parsed_url = urlparse(url)
        netloc = parsed_url.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return parsed_url._replace(netloc=netloc).geturl()

    def get_links(self, driver):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = set()

        for link in soup.find_all('a', href=True):
            url = link['href']
            print(url)

            # Skip external links (i.e., links to a different domain)
            if url.startswith('http'):
                normalized_base_url = self.normalize_domain(self.base_url)
                normalized_url = self.normalize_domain(url)

                # If the domains match (considering www and non-www equivalence)
                if normalized_url.startswith(normalized_base_url) and url not in self.visited_links:
                    links.add(url)

            # Handle relative URLs (e.g., /path, /#fragment)
            elif '/' in url:
                if url.startswith('/'):
                    # Convert relative URL to absolute URL by joining with base URL
                    absolute_url = urljoin(self.base_url, url)
                else:
                    # Relative URL without leading '/', prepend base URL path
                    absolute_url = urljoin(self.base_url.rstrip('/') + '/', url)

                # Add only if it's within the same domain/subdomain
                normalized_base_url = self.normalize_domain(self.base_url)
                normalized_url = self.normalize_domain(absolute_url)

                # Ensure the URLs are from the same base URL or subdomains
                if normalized_url.startswith(normalized_base_url) and absolute_url not in self.visited_links:
                    links.add(absolute_url)

        return links

    def save_text_content(self, driver, url):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        text_content = soup.get_text(separator="\n", strip=True)
        if url[-1] == '/':
            url = url[:-1]
        filename = url.split('/')[-1].strip('.com')
        print(filename)
        
        self.content_buffer += f"URL: {url}\n"
        self.content_buffer += text_content.replace('\n', " ")
        self.content_buffer += "\n\n"

    def visit_link(self, driver, url):
        if url in self.visited_links:
            return
        self.visited_links.add(url)
        try:
            driver.get(url)
            time.sleep(2)  
        except Exception as e:
            print(f"Error visiting {url}: {e}")
            return

        self.save_text_content(driver, url)
        links = self.get_links(driver)
        print(links)

        for link in links:
            self.visit_link(self.driver, link)
            
    def crawl_website(self, base_url):
        driver = self.setup_driver()
        try:
            self.visit_link(driver, base_url)
        finally:
            driver.quit()
            
            os.makedirs('media', exist_ok=True) 
            with open(os.path.join('media', self.output_file), "w", encoding="utf-8") as f:
                f.write(self.content_buffer)
            print(f"Scraping completed. Text data saved to {self.output_file}.")




