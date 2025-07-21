import pandas as pd
import requests
import json
import bs4
import re, csv

page = "拳銃"
headers = {'User-Agent': 'Sample Header'}
url = f"https://ja.wikipedia.org/w/rest.php/v1/page/{page}/html"

response = requests.get(url) #header指定も可能
html = response.content
#print(html)

#print(response)

#print(response.text)

if response == 200:
    print("Success")
else:
    print("Failed:status_code is " + str(response.status_code))

'''requestsで取得したデータをbs4でテキストに見やすい形式で変換'''
soup = bs4.BeautifulSoup(response.text, 'html.parser')
#print(soup)

source = soup.find_all("a")
#print(table)
#print(source)

#特定の文言で抜き出す
source_pickup = soup.find_all(rel=re.compile("mw:WikiLink"))
#print(source_pickup)
print(type(source_pickup))


csvlist = []

for link in source_pickup: # aタグのテキストデータを配列に格納
    sample_txt = link.text
    csvlist.append(sample_txt)
    
#print(csvlist)
header = ["ID", "File"] 

with open("output.csv", "w", encoding="cp932", newline='') as f:

    #辞書型なら、DictWriterだが、配列ならwriterオプション使用可
    writecsv = csv.writer(f, lineterminator='\n')
    writecsv.writerow(csvlist)


with open("output.csv") as output_result:
    print(output_result.read())
    
#for a in csvlist:
    #print(a)
    
    #writecsv.writerows(header)
    #writecsv.writerow(a)
    
#f = open("output.csv", "w", newline='')
#fieldnames = ['Guns', 'Genre']

#writecsv = csv.DictWriter(f, fieldnames=fieldnames)



#for a in csvlist:
#    writecsv.writerow(a)

#source_text = source.split("¥n")
#print(source_text)

#print(df)