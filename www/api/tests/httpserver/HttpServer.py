import base64 
import json

class HttpServer:
    METHOD_PUT = "PUT"
    METHOD_POST = "POST"
    METHOD_GET = "GET"
    METHOD_DELETE = "DELETE"
    METHOD_OPTIONS = "OPTIONS"
    METHOD_HEAD = "HEAD"

    AUTHTYPE_BASIC = "Basic"

    event = None

    def __init__(self, event):
        self.event = event


    def get_headers(self):
        if 'headers' in self.event:
            return self.event['headers']
            
    def get_method(self):
        if 'httpMethod' in self.event:
            return self.event['httpMethod']

    def get_authorization_data(self):
        authorization = {"type": None, "username": None, "password": None}


        if 'headers' in self.event:
            if 'Authorization' in self.event['headers']:
                auth_data_string = self.event['headers']['Authorization']
                auth_data = auth_data_string.split(" ")
                if len(auth_data) == 2:
                    auth_type = auth_data[0]
                    base64_auth_credential = auth_data[1]

                    authorization['type'] = auth_type

                    keypair_string = base64.b64decode(base64_auth_credential)
                    keypair = keypair_string.split(":")
                    if len(keypair) == 2:
                        authorization['username'] = keypair[0]
                        authorization['password'] = keypair[1]

        return authorization

    def get_url(self):
        if 'path' in self.event:
            return self.event['path']

    def get_post_body(self):
        if 'body' in self.event:
            return self.event['body']

    def get_path_parameters(self):
        if 'pathParameters' in self.event:
            return self.event['pathParameters']


    def get_path_parameter(self, path_name):
        if 'pathParameters' in self.event:
            if path_name in self.event['pathParameters']:
                return self.event['pathParameters'][path_name]


    def get_json_post_body(self):
        post_body = self.get_post_body()
        try:
            data = json.loads(post_body)
        except:
            data = None

        return data


    def get_cookie_string(self):
        if 'headers' in self.event:
            if self.event['headers'] != None:
                if 'Cookie' in self.event['headers']:
                    if self.event['headers']['Cookie'] != None:
                        return self.event['headers']['Cookie']
                
    def get_query_parameters(self):
        if 'queryStringParameters' in self.event:
            return self.event['queryStringParameters']

    def get_query_parameter(self, key):
        if 'queryStringParameters' in self.event:
            if key in self.event['queryStringParameters']:
                return self.event['queryStringParameters'][key]


    def get_user_agent(self):
        if 'requestContext' in self.event:
            if 'identity' in self.event['requestContext']:
                if 'userAgent' in self.event['requestContext']['identity']:
                   return self.event['requestContext']['identity']['userAgent']


    def get_ip(self):
        if 'requestContext' in self.event:
            if 'identity' in self.event['requestContext']:
                if 'sourceIp' in self.event['requestContext']['identity']:
                   return self.event['requestContext']['identity']['sourceIp']

    def get_forwarded_for(self):
        if 'headers' in self.event:
            if self.event['headers'] != None:
                if 'X-Forwarded-For' in self.event['headers']:
                    return self.event['headers']['X-Forwarded-For']

    def get_accept_language(self):
        if 'headers' in self.event:
            if self.event['headers'] != None:
                if 'Accept-Language' in self.event['headers']:
                    return self.event['headers']['Accept-Language']


    def get_primary_language_and_locale(self):
        accept_language = self.get_accept_language()
        if accept_language != None:
            accept_language = accept_language.lower()
            split = accept_language.split(",",1)

            primary_language_locale = split[0]

            if primary_language_locale != None:

                primary_language_locale_split = primary_language_locale.split("-",1)

                language = primary_language_locale_split[0]
                locale = None
                if len(primary_language_locale_split) > 1:
                    locale = primary_language_locale_split[1]


                result = { 'language': language, 'locale': locale }
                return result


            

    def get_referer(self):
        if 'headers' in self.event:
            if self.event['headers'] != None:
                if 'Referer' in self.event['headers']:
                    return self.event['headers']['Referer']

    def redirect(self, url, headers=None):
        output_headers =  {
            'Location': url
        }
        if headers != None:
            for key,value in headers.iteritems():
               output_headers[key] = value

        return self.respond("{}", code=301, headers=output_headers)


    def respond(self, value, code=200, content_type=None, headers=None):
        output = {
            'statusCode': code,
            'body': value,
            'headers': {
            }
        }

        if content_type != None:
            output['headers']['Content-Type'] = content_type

        if headers != None:
            for key,value in headers.iteritems():
                output['headers'][key] = value

        print(json.dumps(output,indent=4))
        return output


    def respond_binary(self, value, code=200, content_type='application/octet-stream', headers=None):
        return base64.b64encode(value)

    def respond_options(self, methods, code=200, content_type='httpd/unix-directory'):
        headers = {
            'Allow': ",".join(methods)
        }
        return self.respond("", code, content_type, headers)


    def respond_ok(self, value, code=200, content_type='application/json'):
        output = {
            'statusCode': code,
            'body': json.dumps(value),
            'headers': {
                'Content-Type': content_type
            }
        }

        #print(output)

        return output

    def respond_error(self, message, code=400, content_type='application/json'):
        output = {
            'statusCode': code,
            'body': json.dumps( {"error": message} ),
            'headers': {
                'Content-Type': content_type
            }
        }

        #print(output)

        return output


class HttpServer_AuthError(LookupError):
    '''raise this when there is an authentication requirement'''
