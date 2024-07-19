import logging
import os
from typing import NewType

from hippodrome import message

from pymongo import MongoClient
from pydantic import BaseModel


# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DO_DATA_COLLECTION = bool(int(os.environ.get("DO_DATA_COLLECTION", 0)))
JSONL_DATA_DIR = os.environ.get("JSONL_DATA_DIR")

MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING")
DB_NAME = os.environ.get("MONGODB_NAME")

Model = NewType("Model", BaseModel)


def save(log_object: Model):
    # If data collection is disabled, return early
    if not DO_DATA_COLLECTION:
        logger.info("Not Collecting Data")
        return

    collection = get_collection(log_object)

    # Multiple data collection modes can be enabled at once

    # JSONL mode, saves data to a local JSONL file
    if JSONL_DATA_DIR:
        logger.info(f"Saving to JSONL file: {collection}.jsonl in {JSONL_DATA_DIR}")
        data_dir = JSONL_DATA_DIR
        log_file = os.path.join(data_dir, f"{collection}.jsonl")

        with open(log_file, "a+") as f:
            f.write(log_object.model_dump_json() + "\n")

    # MongoDB mode, saves data to a MongoDB database
    if MONGODB_CONNECTION_STRING:
        client = MongoClient(MONGODB_CONNECTION_STRING)
        db = client[DB_NAME]
        db[collection].insert_one(log_object.model_dump())


def get_collection(log_object: Model) -> str:
    from hippodrome import Game, Player

    if isinstance(log_object, message.AgentMessage):
        collection = "messages"
    if isinstance(log_object, message.Message):
        collection = "messages"
    elif isinstance(log_object, Player):
        collection = "players"
    elif isinstance(log_object, Game):
        collection = "games"
    else:
        raise ValueError(f"Unknown log object type: {type(log_object)}")

    return collection
