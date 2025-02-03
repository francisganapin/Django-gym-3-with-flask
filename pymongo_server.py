import pymongo


class ConnectionMongoDB():
    def __init__(self,uri ='localhost:27017',db_name='gym_system_db'):
        '''connect to mongodb client'''
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[db_name]
        uri = 'localhost:27017'
    

    def get_collection(self,collection_name):
        '''retrieve our collection'''
        return self.database[collection_name]
    
    def close(self):
        '''close the mongo db'''
        self.client.close()
        