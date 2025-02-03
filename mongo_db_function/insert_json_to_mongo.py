import pymongo
import json

with open('member.json','r') as file:
    data = json.load(file)


def insert_member():

    uri = 'localhost:27017'
    client = pymongo.MongoClient(uri)

    try:
        databases = client['gym_system_db']
        collection = databases['member_list']

        # we create unique index for our member
        collection.create_index([('id_card', pymongo.ASCENDING)], unique=True)

        result = collection.insert_many(data)
        print(f'{len(result.inserted_ids)} documents were inserted')

    except pymongo.errors.DuplicateKeyError:
        print("A document with the same id_card already exists.")

    finally:
        client.close()

insert_member()