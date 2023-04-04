from urllib.request import urlopen, Request
from pathlib import Path
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse, urljoin

scraping_dir = Path.cwd() / "python-image-crawler"
scraping_dir.mkdir(parents=True, exist_ok=True)
save_dir = str(f"{scraping_dir}/")
urls = []
base_urls = []
reqs = []
soups = []
img_tags = []
img_list = []

url_input = input("Paste URL here, add commas if multiple URLs (Ex: https://protocolten.com,www.gmail.com,youtube.com): ")

for url in url_input.split(','):
    urls.append(url)

headers = {''
           'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0;'
                         ' Nexus 5 Build/MRA58N) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'}


for url in urls:
    req = Request(url, headers=headers)
    reqs.append(req)
    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
    base_urls.append(base_url)

for req in reqs:
    html_doc = urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(html_doc, 'lxml')
    soups.append(soup)

base_url = ''
save_count = 0
error_count = 0
for soup in soups:
    img_tags = soup.find_all("img")
    for img in img_tags:
        if 'src' in img.attrs and 'http' in img['src'][:4]:
            img_list.append(img['src'])
            base_url = base_urls[soups.index(soup)]
        elif 'src' in img.attrs and '/' in img['src'][:1]:
            base_url = base_urls[soups.index(soup)]
            absolute_url = urljoin(base_url, img['src'])
            img_list.append(absolute_url)

    for i, img_url in tqdm(enumerate(img_list)):
        img_name = f"{base_url[8:]}_{i}_{img_url[-5:]}"
        file_path = save_dir + img_name
        try:
            urllib.request.urlretrieve(img_url, file_path)
            save_count += 1
            if i == 0:
                print(f"\n\nSaving images...\n")
        except Exception as e:
            print(f'Error downloading {img_url}: {str(e)}')
            error_count += 1
            continue

print(f"\nImages saved: {save_count}")
print(f"Errors: {error_count}")

