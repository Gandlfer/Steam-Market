from os import stat
import requests
import json
import time

MAX_VALUE=99999999
WEAR=["Battle-Scarred","Well-Worn","Field-Tested","Minimal Wear","Factory New"]
RARITY={
    1:    "Consumer" ,
    2:    "Industrial",
    3:    "Mil-Spec",
    4:    "Restricted",
    5:    "Classified",
    6:    "Covert",
}

# Sample URL
# https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=StatTrak%E2%84%A2%20P250%20%7C%20Steel%20Disruption%20%28Factory%20New%29
# 
STATTRAK="StatTrak%E2%84%A2%20"
#BASEURL="https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name="
BASEURL="https://csgobackpack.net/api/GetItemPrice/?currency=USD&id="

def makeUrl(item,stat,w):
    split=item.split(" | ")
    requestUrl=BASEURL
    if stat:
        requestUrl=requestUrl+STATTRAK
        
    requestUrl=requestUrl+split[0].replace(" ","%20")+"%20%7C%20"+split[1].replace(" ","%20")+"%20%28"+w.replace(" ","%20")+"%29"
        
    return requestUrl

def find_price(url):
    item_Response=requests.get(url).json()
    #time.sleep(3)

    #print(type(item_Response["success"]))
    try:
        if item_Response["success"]=="false":
            #print(url)
            raise Exception

        price=item_Response["average_price"]

    except KeyError:

        try:   
            price=item_Response["median_price"]
        except(KeyError):
            return -1

    except(Exception):
        return -1

    return float(price)

def loops(data,stat):
    visited=list()
    for r in RARITY:
        #print(r)
        if(r!=6):
            for w in WEAR:
                for collectionKey in data:
                    #print("Head Collection {}".format(collectionKey))
                    visited.append(collectionKey)
                    if len(data[collectionKey][str(r)])==0 or len(data[collectionKey][str(r+1)])==0:
                        continue
                    
                    firstItem=None
                    firstItemMin=MAX_VALUE
                    firstCollectionMin=MAX_VALUE

                    #print("Going in Collection {}".format(collectionKey))
                    #find lowest price item in the collection
                    for item in data[collectionKey][str(r)]:
                        #print("{} from {}".format(item,collectionKey))
                        itemPrice=find_price(makeUrl(item,stat,w))
                        #print("Request body:\n{}".format(makeUrl(item,False,w)))
                        #item_Response=requests.get(makeUrl(item,False,w)).json()                        
                        if itemPrice==-1:
                            continue
                        
                        # if (len(data[collectionKey][str(r)])==1):
                        #     firstItemMin=itemPrice
                        #     firstItem=item

                        elif itemPrice<firstItemMin:
                            firstItemMin=itemPrice
                            firstItem=item

                    #find upgraded lowest price item in the collection 
                    for item in data[collectionKey][str(r+1)]:
                        itemPrice=find_price(makeUrl(item,stat,w))
                        #print("Request body:\n{}".format(makeUrl(item,False,w)))
                        #item_Response=requests.get(makeUrl(item,False,w)).json()                        
                        if itemPrice==-1:
                            continue

                        itemPrice=itemPrice/1.15
                        if itemPrice<firstCollectionMin:
                            firstCollectionMin=itemPrice
            
                    #print(firstCollectionMin)
                    #print("Item 1\nName: {} \tPrice: {}".format(firstItem,firstItemMin))

                    for collectionKey2 in data:
                        if collectionKey2 not in visited:
                            #print("Head2 Collection {}".format(collectionKey2))
                            if len(data[collectionKey2][str(r)])==0 or len(data[collectionKey2][str(r+1)])==0:
                                continue
                            
                            secondItem=None
                            secondItemMin=MAX_VALUE
                            secondCollectionMin=MAX_VALUE

                            #print("Going in 2 Collection {}".format(collectionKey2))
                            #find lowest price item in the collection
                            for item in data[collectionKey2][str(r)]:

                                itemPrice=find_price(makeUrl(item,stat,w))
                  
                                if itemPrice==-1:
                                    continue

                                if itemPrice<secondItemMin:
                                    secondItemMin=itemPrice
                                    secondItem=item

                            #find upgraded lowest price item in the collection 
                            for item in data[collectionKey2][str(r+1)]:
                                itemPrice=find_price(makeUrl(item,stat,w))
                  
                                if itemPrice==-1:
                                    continue

                                itemPrice=itemPrice/1.15
                                if itemPrice<secondCollectionMin:
                                    secondCollectionMin=itemPrice

                            #print(secondCollectionMin)
                            x=9
                            y=1
                            while True:
                                total=(firstItemMin*x + secondItemMin*y)
                                if(total<=firstCollectionMin and total<=secondCollectionMin):
                                    print("Total: {}".format(round(total,2)))
                                    print("{} x Item 1\nName: {} \tPrice: {}".format(x,firstItem,firstItemMin))
                                    print("{} x Item 2\nName: {} \tPrice: {}".format(y,secondItem,secondItemMin)) 
                                    print("Min Profit={} or {}".format(firstCollectionMin,secondCollectionMin))
                                if x==1:
                                    break
                                x=x-1
                                y=y+1
                            
                            #print("Item 1\nName: {} \tPrice: {}".format(firstItem,firstItemMin))
                            #print("Item 2\nName: {} \tPrice: {}".format(secondItem,secondItemMin)) 

                            #print("Next Collection")

if "__main__"==__name__:

    #-------------------
    #Read from json
    file=open("csgoweaponlist.json")
    data = json.load(file)
    file.close()
    #-------------------

    loops(data,False)
    loops(data,True)