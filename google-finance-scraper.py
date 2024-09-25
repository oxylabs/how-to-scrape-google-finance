from bs4 import BeautifulSoup
import requests
import json

def get_price(soup_element):
   price = soup_element.find('main').find('div','AHmHk').get_text()

   return price


def get_change(soup_element):
   change = soup_element.find('main').find('div','JwB6zf').get_text()

   return change


def get_name(soup_element):
   name = soup_element.find('main').find('div','zzDege').get_text()
  
   return name


def save_results(results, filepath):
   with open(filepath, 'w', encoding='utf-8') as file:
       json.dump(results, file, ensure_ascii=False, indent=4)

   return


def get_finance_html(url):
   payload = {
       'source': 'google',
       'render': 'html',
       'url': url,
   }

   response = requests.request(
       'POST',
       'https://realtime.oxylabs.io/v1/queries',
       auth=('username', 'password'),
       json=payload,
   )

   response_json = response.json()

   html = response_json['results'][0]['content']

   return html


def extract_finance_information_from_soup(soup_of_the_whole_page):
   price = get_price(soup_of_the_whole_page)
   change = get_change(soup_of_the_whole_page)
   name = get_name(soup_of_the_whole_page)

   listing = {
       "name": name,
       "change": change,
       "price": price
   }

   return listing


def extract_finance_data_from_urls(urls):
   constructed_finance_results = []

   for url in urls:
       html = get_finance_html(url)

       soup = BeautifulSoup(html,'html.parser')
  
       finance = extract_finance_information_from_soup(soup)

       constructed_finance_results.append({
           'url': url,
           'data': finance
       })

   return constructed_finance_results


def main():
   results_file = 'data.json'

   urls = [
       'https://www.google.com/finance/quote/BNP:EPA?hl=en',
       'https://www.google.com/finance/quote/.DJI:INDEXDJX?hl=en',
       'https://www.google.com/finance/quote/.INX:INDEXSP?hl=en'
   ]

   constructed_finance_results = extract_finance_data_from_urls(urls)

   save_results(constructed_finance_results, results_file)


if __name__ == "__main__":
   main()
