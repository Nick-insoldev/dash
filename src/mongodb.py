from pymongo import MongoClient
import os


import json

server = MongoClient("mongodb://192.168.98.15:27017/")
db = server["Insoldev"]
collection = db["Alarm"]


def find(database, var, value, search_for="_id"):
    collection = db[database]
    test = collection.find({var: value})
    for x in test:
        return x[search_for]


def vind_regelaars(klant):
    collection = db["Klanten"]
    test = collection.find_one("_id",klant)
    return test
    # for x in test:
    #     return x["regelaars"]





def add_one(database, _id, var, value):
    collection = db[database]
    collection.insert_one({"_id": _id, var: value})


def update_(database, _id, var, value):
    collection = db[database]
    collection.update_one({"_id": _id}, {"$set": {var: value}})



def vind_by_subId(database, subId, klant=None, user=None, ):
    if klant:
        a = (find(database, "naam", klant, "regelaars"))
    else:
        a = (find("_id", user, "regelaars"))
    try:
        return a[subId]
    except:
        return None


# a = vind_by_subId("co2-1", "calis-22")
# print(a)
# collection.delete_one({"_id":0})
# collection.insert_one({"_id":"calis-15/aht/adr1","name":"bak-1"})
# collection.update_one({"_id": "calis-15/aht/adr1"}, {"$set": {"name": "Bak-1","alarmgrens":-22}})
# collection.insert_one({"_id": db, "name": naam})

# a = (find("naam", "Noyez Snacks", "ip"))




def standaar_email(vieuw):
    collection = db["Klanten"]
    for x in range(50):
        # try:
        id = "calis-" + str(x)
        print(id)
        # try:
        #
        #     find("Klanten", "_id", id, search_for="Mail_to")
        # except:
        try:
            test= find("Klanten", "_id", id, search_for="naam")
            klant = find("Klanten", "_id", id, search_for="Klant")

        except:
            continue

        if test:
            if klant=="Bonap":
                to=["wachtdienstexpansie@meatandmore.be"]
            elif klant=="Calis" or "calis":
                to = ["xweb@calis.be"]
            else:
                to= ["alerts@insoldev.be"]

            mail_to = ""
            for a in to:
                mail_to = mail_to + a + ";"
            mail_to = mail_to[:-1]
            mail_list = to
            mail_list.append("alerts@insoldev.be")
            collection.update_one({"_id": id}, {"$set": {"Mail_to": mail_to, "Mail_list": mail_list}})


if __name__ == "__main__":
    print("mongo loaded")
