import boto3
import os
import time


def handler(event, context):
    bucket_name = 'bluetoothlowenergy.co'
    bucket_filename = 'index.htm'
    temp_filename = '/tmp/{}'.format(str(time.time()))
    
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket_name, bucket_filename, temp_filename)

    with open(temp_filename, 'rb') as file:
        contents = file.read()
    print(contents)
    
    os.remove(temp_filename)
    
    '''
	try:
		outfile = s3.put_object(Bucket=outbucket,Key=outkey,Body=tmp)
	except Exception as e:
		print(e)
		print(‘Error putting object {} from bucket {} Body {}. Make sure they exist and your bucket is in the same region as this function.’.format(outkey, outbucket,”tmp.txt”))
		raise e
	'''