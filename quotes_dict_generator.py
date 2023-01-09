import requests
import bs4
import lxml
import json


QUOTES_URL='http://quotes.toscrape.com'

quotes_dict = {}

def get_text_from_tags(selector,soup):
    '''This function returns the text inside an specific tag that we get using selectors'''
    tags = soup.select(selector)
    texts = []
    for item in tags:
        texts.append(item.text)
    return texts

def print_quotes_by_cat(categorie):
    '''This function prints quotes when in insert a categorie in the formate of quotes_dict'''
    for author,quote in zip(quotes_dict[categorie]['authors'],quotes_dict[categorie]['quotes']):
        print(f"\t{quote} - {author}\n\n")

def structure_quotes_dict(categorie:str, authors_list:list,quotes_list:list):
    '''This function create a new structured item in the quotes_dict'''
    quotes_dict[categorie] = {'authors': authors_list, 'quotes': quotes_list}

def get_soup(url):
    '''this function makes a request a return a soup'''
    res = requests.get(url)
    return bs4.BeautifulSoup(res.text,'lxml')

def generate_hrefs(initial_url):
    '''This function generetes the array of tags'''
    href = ['/']
    soup = get_soup(initial_url)
    link_tags = soup.select('.tag-item .tag')
    for tag in link_tags:
        href.append(tag.attrs['href'])
    return href

## Creating my dict object 

href_categories = generate_hrefs(QUOTES_URL)

for href in href_categories:
    url = QUOTES_URL + href
    soup = get_soup(url)
    authors = get_text_from_tags('.author',soup)
    quotes = get_text_from_tags('.quote .text',soup)
    if href == '/':
        categorie = 'homepage'
    else:
        categorie = href[5:(len(href)-1)]
    structure_quotes_dict(categorie,authors,quotes)

with open('quotes_dict.json','w') as convert_file:
    convert_file.write(json.dumps(quotes_dict))
## Now printing each quote from each categorie, based on my quotes_dict:

for cat in quotes_dict:
    print(f"Quote Categorie: {cat}\n")
    print_quotes_by_cat(cat)
    print("\n\n\n")







