import os

mysql = {
	'server': os.getenv('MYSQL_SERVER'),
	'username': os.getenv('MYSQL_USER'),
	'password': os.getenv('MYSQL_PASSWORD'),
	'schema': os.getenv('MYSQL_SCHEMA')
}
s3 = {
	'bucket_name': os.getenv('S3_BUCKET_NAME'),
	'bucket_filename': os.getenv('S3_BUCKET_PATH')
}