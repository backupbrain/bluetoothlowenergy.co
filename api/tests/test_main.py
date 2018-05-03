#!/usr/bin/env python3

import main
import json
import base64


http_method = "POST"
body = 'result=%7B%22status%22%3A200%2C%22requestId%22%3A%22b93d12bd-4bb6-49fb-a9aa-20cc17e31937%22%2C%22likelihood%22%3A0.95%2C%22photos%22%3A%5B%7B%22type%22%3A%22linkedin%22%2C%22typeId%22%3A%22linkedin%22%2C%22typeName%22%3A%22LinkedIn%22%2C%22url%22%3A%22https%3A%2F%2Fd2ojpxxtu63wzl.cloudfront.net%2Fstatic%2F1068300cbba0e474ba73858e242e7e07_7ce4e4e0ad5ec135d11bfde4fc6be448dfd34045748ad7ea70bd61e44210557c%22%2C%22isPrimary%22%3Atrue%7D%2C%7B%22type%22%3A%22gravatar%22%2C%22typeId%22%3A%22gravatar%22%2C%22typeName%22%3A%22Gravatar%22%2C%22url%22%3A%22https%3A%2F%2Fd2ojpxxtu63wzl.cloudfront.net%2Fstatic%2F8945245d3512e80b43fcc4a5cb7536ee_1a095dbf110e341b1a4fcc4555311e82c504a6873ca6965f0842ad398f782816%22%7D%2C%7B%22type%22%3A%22other%22%2C%22typeId%22%3A%22twitter%22%2C%22typeName%22%3A%22Twitter%22%2C%22url%22%3A%22https%3A%2F%2Fd2ojpxxtu63wzl.cloudfront.net%2Fstatic%2Fa3cc01b8e301a09ca361ccda6dbf3e2e_40031cc26435f86b35ecfb567f41e0b766d10768174aae9381c235870953f1c3%22%7D%2C%7B%22type%22%3A%22google%22%2C%22typeId%22%3A%22google%22%2C%22typeName%22%3A%22GooglePlus%22%2C%22url%22%3A%22https%3A%2F%2Fd2ojpxxtu63wzl.cloudfront.net%2Fstatic%2F5f1f4dfefc393c4dc7f974a51425374d_517000629dcee8ac74d86dc3b9335769d1f8fe3b16b0a1b812697317d1a0d8cb%22%7D%5D%2C%22contactInfo%22%3A%7B%22websites%22%3A%5B%7B%22url%22%3A%22http%3A%2F%2Fbackupbrain.org%22%7D%2C%7B%22url%22%3A%22http%3A%2F%2Fpersonalneuro.com%22%7D%2C%7B%22url%22%3A%22http%3A%2F%2Ftonygaitatzis.com%22%7D%5D%2C%22familyName%22%3A%22Gaitatzis%22%2C%22fullName%22%3A%22Tony+Gaitatzis%22%2C%22givenName%22%3A%22Tony%22%7D%2C%22organizations%22%3A%5B%7B%22name%22%3A%22ReadWrite%22%2C%22startDate%22%3A%222017%22%2C%22title%22%3A%22Instructor%22%2C%22current%22%3Atrue%7D%5D%2C%22demographics%22%3A%7B%22locationDeduced%22%3A%7B%22normalizedLocation%22%3A%22San+Francisco%2C+California%2C+United+States%22%2C%22deducedLocation%22%3A%22San+Francisco%2C+California%2C+United+States%22%2C%22city%22%3A%7B%22name%22%3A%22San+Francisco%22%7D%2C%22state%22%3A%7B%22name%22%3A%22California%22%2C%22code%22%3A%22CA%22%7D%2C%22country%22%3A%7B%22name%22%3A%22United+States%22%2C%22code%22%3A%22US%22%7D%2C%22continent%22%3A%7B%22deduced%22%3Atrue%2C%22name%22%3A%22North+America%22%7D%2C%22county%22%3A%7B%22deduced%22%3Atrue%2C%22name%22%3A%22San+Francisco%22%7D%2C%22likelihood%22%3A1.0%7D%2C%22gender%22%3A%22Male%22%2C%22locationGeneral%22%3A%22San+Francisco%2C+California%2C+United+States%22%7D%2C%22socialProfiles%22%3A%5B%7B%22type%22%3A%22aboutme%22%2C%22typeId%22%3A%22aboutme%22%2C%22typeName%22%3A%22About.me%22%2C%22url%22%3A%22https%3A%2F%2Fabout.me%2Ftonygaitatzis%22%2C%22username%22%3A%22tonygaitatzis%22%7D%2C%7B%22bio%22%3A%22Founder+%40personal-neuro%2C+NetNinja+%E2%80%A2+Worked+at+%40dollero%2C+My+skills+are+remarkably+diverse+but+I+always+inspire+a+team+of+people+to+shine+together%22%2C%22followers%22%3A151%2C%22type%22%3A%22angellist%22%2C%22typeId%22%3A%22angellist%22%2C%22typeName%22%3A%22AngelList%22%2C%22url%22%3A%22https%3A%2F%2Fangel.co%2Ftony-gaitatzis%22%2C%22username%22%3A%22tony-gaitatzis%22%2C%22id%22%3A%22257171%22%7D%2C%7B%22type%22%3A%22github%22%2C%22typeId%22%3A%22github%22%2C%22typeName%22%3A%22Github%22%2C%22url%22%3A%22https%3A%2F%2Fgithub.com%2Fbackupbrain%22%2C%22username%22%3A%22backupbrain%22%7D%2C%7B%22followers%22%3A37%2C%22type%22%3A%22google%22%2C%22typeId%22%3A%22google%22%2C%22typeName%22%3A%22GooglePlus%22%2C%22url%22%3A%22https%3A%2F%2Fplus.google.com%2F101460153830694657925%22%2C%22id%22%3A%22101460153830694657925%22%7D%2C%7B%22type%22%3A%22gravatar%22%2C%22typeId%22%3A%22gravatar%22%2C%22typeName%22%3A%22Gravatar%22%2C%22url%22%3A%22https%3A%2F%2Fgravatar.com%2Fbackupbrain%22%2C%22username%22%3A%22backupbrain%22%2C%22id%22%3A%2219765%22%7D%2C%7B%22type%22%3A%22klout%22%2C%22typeId%22%3A%22klout%22%2C%22typeName%22%3A%22Klout%22%2C%22url%22%3A%22http%3A%2F%2Fklout.com%2FHealthDevsSF%22%2C%22username%22%3A%22HealthDevsSF%22%2C%22id%22%3A%22228839172979703340%22%7D%2C%7B%22bio%22%3A%22I%27m+a+traveling+entrepreneur.+I%27ve+started+several+award-winning+companies+in+several+countries.+I+am+not+only+creative+and+have+a+deep+understanding+of+technology%2C+but+I+have+an+amazing+ability+to+rally+people+to+work+together+towards+a+singular+goal.+My+strengths+lie+in+branding%2C+team+building%2C+and+software+development.+I%27m+multicultural+and+can+speak+to+many+people%27s+diverse+interests.+My+strong+communication+skills+and+personal+brand+have+led+me+to+be+featured+in+several+cultural+pieces+in+major+media+including+Bloomberg%2C+the+Guardian%2C+and+GEO+magazines.+My+strong+technical+skills+have+led+me+to+acquire+several+provisional+patents+in+biosensor+technology+and+network+security%2C+and+to+publish+a+book.%22%2C%22followers%22%3A500%2C%22following%22%3A500%2C%22type%22%3A%22linkedin%22%2C%22typeId%22%3A%22linkedin%22%2C%22typeName%22%3A%22LinkedIn%22%2C%22url%22%3A%22https%3A%2F%2Fwww.linkedin.com%2Fin%2Ftonygaitatzis%22%2C%22username%22%3A%22tonygaitatzis%22%7D%2C%7B%22type%22%3A%22tumblr%22%2C%22typeId%22%3A%22tumblr%22%2C%22typeName%22%3A%22Tumblr%22%2C%22url%22%3A%22http%3A%2F%2Ftonygaitatzis.tumblr.com%22%2C%22username%22%3A%22tonygaitatzis%22%7D%2C%7B%22bio%22%3A%22Has+been+bringing+technology+companies+into+the+social+media+age+for+almost+a+decade.++Currently+in+Silicon+Valley+Guiding+the+development+of+a+BCI+company.%22%2C%22followers%22%3A84%2C%22following%22%3A124%2C%22type%22%3A%22twitter%22%2C%22typeId%22%3A%22twitter%22%2C%22typeName%22%3A%22Twitter%22%2C%22url%22%3A%22https%3A%2F%2Ftwitter.com%2Fgaitatzis%22%2C%22username%22%3A%22gaitatzis%22%2C%22id%22%3A%22409367607%22%7D%5D%2C%22digitalFootprint%22%3A%7B%22scores%22%3A%5B%7B%22provider%22%3A%22klout%22%2C%22type%22%3A%22general%22%2C%22value%22%3A42%7D%5D%2C%22topics%22%3A%5B%7B%22provider%22%3A%22aboutme%22%2C%22value%22%3A%22BCI%22%7D%2C%7B%22provider%22%3A%22aboutme%22%2C%22value%22%3A%22Disruptive+Health%22%7D%2C%7B%22provider%22%3A%22klout%22%2C%22value%22%3A%22Atlanta%22%7D%2C%7B%22provider%22%3A%22klout%22%2C%22value%22%3A%22Bitcoin%22%7D%2C%7B%22provider%22%3A%22klout%22%2C%22value%22%3A%22Health%22%7D%2C%7B%22provider%22%3A%22klout%22%2C%22value%22%3A%22Neuroscience%22%7D%2C%7B%22provider%22%3A%22klout%22%2C%22value%22%3A%22Ruby%22%7D%2C%7B%22provider%22%3A%22klout%22%2C%22value%22%3A%22Startups%22%7D%5D%7D%7D&webhookId=backupbrain%40gmail.com'
'''
query_string_parameters = {
    'email': 'compound.email@gmail.com',
    'url': 'http://example.com',
    'utm_campaign': 'testCampaign',
    'utm_source' : 'readwrite.com',
    'utm_medium' : 'email',
    'event': 'inbound',
}
'''
query_string_parameters = {
    'email': 'compound.email@gmail.com',
    'url': 'http://example.com?utm_source=fake_utm',
    'utm_campaign': 'testCampaign',
    'utm_source' : 'readwrite.com',
    'utm_medium' : 'email',
    'event': 'inbound',
}
headers = {
  "Accept": "*/*",
  "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
}
http_auth = {
#	'username': 'lzh0jzmzjxngqji8',
#	'password': 'h4qle8iosbj95647g6u8hp8vxn84lob3'
}

