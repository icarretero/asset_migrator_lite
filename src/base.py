from src.main_db import (
    MainDBConnectionError,
    MainDBException,
)
from src.aws_helper import (
    AWSHelperNotFoundError,
    AWSHelperConnectionError,
    AWSHelperException
)
from dataclasses import dataclass

class CriticalError(Exception):
    pass


@dataclass
class Job():
    job_id: int
    old_key: str
    new_key: str


def handle_aws_exceptions(method):
    def wrapper(*v, **kw):
        try:
            return method(*v, **kw)
        except AWSHelperConnectionError:
            raise CriticalError("Connection Error with AWS. Review credentials")
        except AWSHelperException:
            raise CriticalError("Error in AWS Helper")
    return wrapper


def handle_main_db_exceptions(method):
    def wrapper(*v, **kw):
        try:
            return method(*v, **kw)
        except MainDBConnectionError as e:
            raise e
            #raise CriticalError("Connection Error with DB. Review credentials")
        except MainDBException:
            raise CriticalError("Error in DB connector")
    return wrapper
