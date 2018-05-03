#!/usr/bin/python

import sys
import inspect
from os import path
import base64
import json
import unittest

class HttpServerTestCase(unittest.TestCase):

    ''' test inferences '''
    def test_get_primary_language_simple(self):
        accept_language = 'en-US'
        expected_language = {'language': 'en', 'locale': 'us'}

        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None, 
            'headers': {
                'Accept-Language': accept_language
            }
        }

        http_server = HttpServer(event)
        resulting_language = http_server.get_primary_language_and_locale()

        self.assertEqual(expected_language, resulting_language)

    def test_get_primary_language_complet(self):
        accept_language = 'nb-NO,en-US;q=0.8'
        expected_language = {'language': 'nb', 'locale': 'no'}

        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None, 
            'headers': {
                'Accept-Language': accept_language
            }
        }

        http_server = HttpServer(event)
        resulting_language = http_server.get_primary_language_and_locale()

        self.assertEqual(expected_language, resulting_language)


    ''' test lookups '''

    def test_get_ip(self):
        ip = '192.168.0.1'

        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None, 
            'requestContext': {
                'identity':{
                     'sourceIp': ip
               },
            },
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }

        http_server = HttpServer(event)
        resulting_ip = http_server.get_ip()

        self.assertEqual(ip, resulting_ip)

    def test_get_forwarded_for(self):
        forwarded_ips = [ '192.168.0.1', '192.168.0.1']
        forward_string = ",".join(forwarded_ips)
      
        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None,
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
                'X-Forwarded-For': forward_string
            }
        }


        http_server = HttpServer(event)
        resulting_forwards = http_server.get_forwarded_for()

        self.assertEqual(forward_string, resulting_forwards)

    def test_get_user_agent(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

      
        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None,
            'requestContext':{  
                'identity':{  
                    'userAgent': user_agent
                 },
            },
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*'
            }
        }


        http_server = HttpServer(event)
        resulting_user_agent = http_server.get_user_agent()

        self.assertEqual(user_agent, resulting_user_agent)


    def test_get_accept_language(self):
        accept_language = "en-US,en;q=0.8"

      
        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None,
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*',
                'Accept-Language': accept_language
            }
        }


        http_server = HttpServer(event)
        resulting_accept_language = http_server.get_accept_language()

        self.assertEqual(accept_language, resulting_accept_language)
          

    ''' Test Query String '''
    def test_get_query_parameters(self):
        query_string_parameters = {
            "key1": "value1",
            "key2": "value2"
        }

      
        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None,
            "queryStringParameters": query_string_parameters,
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*',
            }
        }


        http_server = HttpServer(event)
        resulting_query_string_parameters = http_server.get_query_parameters()

        self.assertEqual(query_string_parameters, resulting_query_string_parameters)
          

    def test_get_query_parameter_exists(self):
        query_string_parameters = {
            "key1": "value1",
            "key2": "value2"
        }
        key = 'key1'
        expected_value = query_string_parameters[key]

      
        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None,
            "queryStringParameters": query_string_parameters,
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*',
            }
        }


        http_server = HttpServer(event)
        resulting_value = http_server.get_query_parameter(key)

        self.assertEqual(expected_value, resulting_value)
          


    def test_get_query_parameter_empty(self):
        query_string_parameters = {
            "key1": "value1",
            "key2": "value2"
        }
        key = 'key3'
        expected_value = None

      
        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None,
            "queryStringParameters": query_string_parameters,
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*',
            }
        }


        http_server = HttpServer(event)
        resulting_value = http_server.get_query_parameter(key)

        self.assertEqual(expected_value, resulting_value)



    def test_get_referrer(self):
        referer = 'http://google.com'

        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None, 
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
                'Referer': referer
            }
        }

        http_server = HttpServer(event)
        resulting_referer = http_server.get_referer()

        self.assertEqual(referer, resulting_referer)


    ''' Test errors '''
    def test_event_load_no_body(self):
        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'PUT', 
            'pathParameters': None, 
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }
        http_server = HttpServer(event)

        self.assertEqual(event, http_server.event)


    def test_event_load_json_body(self):

        input_json = {"email": "email@example.com", "password": "password"}
        event = {
            'body': json.dumps(input_json), 
            'queryStringParameters': None, 
            'httpMethod': 'PUT', 
            'pathParameters': None, 
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }
        http_server = HttpServer(event)
        output_json = http_server.get_json_post_body()

        self.assertEqual(input_json, output_json)


    ''' Test Authorization '''
    def test_authorization_no_auth(self):
        expected_auth = {
            "type": None,
            "username": None,
            "password": None
        }

        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'PUT', 
            'pathParameters': None, 
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }
        http_server = HttpServer(event)
        resulting_auth = http_server.get_authorization_data()

        self.assertEqual(expected_auth, resulting_auth)


    def test_authorization_bad_type(self):
        username = "username"
        password = "password"
        expected_auth = {
            "type": None,
            "username": None,
            "password": None
        }

        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'PUT', 
            'pathParameters': None, 
            'headers': {
                'Authorization': base64.b64encode(username + ":" + password),
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }
        http_server = HttpServer(event)
        resulting_auth = http_server.get_authorization_data()

        self.assertEqual(expected_auth, resulting_auth)


    def test_authorization_bad_format(self):
        auth_type = "Basic"
        username = "username"
        expected_auth = {
            "type": auth_type,
            "username": None,
            "password": None
        }

        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'PUT', 
            'pathParameters': None, 
            'headers': {
                'Authorization': auth_type + ' ' + base64.b64encode(username),
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }
        http_server = HttpServer(event)
        resulting_auth = http_server.get_authorization_data()

        self.assertEqual(expected_auth, resulting_auth)


    def test_authorization_good_authorization(self):
        auth_type = "Basic"
        username = "username"
        password = "password"
        expected_auth = {
            "type": auth_type,
            "username": username,
            "password": password
        }

        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'PUT', 
            'pathParameters': None, 
            'headers': {
                'Authorization': auth_type + " " + base64.b64encode(username + ':' + password),
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }
        http_server = HttpServer(event)
        resulting_auth = http_server.get_authorization_data()

        self.assertEqual(expected_auth, resulting_auth)


    ''' test responses '''
    def test_response_options(self):
        code = '123'
        supported_methods = ["POST", "PUT", "GET"]
        expected_output = {
            'statusCode': code,
            'body': "",
            'headers': {
                'Allow': ",".join(supported_methods)

            }
        }
        
        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'OPTIONS', 
            'pathParameters': None, 
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }

        http_server = HttpServer(event)
        resulting_output = http_server.respond_options(supported_methods, code)

        self.assertEqual(expected_output, resulting_output)


    def test_response_ok(self):
        code = '123'
        value = {"email": "email@example.com", "password": "password"}

        expected_output = {
            'statusCode': code,
            'body': json.dumps(value),
            'headers': {
                'Content-Type': 'application/json',
            }
        }
        
        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None, 
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }

        http_server = HttpServer(event)
        resulting_output = http_server.respond_ok(value, code)

        self.assertEqual(expected_output, resulting_output)


    def test_response_error(self):
        code = '123'
        message = "This is an error"

        expected_output = {
            'statusCode': code,
            'body': json.dumps( {"error": message} ),
            'headers': {
                'Content-Type': 'application/json',
            }
        }

        event = {
            'body': None,
            'queryStringParameters': None, 
            'httpMethod': 'GET', 
            'pathParameters': None, 
            'headers': {
                'Content-Type': 'application/json', 
                'Accept-Encoding': 'gzip, deflate', 
                'Charset': 'utf-8', 
                'Accept': '*/*', 
            }
        }

        http_server = HttpServer(event)
        resulting_output = http_server.respond_error(message, code)

        self.assertEqual(expected_output, resulting_output)




if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        currentdir = path.dirname(path.abspath(inspect.getfile(inspect.currentframe())))
        parentdir = path.dirname(currentdir)
        sys.path.insert(0,parentdir) 
        from HttpServer import HttpServer
    else:
        from ..HttpServer import HttpServer


    unittest.main()
