
import boto3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def lambda_handler(event, context):
    sender = 'tonyg@bluetoothlowenergy.co'
    recipient = 'tonyg@tonygaitatzis.com'

    message = MIMEMultipart()
    message["Subject"] = "ses test"
    message["From"] = sender
    message["To"] = recipient
    html = "<h1>Hello</h1><p>This is a test</p>"
    attachment = MIMEText(html, 'html')
    message.attach(attachment)

    #text_message = MIMEText('Attached is an important CSV')
    #message.attach(text_message)

    # binary attachments
    '''
    file_name = s3_client.download_file('s3_bucket_name', 'path/to/file.jpg', '/tmp/x.jpg')

    book_attachment = MIMEApplication(book_contents)
    book_attachment.add_header(
        'Content-Disposition', 
        'attachment', 
        filename=book_filename
    )
    message.attach(book_attachment)
    '''

    recipients = []
    recipients.append(message['To'])

    try:
        ses_client = boto3.client('ses')
        #bounceResponse = ses_client.send_raw_email(**send_bounce_params)
        bounceResponse = ses_client.send_raw_email(
            Source=message['From'],
            Destinations=recipients,
            RawMessage={'Data': message.as_string()}
        )
        print('message sent')
        return {'disposition': 'stop_rule_set'}
    except Exception as e:
        print_with_timestamp(e)
        print_with_timestamp('An error occurred while sending bounce for message')
        raise e
