import logging

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

# Used for local development but not in Docker
#from dotenv import load_dotenv

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

BATCH_SIZE = 10
OLD_PATH_PREFIX = "images"
NEW_PATH_PREFIX = "avatar"



def generate_batch_from_raw(batch_raw):
    batch = []
    logging.info("Genetaring batch of Jobs")
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
    logging.info(
        "Getting batch of {batch_size} starting in id: {min_id}".format(
            batch_size=BATCH_SIZE,
            min_id=min_id
        )
    )
    jobs_raw = MainDB().get_batch_from_id_with_prefix(
        batch_size=BATCH_SIZE,
        _id=min_id,
        prefix=OLD_PATH_PREFIX
    )
    return jobs_raw


def get_batch_from_id(min_id=0):
    batch_raw = get_batch_from_database(min_id)
    batch = generate_batch_from_raw(batch_raw)
    logging.info(
        "Generated batch of {items} jobs".format(
            items=len(batch)
        )
    )
    return batch


@handle_aws_exceptions
def migrate_batch(batch):
    helper = AWSHelper()
    logging.info(
        "Migrating files for batch of {items} jobs".format(
            items=len(batch)
        )
    )
    for job in batch:
        source_key = job.old_key
        destination_key = job.new_key
        print("Copy item: {item}".format(item=job))
        try:
            helper.copy_key(source_key, destination_key)
        except AWSHelperNotFoundError:
            logging.warning((
                "File not found in source. "
                "Could not be migrated: {job_path}").format(
                    job_path=job.old_key
                )
            )
            batch.remove(job)
    logging.info(
        "Migrated files for {items} jobs".format(items=len(batch))
    )


@handle_aws_exceptions
def check_keys(batch):
    helper = AWSHelper()
    logging.info(
        "Check keys on destination for {items} jobs".format(items=len(batch))
    )
    for job in batch:
        try:
            helper.check_key(job.new_key)
        except AWSHelperNotFoundError:
            logging.warning((
                "File not found in destination. "
                "Dropping from batch: {job_path}").format(
                    job_path=job.new_key
                )
            )
            batch.remove(job)
    logging.info(
        "Checked keys for {items} jobs".format(items=len(batch))
    )


@handle_main_db_exceptions
def update_path(batch):
    db = MainDB()
    logging.info(
        "Updating path of batch of {items} jobs".format(
            items=len(batch)
        )
    )
    for job in batch:
        db.update_path(
            _id=job.job_id,
            path=job.new_key
        )
    logging.info(
        "Updated path for {items} jobs".format(items=len(batch))
    )


@handle_aws_exceptions
def delete_batch(batch):
    helper = AWSHelper()
    logging.info(
        "Deleting files for batch of {items} jobs".format(
            items=len(batch)
        )
    )
    for job in batch:
        try:
            helper.delete_key(job.old_key)
        except AWSHelperNotFoundError:
            logging.warning(
                "File not found. Could not be deleted: {job_path}".format(
                    job_path=job.new_key
                )
            )
            batch.remove(job)
    logging.info(
        "Deleted files for {items} jobs".format(items=len(batch))
    )


def run():
    last_id = 0
    while True:
        batch = get_batch_from_id(last_id)
        # If batch size is larger than 0
        if len(batch) == 0:
            logging.info("Received empty batch. No more items to migrate")
            break
        last_id = batch[-1].job_id
        migrate_batch(batch)
        check_keys(batch)
        update_path(batch)
        delete_batch(batch)


if __name__ == '__main__':
    # load_dotenv()
    logging.info("Starting migration!")
    try:
        run()
    except CriticalError as e:
        logging.error(e)
        exit(1)
    logging.info("Finished migration!")
