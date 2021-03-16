from src.main_db import MainDB
from src.aws_helper import AWSHelper
from dotenv import load_dotenv
from dataclasses import dataclass

BATCH_SIZE = 10
OLD_PATH_PREFIX = "images"
NEW_PATH_PREFIX = "avatar"
@dataclass
class Job():
    job_id: int
    old_key: str
    new_key: str

def generate_batch_from_raw(jobs_raw):
    batch = []
    for job in jobs_raw:
        batch.append(Job(
            job[0],
            job[1],
            job[1].replace(
                OLD_PATH_PREFIX,
                NEW_PATH_PREFIX
            )
        ))
    return batch

def get_batch_from_id(_id=0):
    jobs_raw = MainDB().get_batch_from_id_with_prefix(
        batch_size=BATCH_SIZE,
        _id=_id,
        prefix=OLD_PATH_PREFIX
    )
    batch = generate_batch_from_raw(jobs_raw)
    print(batch)
    return batch

def migrate_batch(batch):
    helper = AWSHelper()
    for job in batch:
        source_key = job.old_key
        destination_key = job.new_key
        print("Copy item: {item}".format(item=job))
        helper.copy_key(source_key, destination_key)

def update_path(batch):
    db = MainDB()
    print("Transaction updating {items} rows".format(items=len(batch)))
    for job in batch:
        db.update_path(
            _id=job.job_id,
            path=job.new_key
        )

def delete_batch(batch):
    helper = AWSHelper()
    for job in batch:
        print("Testing item {item}".format(item=job))
        helper.check_key(job.new_key)
        print("Deleting item {item}".format(item=job))
        helper.delete_key(job.old_key)

def run():
    last_id = 0
    while True:
        batch = get_batch_from_id(last_id)
        # If batch size is larger than 0
        if len(batch) == 0:
            break
        last_id = batch[-1].job_id
        migrate_batch(batch)
        update_path(batch)
        delete_batch(batch)


if __name__ == '__main__':
    load_dotenv()
    run()
