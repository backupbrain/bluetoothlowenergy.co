# -*- coding: utf-8 -*-
'''
@author Tony Gaitatzis
@organization ReadWrite
@licence MIT
@contact backupbrain@gmail.com
'''
import json
import os
import traceback
from urllib.parse import quote
import requests
import time

import pymysql
from databaseobject.DatabaseObject import DatabaseObject
from httpserver.HttpServer import HttpServer
from LambdaLog import LambdaLog
from settings import settings

import boto3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(source_email, recipient_emails, message_data):
    ses_client = boto3.client('ses')
    bounceResponse = ses_client.send_raw_email(
        Source=source_email,
        Destinations=recipient_emails,
        RawMessage=message_data
    )
    bucket_name = 'bluetoothlowenergy.co'
    bucket_filename = 'index.htm'


def get_download_contents(bucket_name, filename_path):
    temp_filename = '/tmp/{}'.format(str(time.time()))
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket_name, filename_path, temp_filename)
    with open(temp_filename, 'rb') as file:
        contents = file.read()
    os.remove(temp_filename)
    return contents


def create_download_link(bucket, filename_path, file_contents):
    s3_client = boto3.client('s3')
    try:
        outfile = s3_client.put_object(
            Bucket=bucket,
            Key=filename_path,
            Body=file_contents
        )
        return temp_filename
    except Exception as e:
        print(e)
        print('Error putting object {} from bucket {}. '.format(
            filename_path, 
            bucket 
        ) + 'Make sure they exist and your bucket is in the same region' + \
        ' as this function.')
        raise e


def lambda_handler(event, context):
    is_logging_enabled = False
    if os.getenv('IS_LOGGING_ENABLED') == '1':
        is_logging_enabled = True

    http_server = HttpServer(event)
    #print(json.dumps(event, indent=4))

    print(json.dumps(settings.mysql, indent=4))
    print(json.dumps(settings.s3, indent=4))

    try:
        database = pymysql.connect(host=settings.mysql['server'],
                                user=settings.mysql['username'],
                                password=settings.mysql['password'],
                                db=settings.mysql['schema'],
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)
    except:
        message = "Error connecting to database"
        headers = http_server.get_headers()
        headers['response'] = message
        print(message)

        # We don't push an error here, because 
        # we want the system to fail gracefully by forwarding the user
        # even if there's a problem connecting to the database
        return http_server.respond_error(message) # Shortcut to forwarding

    database_object = DatabaseObject(database)
    
    if is_logging_enabled:
        lambda_log = LambdaLog(database_object)
        if 'resource' in event:
            lambda_log.application_id = event['resource']
        lambda_log.endpoint_url = http_server.get_url()
        lambda_log.url_query = json.dumps(
            http_server.get_query_parameters(),
            indent=0
        )
        lambda_log.ip_address = http_server.get_ip()
        lambda_log.forwarding_ip_addresses = http_server.get_forwarded_for()
        lambda_log.cookie_value = http_server.get_cookie_string()
        lambda_log.user_agent = http_server.get_user_agent()
        lambda_log.http_method = http_server.get_method()
        lambda_log.http_headers = json.dumps(
            http_server.get_headers(),
            indent=0
        )
        lambda_log.post_body = http_server.get_post_body()
        lambda_log.path_parameters = json.dumps(
            http_server.get_path_parameters(),
            indent=0
        )
        #print(json.dumps(dict(lambda_log), indent=4))
        lambda_log.insert()

    if event['httpMethod'] == HttpServer.METHOD_GET or \
       event['httpMethod'] == HttpServer.METHOD_POST:
        # check for book filename
        book_name = http_server.get_path_parameter('book_name')
        book_filename = 'Bluetooth Low Energy for iOS Swift'
        if book_name is not None:
            if book_name == 'ios-book':
                book_filename = 'Bluetooth Low Energy for iOS Swift'
            if book_name == 'android-book':
                book_filename = 'Bluetooth Low Energy in Android Java'
            if book_name == 'nrf-book':
                book_filename = 'Bluetooth Low Energy in C++ ' + \
                                'for nRF Microcontrollers'
            if book_name == 'arduino-book':
                book_filename = 'Bluetooth Low Energy in Arduino 101'
            if book_name == 'overview-book':
                book_filename = 'Bluetooth Low Energy - A Technical Primer'


        sender = 'tonyg@bluetoothlowenergy.co'
        recipient = 'tonyg@tonygaitatzis.com'
        bucket_filename = settings.s3['bucket_filename'] + book_filename + '.pdf'

        book_contents = get_download_contents(
            settings.s3['bucket_name'],
            bucket_filename
        )
        book_filename = 'downloads/{}.pdf'.format(
            str(round(1000000*time.time()))
        )
        book_url = create_download_link(
            settings.s3['bucket_name'], 
            book_filename,
            book_contents
        )
        book_url = 'http://bluetoothlowenergy.co/{}'.format(
            quote(book_filename)
        )


        print("book_filename: {}".format(book_filename))
        print("bucket: {}".format(settings.s3['bucket_name']))
        print("filename: {}".format(bucket_filename))

        message = MIMEMultipart()
        message["Subject"] = "Your book purchase"
        message["From"] = sender
        message["To"] = recipient
        message_content = MIMEText(
            'Thank you for your recent purchase of '
            '' + book_name + '\n'
            '\n'
            'It is available for download for 5 days with this link:\n'
            '' + book_url + '\n'
            '\n'
            'Enjoy,\n'
            'Tony'
        )
        message.attach(message_content)
        #html = "<h1>Hello</h1><p>This is a test</p>"
        #attachment = MIMEText(html, 'html')

        recipients = []
        recipients.append(message['To'])

        message_data = {'Data': message.as_string()}

        send_email(message["From"], recipients, message_data)

    output = {
        "status": "success"
    }
    return http_server.respond_ok(output)

