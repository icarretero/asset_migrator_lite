# Asset Migrator Lite

This is a lightweight version of the Asset Migrator. A second attempt to do a simpler and less complex solution to the challenge.

## Process

The steps I ~~will follow~~ have followed are:

1. Creation of the happy path flow without iteration [DONE]
1. Create the local environment for development [DONE]
1. Implementation of methods to do real stuff [DONE]
1. Create iteration loop for all migrations [DONE]
1. Implement basic error handling [DONE]
1. Implement basic logging [DONE]
1. Save current status and resume operations [WON'T DO]
1. Config as files/vars [WON'T DO]
1. Conteinarization [DONE]
1. Advanced error handling [WON'T DO]
1. Advanced logging [WON'T DO]
1. README [DONE]

## What things have not been done

There is a huge "elephant in the room" missing in the process which is testing. I know it is something critical and something I trust a lot. However, it would have been longer hours for this challenge so I decided to exclude it of the scope.

### Save current status and resume operations

The current script can stop and resume in the latest batch it has been migrated as it queries the DB filtering results. However, had I had more time I would have implemented a way to persist the `last_id` being updated in the operations.

A simple way could be a local file and mount it with a volume in Docker and passing its path with an env-var. More resilient ways could be using another DB.

### Config as files/vars

I have tried to keep secrets (keys) and basic config for the DB as env-vars. However, further configuration such as the bucket names, batch size and so on have been kept as constants due to time constraints. I would have loved to have a centralized config declaring all settings and some tuning (sucha as doing the check of the migrated keys or not) as flags or vars. I could have considered moved all of them to env-vars as a more 12-factor approach.

### Advanced error handling

I have created a basic structure of Exception handling and decorators and only tested and considered the most usual and basic cases but, as there are no tests, I would have loved to create a more robust error handling strategy.

### Advanced logging
Similar as the error handling. I have only created the basic logging entries as info and some warnings/errors for errors. However, there is no debug level at all.

## OK, how do I run it?

You can run it locally or use Docker. I don't have a DockerHub to upload it now but maybe in a future I will create it and push it (or to any other registry)

In both cases the program expects, at least, the following variables are defined where it runs:
- MYSQL_PWD: The password to the user to be used
- AWS_ACCESS_KEY_ID: The AWS access key with access to the buckets
- AWS_SECRET_ACCESS_KEY: The AWS secret access key

Other env-vars that can be defined:
- MYSQL_USER: The user to be used in MariaDB. Default is `root`
- MYSQL_HOST: The host of the MariaDB instance. Default is `localhost`
- MYSQL_PORT: The port of the MariaDB instance. Default `3306`

Settings as env-vars (see previous point about config):
- MYSQL_DB: The DB name where the table of items is located. Default is `assets`.
- MYSQL_TABLE_NAME: The table name where the items are located. Default is `assets`.
- MYSQL_ID_KEY: The table key with the id of the items. Default is `entry_id`.
- MYSQL_PATH_KEY: The table key with the path of the items. Default is `path_id`.
- AWS_OLD_BUCKET: The name of the s3 bucket where the items have to be migrated from. Default is `asset-migrator-legacy-s3`
- AWS_NEW_BUCKET: The name of the s3 bucket where the items have to be migrated to. Default is `asset-migrator-production-s3`
- OLD_PATH_PREFIX: The prefix used in the path of the s3 bucket key in source. Default is `images`
- NEW_PATH_PREFIX: The prefix used in the path of the s3 bucket key in destination. Default is `avatar`

### I wan't Docker fun
That's an easy one. First of all, complete the `.env.local` file with all of your env variables. There is only one thing to consider. If the MariaDB instance is running in your localhost:

If it is not, remember to define `MYSQL_HOST` in the file and just execute `make run`

If it is, do not define `MYSQL_HOST` in the file and execute `make run-local`

### I prefer to run it without Docker

First you might need to create a virtualenv with Python. I have used Python 3.8. Then uncomment the line 2 of the `requirements.txt` file and execute `pip install -r requirements.txt`.

To create the environment file copy the `.env.local` as `.env` in the same folder. Complete the proper values and uncomment the lines 16 and 174 in `main.py`.

Finally, execute `python main.py`

## How did you tested this?

I created my own AWS project and 2 buckets. Then I span up a MariaDB in a local container. To fill ub the DB and the S3 buckets with files I have used the script I created in the [other repository](https://github.com/icarretero/asset_migrator/tree/main/local/S3%2BDB)

## And my extra ball?

The MariaDB user needs to have connection permission to the Database and `SELECT` and `UPDATE` permisions to the table where the items are.

The AWS user must be able to perform a copy, a head and a delete operation:
- copy: `s3:GetObject` in source and `s3:PutObject` in destination
- head: `s3:GetObject`, `s3:ListBucket` (to get the 404 response according to docu)
- delete: `s3:DeleteObject` in destination
