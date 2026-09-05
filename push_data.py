import os
import sys
import json
import dns.resolver

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Use Google DNS for MongoDB SRV lookup
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8", "8.8.4.4"]

# Get MongoDB URL from .env
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL is not found in .env file")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)

            data.reset_index(drop=True, inplace=True)

            records = list(
                json.loads(data.T.to_json()).values()
            )

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            # Select database
            self.database = self.mongo_client[self.database]

            # Select collection
            self.collection = self.database[self.collection]

            # Insert records
            self.collection.insert_many(self.records)

            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    FILE_PATH = "Network_Data/phisingData.csv"

    DATABASE = "MUDASIRAI"

    Collection = "NetworkData"

    networkobj = NetworkDataExtract()

    records = networkobj.csv_to_json_convertor(
        file_path=FILE_PATH
    )

    print(f"Total records read from CSV: {len(records)}")

    no_of_records = networkobj.insert_data_mongodb(
        records,
        DATABASE,
        Collection
    )

    print(f"Total records inserted into MongoDB: {no_of_records}")