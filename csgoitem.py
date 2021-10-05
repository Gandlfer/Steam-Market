import json
import requests
from bs4 import BeautifulSoup, element

RARITY={
    1:    "Consumer" ,
    2:    "Industrial",
    3:    "Mil-Spec",
    4:    "Restricted",
    5:    "Classified",
    6:    "Covert",
}

if "__main__"==__name__:
    data=dict()
    url="https://csgostash.com"
    page=requests.get(url)
    soup=BeautifulSoup(page.content,"html.parser")
    collectionList=None
    for x in soup.find_all("li",class_="dropdown"):
        if x.find("a",class_="dropdown-toggle").text=="Collections":
            collectionList = x

    for x in collectionList.find("ul",class_="dropdown-menu").find_all("li"):
        attr=x.find("a")
        if attr!=None:
            # print(attr.text)
            # print(attr["href"])
            data[attr.text]=dict()
            for i in range(1,7):
                data[attr.text][i]=list()
            page2=requests.get(attr["href"])
            soup2=BeautifulSoup(page2.content,"html.parser")
            for div in soup2.find_all("div",class_="col-lg-4 col-md-6 col-widen text-center"):
                if div.find("h3")!=None:
                    data[attr.text][list(RARITY.keys())[list(RARITY.values()).index(div.find("p",class_="nomargin").text.strip().split(" ")[0])]].append(div.find("h3").text)
    
    for x in data["2021 Train"].keys():
        print(x)
        print(type(x))
    # Writing to sample.json
    with open("csgoweaponlist.json", "w") as outfile:
        outfile.write(json.dumps(data, indent = 4))             
