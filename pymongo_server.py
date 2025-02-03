import pymongo


class ConnectionMongoDB():
    def __init__(self,uri ='localhost:27017',db_name='gym_system_db'):
        '''connect to mongodb client'''
        try:

            self.client = pymongo.MongoClient(uri)
            self.database = self.client[db_name]
            self.db_name = db_name
            uri = 'localhost:27017'
            print(f'connected to {uri} mongodb')
        except:
            print('sorry cant connect to mongoDB')


    def get_collection(self,collection_name):
        '''retrieve our collection'''
        return self.database[collection_name]
    
    def close(self):
        '''close the mongo db'''
        self.client.close()
    
    def check_exist(self):
        '''print if our database exist'''
        dblist = self.client.list_database_names()
        if self.db_name in dblist:
            print('database is exist')
        else:
            print('database was not exist')


conn = ConnectionMongoDB()
conn.check_exist()