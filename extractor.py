import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import urllib.parse
import time

def generate_headers():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    return headers


async def extract_urls(session, url, headers):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            urls = set(anchor_tag.get('href') for anchor_tag in soup.find_all('a'))
            joined_urls = [urllib.parse.urljoin(url, href) for href in urls if href]
            return joined_urls
    except aiohttp.ClientError:
        return []


async def get_website_title(session, url, headers):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            title = soup.title.string.strip() if soup.title else ''
            return title
    except aiohttp.ClientError:
        return ''


async def process_website(session, website, headers):
    website = website.strip()
    parsed_url = urllib.parse.urlparse(website)
    if not parsed_url.scheme:
        website = f"https://{website}"
    try:
        urls = await extract_urls(session, website, headers)
        title = await get_website_title(session, website, headers)
        website_data = {
            "website": website,
            "title": title,
            "urls": urls
        }
        return website_data
    except aiohttp.ClientError:
        return None


async def process_websites(file_path):
    result = []
    visited_websites = set()
    all_urls = set()
    headers = generate_headers()

    async with aiohttp.ClientSession() as session:
        try:
            with open(file_path, 'r') as file:
                tasks = []
                for website in file:
                    website = website.strip()
                    if website and website not in visited_websites:
                        visited_websites.add(website)
                        tasks.append(process_website(session, website, headers))

                print("Process                   :  Started")

                start_time = time.time()
                website_data_list = await asyncio.gather(*tasks, return_exceptions=True)
                end_time = time.time()

                print("Extraction                :  Complete")
                print("Time                      :  {:.2f} seconds".format(end_time - start_time))

                for website_data in website_data_list:
                    if isinstance(website_data, dict):
                        all_urls.update(website_data['urls'])
                        result.append(website_data)

            total_websites_scrapped = len(result)
            total_urls_scrapped = len(all_urls)
            print("Total Websites Scrapped   : ", total_websites_scrapped)
            print("Total URLs Collected      : ", total_urls_scrapped)

        except FileNotFoundError:
            print("File not found")

    return result


def main():
    input_file_path = input("Enter the path to the input file: ")

    output_file_name = input("Enter the output file name (Press Enter to use 'output.json'): ")
    output_file_path = output_file_name.strip() if output_file_name else 'output.json'

    scraped_data = asyncio.run(process_websites(input_file_path))

    with open(output_file_path, 'w') as output_file:
        json.dump(scraped_data, output_file, indent=4)

if __name__ == "__main__":
    main()
