import logging
from os import environ
from pymongo import MongoClient


db_config = {
    'PASS': environ.get('PASS', ''),
    'DOMAIN': environ.get('DOMAIN', ''),
    'HASH_SIZE': environ.get('HASH_SIZE', ''),
    'RECORDS': environ.get('RECORDS', ''),
}


def generate_random_hash(numb: int = 1) -> str:
    import random
    import string
    import hashlib
    if numb == 1:
        return hashlib.sha256(''.join(random.choices(string.ascii_letters + string.digits, k=64)).encode()).hexdigest()
    else:
        return ''.join(
            [hashlib.sha256(''.join(random.choices(string.ascii_letters + string.digits, k=64)).encode()).hexdigest()
             for _ in range(numb)])


def check_mongo_connection():
    try:
        mongo_client = MongoClient(
            f'mongodb://root:{db_config["PASS"]}@{db_config["DOMAIN"]}:27017/',
            serverSelectionTimeoutMS=5000)
        mongo_client.server_info()
        logging.info("Successfully connected to MongoDB")
        return True
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {str(e)}")
        return False


def mongo_write_hash(size: int = 100) -> bool:
    if check_mongo_connection():
        client = MongoClient(
            f'mongodb://root:{db_config["PASS"]}@{db_config["DOMAIN"]}:27017/',
            serverSelectionTimeoutMS=5000)
        db = client.db
        for _ in range(size):
            db.hashes.insert_one({'hash': generate_random_hash(db_config['HASH_SIZE'])})
        return True
    return False