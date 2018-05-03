class LambdaLog:
	database_object = None

	id = None
	application_id = None
	endpoint_url = None
	url_query = None
	ip_address = None
	forwarding_ip_addresses = None
	cookie_value = None
	user_agent = None
	http_method = None
	http_headers = None
	post_body = None
	response_code = None
	response_body = None
	path_parameters = None
	internal_message = None
	ctime = None

	def __init__(self, database_object):
		self.database_object = database_object


	def __iter__(self):
		exclusions = [
			'database_object'
		]
		for property, value in vars(self).items():
			if not property in exclusions:
				yield(property, value)



	def insert(self):
		self.id = self.database_object.insert(self)
		return self.id

	def update(self):
		result = self.database_object.update(self)
		return result