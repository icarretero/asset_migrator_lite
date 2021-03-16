
from src.base import (
    Job,
    CriticalError,
    handle_aws_exceptions,
    handle_main_db_exceptions
)
from src.main_db import MainDB
from src.aws_helper import (
    AWSHelper,
    AWSHelperNotFoundError
)

from dotenv import load_dotenv

BATCH_SIZE = 10
OLD_PATH_PREFIX = "images"
NEW_PATH_PREFIX = "avatar"



def generate_batch_from_raw(batch_raw):
    batch = []
    for row in batch_raw:
        batch.append(Job(
            row[0],
            row[1],
            row[1].replace(
                OLD_PATH_PREFIX,
                NEW_PATH_PREFIX
            )
        ))
    return batch


@handle_main_db_exceptions
def get_batch_from_database(min_id):
    jobs_raw = MainDB().get_batch_from_id_with_prefix(
        batch_size=BATCH_SIZE,
        _id=min_id,
        prefix=OLD_PATH_PREFIX
    )
    return jobs_raw


def get_batch_from_id(min_id=0):
    batch_raw = get_batch_from_database(min_id)
    batch = generate_batch_from_raw(batch_raw)
    print(batch)
    return batch


@handle_aws_exceptions
def migrate_batch(batch):
    helper = AWSHelper()
    for job in batch:
        source_key = job.old_key
        destination_key = job.new_key
        print("Copy item: {item}".format(item=job))
        try:
            helper.copy_key(source_key, destination_key)
        except AWSHelperNotFoundError:
            batch.remove(job)


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
        try:
            helper.check_key(job.new_key)
        except AWSHelperNotFoundError:
            batch.remove(job)
        print("Deleting item {item}".format(item=job))
        try:
            helper.delete_key(job.old_key)
        except AWSHelperNotFoundError:
            batch.remove(job)


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
    try:
        run()
    except CriticalError as e:
        print(e)
        exit(1)