user_agent_string = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
user_agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"

event = {  
   "body":body,
   "resource":"/exit",
   "requestContext":{  
      "resourceId":"1ozsvw",
      "apiId":"39zmlgv432",
      "resourcePath":"/exit",
      "httpMethod":http_method,
      "requestId":"4dc41b03-26ab-11e7-89cc-8d1866127737",
      "accountId":"641387272068",
      "identity":{  
         "apiKey":None,
         "userArn":None,
         "cognitoAuthenticationType":None,
         "accessKey":None,
         "caller":None,
         "userAgent": user_agent_string,
         "user":None,
         "cognitoIdentityPoolId":None,
         "cognitoIdentityId":None,
         "cognitoAuthenticationProvider":None,
         "sourceIp":"85.144.185.221",
         "accountId":None
      },
      "stage":"prod"
   },
   "queryStringParameters": query_string_parameters,
   "httpMethod":http_method,
   "pathParameters":{'book_name':'ios-book'},
   "headers":{  
      "Via":"2.0 c87cfbad1c3e6dd7cee82f341ee59ed8.cloudfront.net (CloudFront)",
      "Accept-Language":"en-US,en;q=0.8",
      "Accept-Encoding":"gzip, deflate, sdch, br",
      "CloudFront-Is-SmartTV-Viewer":"false",
      "CloudFront-Forwarded-Proto":"https",
      "X-Forwarded-For":"85.144.185.221, 54.240.156.109",
      "CloudFront-Viewer-Country":"NL",
      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "upgrade-insecure-requests":"1",
      "X-Amzn-Trace-Id":"Root=1-58fa2c0c-1c3548b95a9852417a734681",
      "Host":"39zmlgv432.execute-api.us-east-1.amazonaws.com",
      "X-Forwarded-Proto":"https",
      "X-Amz-Cf-Id":"I9wUfTnzTFukNkPPcqNhZ94-kq-T7HLt3vaaYwbdx_6ldOh9OfYD8Q==",
      "CloudFront-Is-Tablet-Viewer":"false",
      "X-Forwarded-Port":"443",
      "User-Agent":user_agent_string,
      "CloudFront-Is-Mobile-Viewer":"false",
      "CloudFront-Is-Desktop-Viewer":"true",
      "Cookie": "a=1; b=2"
   },
   "stageVariables":None,
   "path":"/pixel",
   "isBase64Encoded":False
}



for header in headers:
	event['headers'][header] = headers[header]

if len(http_auth) == 2:
	event['headers']["Authorization"] = "Basic " + base64.b64encode(http_auth['username'] + ":" + http_auth['password'])

result = main.lambda_handler(event, event['requestContext'])

#print(json.dumps(event,indent=4))

print("Result:")
print(json.dumps(result,indent=4))

