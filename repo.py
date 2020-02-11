from __future__ import division
from db_connectivity import *
import pymongo

class CurrencyRepo(object):
    """
    CurrencyRepo is used to perform CRUD operations on currencies master table
    """
    db_inst = None

    def __init__(self):
        mongo = MongoCon()
        db_cli = mongo.get_connection()
        self.db_inst = db_cli.currencies

    def init_db(self):
        mongo = MongoCon()
        db_cli = mongo.get_connection()
        self.db_inst = db_cli.currencies
        return

    def find_record(self, query):
        return self.db_inst.find(query)

    def find_one_record(self, query):
        return self.db_inst.find_one(query)

    def find_and_update(self, query, update):
        self.db_inst.update_one(query, update)

    def find_record_with_projection(self, query, projection):
        return self.db_inst.find(query, projection)

    def insert_record(self, query, insert_doc):
        return self.db_inst.update_one(query, insert_doc, upsert=True)

'''
The StocksRepo performs all database operations on stocks collection.
'''


class StocksRepo(object):

    db_inst = None

    def __init__(self):
        mongo = MongoCon()
        db_cli = mongo.get_connection()
        self.db_inst = db_cli.stocks

    def init_db(self):
        mongo = MongoCon()
        db_cli = mongo.get_connection()
        self.db_inst = db_cli.stocks
        return

    def find_record(self, query):
        return self.db_inst.find(query)

    def find_one_record(self, query):
        return self.db_inst.find_one(query)

    def find_and_update(self, query, update):
        self.db_inst.update_one(query, update)

    def find_record_with_projection(self, query, projection):
        return self.db_inst.find(query, projection)

    def insert_record(self, query, insert_doc):
        return self.db_inst.update_one(query, insert_doc, upsert=True)


'''
The OhlcRepo performs all database operations on a given stock's collection.
'''


class OhlcRepo(object):

    db_inst = None
    db_cli = None

    def __init__(self):
        mongo = MongoCon()
        self.db_cli = mongo.get_connection()

    def drop_collection(self, collection_name):
        self.db_inst = self.db_cli[collection_name]
        return self.db_inst.drop()

    def insert_record(self, collection_name, query, insert_doc):
        self.db_inst = self.db_cli[collection_name]
        return self.db_inst.update_one(query, insert_doc, upsert=True)

    def insert_new_record(self, collection_name, insert_doc):
        self.db_inst = self.db_cli[collection_name]
        return self.db_inst.insert_one(insert_doc)

    def insert_many_records(self, collection_name, insert_doc):
        self.db_inst = self.db_cli[collection_name]
        return self.db_inst.insert_many(insert_doc)

    def find_records(self, collection_name):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find())

    def find_records_with_query(self, collection_name, query):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query))

    def find_records_with_limit(self, collection_name, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find().sort('timestamp', pymongo.DESCENDING).limit(limit))

    def find_record_with_limit(self, collection_name, query, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query).limit(limit))

    def find_records_with_sort(self, collection_name, query):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query).sort('timestamp', pymongo.DESCENDING))

    def find_record_with_projection_limit(self, collection_name, query, projection, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query, projection).sort('timestamp', pymongo.DESCENDING).limit(limit))

    def find_record_with_projection(self, collection_name, query, projection):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query, projection))

    def find_record_with_projection_sort(self, collection_name, query, projection):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query, projection).sort('timestamp', pymongo.DESCENDING))

    def find_record_with_sort_limit(self, collection_name, query, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query).sort('timestamp', pymongo.ASCENDING).limit(limit))

    def find_record_with_sort_limit_projection(self, collection_name, query, projection, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query, projection).sort('timestamp', pymongo.ASCENDING).limit(limit))

    def aggregate_with_projection_sort(self, collection_name, pipeline):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.aggregate(pipeline))

    def update_query(self, collection_name, query_doc, insert_doc):
        self.db_inst = self.db_cli[collection_name]
        self.db_inst.update_one(query_doc, {'$set': insert_doc})


'''
The Config performs all database operations on config collection.
'''


class Config(object):

    db_inst = None

    def __init__(self):
        mongo = MongoCon()
        db_cli = mongo.get_connection()
        self.db_inst = db_cli.config

    def init_db(self):
        mongo = MongoCon()
        db_cli = mongo.get_connection()
        self.db_inst = db_cli.config
        return

    def find_record_with_projection(self, query, projection):
        return self.db_inst.find(query, projection)

    def update_record(self, query, insert_doc):
        return self.db_inst.update_one(query, insert_doc, upsert=False)
