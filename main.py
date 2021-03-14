from src.main_db import MainDB
from dotenv import load_dotenv

BATCH_SIZE = 10
OLD_PATH_PREFIX = "images"
NEW_PATH_PREFIX = "avatar"

def get_batch_from_id(_id=0):
    batch = MainDB().get_batch_from_id_with_prefix(
        batch_size=BATCH_SIZE,
        _id=_id,
        prefix=OLD_PATH_PREFIX
    )
    print(batch)
    return batch

def copy_batch(batch):
    for migration in batch:
        print("Copy item: {item}".format(item=migration))

def update_path(batch):
    print("Transaction updating {items} rows".format(items=len(batch)))

def delete_batch(batch):
    for migration in batch:
        print("Testing item {item}".format(item=migration))
        print("Deleting item {item}".format(item=migration))

def run():
    # Get first batch
    batch = get_batch_from_id()
    # If batch size is larger than 0
    if len(batch) > 0:
        copy_batch(batch)
        update_path(batch)
        delete_batch(batch)
    # next batch


if __name__ == '__main__':
    load_dotenv()
    run()
