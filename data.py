from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from selenium import webdriver



urls = [
"https://ximbio.com/reagent/151107/anti-plap-hd-8b6",
"https://ximbio.com/reagent/151105/anti-integrin-a2-has-4",
# "https://ximbio.com/reagent/151108/anti-ptprc-hle-12d1",
# "https://ximbio.com/reagent/151111/anti-icam3-icam-32",
# "https://ximbio.com/reagent/151114/anti-keratin71317-18-lds-23",
# "https://ximbio.com/reagent/151096/anti-integrin-alpha-3-f35-177-1",
# "https://ximbio.com/reagent/151117/anti-hladr-lhm-4",
# "https://ximbio.com/reagent/151097/anti-egfr-f4",
]



title1 = []
antigen_Gene = []
reactivity = []
host = []


for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')


    header1 = soup.find('h1').get_text().strip()

    start_index_square_bracket = ''
    end_index_square_bracket = ''

    start_index_prantsies = ''
    end_index_prantsies = ''
    time.sleep(1)
    for index, letter in enumerate(header1):
        if letter == '[':
            start_index_square_bracket += str(index)
            continue
        elif letter == ']':
            end_index_square_bracket += str(index)
            continue
        elif letter == '(':
            start_index_prantsies += str(index)
            continue
        elif letter == ')':
            end_index_prantsies += str(index)
            continue
        else:
            continue
        
    time.sleep(1)

    if start_index_square_bracket and end_index_square_bracket:
        title1.append(header1[int(start_index_square_bracket):int(end_index_square_bracket)+1])
    elif start_index_prantsies and end_index_prantsies:
        title1.append(header1[int(start_index_prantsies):int(end_index_prantsies)+1])
    else:
        print(url)
        continue


    if not soup.select("tr:-soup-contains('Antigen/Gene or Protein Targets') td:nth-of-type(2)"):
        antigen_Gene.append("N/A")

    elif soup.select("tr:-soup-contains('Antigen/Gene or Protein Targets') i"):
        antigen_Gene.append(soup.select("tr:-soup-contains('Antigen/Gene or Protein Targets') i")[0].text.strip())

    elif soup.select("tr:-soup-contains('Antigen/Gene or Protein Targets') td:nth-of-type(2)"):
        antigen_Gene.append(soup.select("tr:-soup-contains('Antigen/Gene or Protein Targets') td:nth-of-type(2)")[0].text.strip())

    time.sleep(1)
        
    react = soup.select("tr:-soup-contains('Reactivity') td:nth-of-type(2)")
    if react:
        reactivity.append(soup.select("tr:-soup-contains('Reactivity') td:nth-of-type(2)")[0].text.strip())
    elif soup.select("tr:-soup-contains('Antigen/Gene or Protein Targets') i"):
        reactivity.append(soup.select("tr:-soup-contains('Antigen/Gene or Protein Targets') i")[0].text.strip())
    else:
        reactivity.append("N/A")            



    host1 = soup.select("tr:-soup-contains('Host') td:nth-of-type(2)")
    if host1:
        host.append(soup.select("tr:-soup-contains('Host') td:nth-of-type(2)")[0].text.strip())
    else:
        host.append("N/A")


    time.sleep(2)


    print(url)


l1 = title1
l2 = antigen_Gene
l3 = reactivity
l4 = host



s1 = pd.Series(l1, name='Title')
s2 = pd.Series(l2, name='Antigen Gene')
s3 = pd.Series(l3, name='Reactivity')
s4 = pd.Series(l4, name='Host')



df = pd.concat([s1, s2, s3, s4], axis=1)
df.to_csv('example_01.csv', index=False)
print("Done")
