import os
SECRET_KEY = 'Cloud2019'
DATA_BACKEND = 'cloudsql'
PROJECT_ID = 's3488797-cc2019'

CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'Cloud2019'
CLOUDSQL_DATABASE = 'spotify_project'
CLOUDSQL_CONNECTION_NAME = 's3488797-cc2019:australia-southeast1:sql-storage'

LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://root:Cloud2019@127.0.0.1:3306/spotify_project').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

# When running on App Engine a unix socket is used to connect to the cloudsql
# instance.
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://root:Cloud2019@localhost/spotify_project'
    '?unix_socket=/cloudsql/s3488797-cc2019:australia-southeast1:sql-storage').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('OS'):
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
