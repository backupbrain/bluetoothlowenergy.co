import re
import json
import copy

class DatabaseObject(object):

	database = None
	verbose = False
	debug = False

	def __init__(self, database):
		self.database = database


	@staticmethod
	def camel_to_underscore(name, separator="_"):
		s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
		underscore_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
		underscore_name = underscore_name.replace("__", "_")
		return underscore_name


	def dict_factory(self, cursor, row):
		''' http://stackoverflow.com/a/3300514 '''
		data = {}
		for index, column in enumerate(cursor.description):
			data[column[0]] = row[index]
		return data

	def execute(self, query):
		cursor = self.database.cursor()
		if self.verbose:
			print(query)
			#pass

		if not self.debug:
			query_type = query.split(" ",1)[0].lower()

			self.database.row_factory = self.dict_factory
			try:

				result = cursor.execute(query)
			except Exception as e:
				print(e)
				print("query: '{}'".format(query))
				return None

				
			if query_type == "select" or query_type == "show":
				return cursor.fetchall()

			elif query_type == "update" or query_type == "delete":
				self.database.commit()
				return result

			elif query_type == "insert":
				self.database.commit()
				inserted_id = cursor.lastrowid
				return inserted_id

			else:
				self.database.commit()
				return None


	def drop_table(self, obj):
		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)
		query = 'DROP TABLE IF EXISTS `{}`'.format(table_name)
		
		result = self.execute(query)

		return result

	
	def create_table(self, obj, data_types):
		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)

		types = []
		for column, data_type in data_types.items():
			types.append("`{}` {}".format(column, data_type))
		query = "CREATE TABLE IF NOT EXISTS `{}` ({})".format(table_name, ",".join(types))

		result = self.execute(query)
		return result

	def fetch_all(self, obj, columns="*"):
		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)
		#print(table_name)
		
		query = "SELECT {columns} FROM `{table}`".format(
			columns=columns,
			table=table_name
		)

		result = self.execute(query)

		#print(json.dumps(result,indent=4))
		results = None
		if len(result) > 0:
			results = []
			for row in result:
				o = copy.copy(obj)
				if isinstance(row, dict):
					for column, value in row.items():
						setattr(o, column, value)
				elif isinstance(row, tuple) or isinstance(row, list):
					for idx, col in enumerate(cursor.description):
						setattr(o, col[0], row[idx])
				
				results.append(o)


		#print(results)
		return results

	def fetch(self, obj, id):
		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)
		conditions = [{
			'column': 'id',
			'equivalence': '=',
			'value': id
		}]
		return self.fetch_by(table_name, conditions)

	def fetch_by(self, obj, conditions, columns="*", num_rows=None, start_row=None):
		''' condition is like ['column': id, 'equivalence': '=', 'value': '1']
		'''
		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)
		
		data = dict(obj)

		columns_string = "*"
		if columns != None:
			if isinstance(columns, list):
				",".join(["`" + column + "`" for column in columns if not column == "*"])
			else:
				if columns == "*":
					columns_string = columns
				else:
					columns_string = "`" + columns + "`"


		condition_strings = []
		for condition in conditions:
			if isinstance(condition['value'], type(None)):
				cleaned_value = 'NULL'
			elif isinstance(condition['value'], bool):
				cleaned_value = str(condition['value']).upper()
			elif isinstance(condition['value'], int) or isinstance(condition['value'], float):
				cleaned_value = str(condition['value'])
			else:
				try:
					cleaned_value = self.database.escape(condition['value'])
				except:
					cleaned_value = condition['value'].replace("'","\'")
					cleaned_value = cleaned_value.replace('"', '\"')
					cleaned_value = "'" + cleaned_value + "'"

			condition_string = "`{column}` {equivalence} {value}".format(
				column=condition['column'],
				equivalence=condition['equivalence'],
				value=cleaned_value
			)
			condition_strings.append(condition_string)
		conditions_string = " AND ".join(condition_strings)

		limit_string = ""
		if start_row != None:
			if num_rows != None:
				limit_string = " LIMIT {},{}".format(start_row, num_rows)
		else:
			if num_rows != None:
				limit_string = " LIMIT {}".format(num_rows)

		query = "SELECT {columns} FROM `{table}` WHERE ({conditions}){limit}".format(
			columns=columns_string,
			table=table_name,
			conditions=conditions_string,
			limit=limit_string
		)
		#print(query)
		
		result = self.execute(query)

		#print("results:")
		#print(json.dumps(result,indent=4))
		results = None
		if result != None and len(result) > 0:
			if len(result) == 1:
				return result[0]
			else:
				results = []
				for row in result:
					o = copy.copy(obj)
					if isinstance(row, dict):
						for column, value in row.items():
							setattr(o, column, value)
					elif isinstance(row, tuple) or isinstance(row, list):
						for idx, col in enumerate(cursor.description):
							setattr(o, col[0], row[idx])
					
					results.append(o)


		#print(results)
		return results


	def delete(self, obj, conditions):
		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)
		data = dict(obj)

		condition_strings = []
		for condition in conditions:
			if isinstance(condition['value'], type(None)):
				cleaned_value = 'NULL'
			elif isinstance(condition['value'], bool):
				cleaned_value = str(condition['value']).upper()
			elif isinstance(condition['value'], int) or isinstance(condition['value'], float):
				cleaned_value = str(condition['value'])
			else:
				try:
					cleaned_value = self.database.escape(condition['value'])
				except:
					cleaned_value = condition['value'].replace("'","\'")
					cleaned_value = cleaned_value.replace('"', '\"')
					cleaned_value = "'" + cleaned_value + "'"

			condition_string = "`{column}` {equivalence} {value}".format(
				column=condition['column'],
				equivalence=condition['equivalence'],
				value=cleaned_value
			)
			condition_strings.append(condition_string)
		conditions_string = " AND ".join(condition_strings)

		query = "DELETE FROM `{table}` WHERE ({conditions})".format(
			table=table_name,
			conditions=conditions_string)

		self.execute(query)


	def insert_if_not_exists(self, obj):
		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)
		#print("table_name: "+ table_name)
		data = dict(obj)

		#print(json.dumps(data, indent=4))

		to_insert = False
		if 'id' not in data:
			to_insert = True
		else:
			if data['id'] == None:
				to_insert = True

		if to_insert:
			if 'ctime' in data:
				del(data['ctime'])

			# check if the row exists in the database
			conditions = []
			for key, value in data.items():
				if value != None:
					#if isinstance(value, type(None)):
					#	cleaned_value = 'NULL'
					#	cleaned_equivalence = ' IS '
					if isinstance(value, bool):
						cleaned_value = int(value == 'true') #str(value).upper()
						cleaned_equivalence = '='
					elif isinstance(value, int) or isinstance(value, float):
						cleaned_value = str(value)
						cleaned_equivalence = '='
					else:
						cleaned_value = str(value).encode('utf-8') #self.database.escape(value) 
						cleaned_equivalence = '='

					fetch_condition = {
						'column': key,
						'equivalence': cleaned_equivalence,
						'value': cleaned_value
					}
					conditions.append(fetch_condition)


			result = self.fetch_by(obj, conditions, 'id', num_rows=1)
			#print(json.dumps(result, indent=4))
			if result != None:
				id = None
				if isinstance(result, dict):
					id = result['id']
				else:
					id = result.id
				return id
			else:
				return self.insert(obj)

	def save(self, obj):
		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)
		data = dict(obj)

		to_insert = False
		if 'id' not in data:
			to_insert = True
		else:
			if data['id'] == None:
				to_insert = True


		if to_insert == False:
			if data['id'] != None:
				return self.update(obj)
		else:

			if 'ctime' in data:
				del(data['ctime'])

			# check if the row exists in the database
			conditions = []
			for key, value in data.items():
				if value != None:
					#if isinstance(value, type(None)):
					#	cleaned_value = 'NULL'
					#	cleaned_equivalence = ' IS '
					if isinstance(value, bool):
						cleaned_value = int(value == 'true') #str(value).upper()
						cleaned_equivalence = '='
					elif isinstance(value, int) or isinstance(value, float):
						cleaned_value = str(value)
						cleaned_equivalence = '='
					else:
						cleaned_value = str(value).encode('utf-8') #self.database.escape(value) 
						cleaned_equivalence = '='

					fetch_condition = {
						'column': key,
						'equivalence': cleaned_equivalence,
						'value': cleaned_value
					}
					conditions.append(fetch_condition)


			result = self.fetch_by(obj, conditions, 'id', num_rows=1)
			if result != None:
				if isinstance(result, dict):
					obj.id = result['id']
				else:
					obj.id = result.id
				self.update(obj)
				return obj.id
			else:
				return self.insert(obj)

	def update(self, obj):
		''' condition is like ['column': id, 'equivalence': '=', 'value': '1']
		'''

		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)
		data = dict(obj)

		#if 'id' in data:
		condition = {
			'column': 'id',
			'equivalence': '=',
			'value': str(data['id'])
		}
		del(data['id'])

		#print(json.dumps(data,indent=3))
		sets = []
		for column, value in data.items():
			#print(column + ": " + str(value))

			if isinstance(value, type(None)):
				cleaned_value = 'NULL'
			elif isinstance(value, bool):
				cleaned_value = str(value).upper()
			elif isinstance(value, int) or isinstance(value, float):
				cleaned_value = str(value)
			else:
				try:
					cleaned_value = self.database.escape(value.encode("utf8"))
				except:
					cleaned_value = str(value).replace("'","\'")
					cleaned_value = cleaned_value.replace('"', '\"')
					cleaned_value = "'" + cleaned_value + "'"

			sets.append("`{column}`={value}".format(column=column, value=cleaned_value))

		set_string = ", ".join(sets)


		try:
			cleaned_value = self.database.escape(condition['value'])
		except:
			cleaned_value = condition['value'].replace("'","\'")
			cleaned_value = cleaned_value.replace('"', '\"')
			cleaned_value = "'" + cleaned_value + "'"

		query = "UPDATE `{table}` SET {sets}  WHERE `{column}` {equivalence} {value}".format(
			table=table_name,
			sets=set_string,
			column=condition['column'], 
			equivalence=condition['equivalence'], 
			value=cleaned_value
		)

		self.execute(query)


	def insert(self, obj):
		table_name = DatabaseObject.camel_to_underscore(obj.__class__.__name__)
		data = dict(obj)
		if 'id' in data:
			if data['id'] != None:
				del(data['id'])

		columns = []
		cleaned_values = []
		for column, value in data.items():
			columns.append('`{column}`'.format(column=column))

			if isinstance(value, type(None)):
				cleaned_value = 'NULL'
			elif isinstance(value, bool):
				cleaned_value = str(value).upper()
			elif isinstance(value, int) or isinstance(value, float):
				cleaned_value = str(value)
			else:
				try:
					cleaned_value = self.database.escape(value)
				except:
					cleaned_value = value.replace("'","\'")
					cleaned_value = cleaned_value.replace('"', '\"')
					cleaned_value = "'" + cleaned_value + "'"

			cleaned_values.append(cleaned_value)

		query = "INSERT INTO `{table}` ({columns}) VALUES ({values})".format(
			table=table_name,
			columns=",".join(columns),
			values=",".join(cleaned_values)
		)

		inserted_id = self.execute(query)

		return inserted_id


	def insert_many(self, objs):
		if len(objs) < 1:
			return

		table_name = DatabaseObject.camel_to_underscore(objs[0].__class__.__name__)

		columns = []
		column_names = []
		data = dict(objs[0])
		if 'id' in data:
			if data['id'] != None:
				del(data['id'])
		for column in data:
			columns.append('`{column}`'.format(column=column))
			column_names.append(column)

		#print("column names")
		#print(json.dumps(column_names, indent=4))

		sets = []
		for obj in objs:
			#print(obj.__class__)
			data = dict(obj)

			#print(json.dumps(data, indent=4))
			if 'id' in data:
				if data['id'] != None:
					del(data['id'])
			cleaned_values = []
			for column in column_names:
				if not column in data:
					cleaned_value = "NULL"
				else:
					value = data[column]
					if isinstance(value, type(None)):
						cleaned_value = 'NULL'
					elif isinstance(value, bool):
						cleaned_value = str(value).upper()
					elif isinstance(value, int) or isinstance(value, float):
						cleaned_value = str(value)
					else:
						try:
							cleaned_value = self.database.escape(value.encode('utf-8'))
						except:
							cleaned_value = value.encode('utf-8').replace("'","\'")
							cleaned_value = cleaned_value.replace('"', '\"')
							cleaned_value = "'" + cleaned_value + "'"


				cleaned_values.append(cleaned_value)
			sets.append(",".join(cleaned_values))

		cleaned_value_sets = "({sets})".format(sets="),(".join(sets))

		query = "INSERT INTO `{table}` ({columns}) VALUES {values}".format(
			table=table_name,
			columns=",".join(columns),
			values=cleaned_value_sets
		)

		self.execute(query)
