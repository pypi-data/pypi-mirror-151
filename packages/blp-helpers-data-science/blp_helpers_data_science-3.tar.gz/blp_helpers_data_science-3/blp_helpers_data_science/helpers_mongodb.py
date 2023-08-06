import os
from pymongo import MongoClient
import yaml


def get_mongo_db_collection(collection_name, path_config_file, environment):
    if not environment:
        environment = os.environ['ENVIRONMENT']
    with open(path_config_file, "r") as stream:
        try:
            db_names_env_mapping = yaml.safe_load(stream)
            db_name = db_names_env_mapping.get(environment)
            client = MongoClient("mongodb+srv://{}:{}@{}.mongodb.net/{}".format(
                os.environ['RESEARCHLY_MONGODB_USERNAME']
                , os.environ['RESEARCHLY_MONGODB_PASSWORD']
                , os.environ['RESEARCHLY_MONGODB_CLUSTER']
                , db_name
            ))
            return client[db_name][collection_name]
        except yaml.YAMLError as exc:
            print(exc)