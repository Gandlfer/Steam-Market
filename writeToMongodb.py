import pymongo
import json
from csgoitem import func

if __name__=="__main__":
    func()
    myclient= pymongo.MongoClient("mongodb://192.168.0.252:27017/")
    mydb=myclient["csgo"]
    with open("csgoweaponlist.json") as f:
        data=json.load(f)
    
    if "csgo-skins-collection" not in mydb.list_collection_names():
        col=mydb["csgo-skins-collection"]
        for key in data.keys():
            col.insert_one({"name": key, "skins":data[key]})

    