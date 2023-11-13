import json
import mysql.connector

class MySQLDatabase:
  def __init__(self, config_file):
    with open(config_file, "r") as file:
      self.config = json.load(file)

  def connect(self):
    try:
      db_config = self.config["database"]
      self.connection = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        auth_plugin='caching_sha2_password'
      )
      print("Connected to the database securely")
    except mysql.connector.Error as err:
      print(f"Error: {err}")

  def call_stp(self, stp, params=None, outcome = None):
    data = None
    if self.connection:
      cursor = self.connection.cursor()
      try:
        if outcome == 'output_params':
          data = cursor.callproc(stp) if params is None else cursor.callproc(stp, params)
        else:
          if params is None:
            cursor.callproc(stp)
          else:
            cursor.callproc(stp, params)
        
          for result in cursor.stored_results():
            data = result.fetchall()
        self.connection.commit()
        # print(data) #Looking inside the data
      except mysql.connector.Error as err:
        print(f"Error calling stored procedure: {err}")
      finally:
        cursor.close()
      return data
    else:
      print("Not connected to the database. Call the connect() method first.")

  # def call_stp_test(self, stp):
  #   # i=0
  #   if self.connection:
  #     cursor = self.connection.cursor()
  #     try:
  #       cursor.callproc(stp)
  #       for result in cursor.stored_results():
  #         # i += 1
  #         data = result.fetchall()

  #         # print(f"{i} & {data}")
  #     except mysql.connector.Error as err:
  #       print(f'Error calling stored procedure: {err}')
  #     finally:
  #       cursor.close()
  #   else:
  #     print('Not connected to the db')
  
  def close(self):
    if self.connection:
      self.connection.close()
      print("Database connection closed")
