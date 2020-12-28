import psycopg2 


class DBHelper:

	def __init__(self):
		global conn
		conn = psycopg2.connect(
					   host = "",
					   database = "",
					   user = "",
					   password = "")
		conn.set_session(autocommit = True)
		cur = conn.cursor()

	def setup(self):
		stmt = "CREATE TABLE IF NOT EXISTS Attendence (user_id integer UNIQUE , Name text, Physics integer, Chemistry integer, Maths integer, CPrograming integer, TotalAttendedlecture integer, Totallecture integer, Percentage integer, Email_id text)"
		cur = conn.cursor()
		cur.execute(stmt)
		conn.commit()

	def updatep(self, user_id):
		command = "UPDATE Attendence SET Physics=Physics+1 WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		conn.commit()

	def updatec(self, user_id):
		command = "UPDATE Attendence SET Chemistry = Chemistry+1 WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		conn.commit()

	def updatem(self, user_id):
		command = "UPDATE Attendence SET Maths = Maths+1 WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		conn.commit()

	def updatecp(self, user_id):
		command = "UPDATE Attendence SET CPrograming = CPrograming+1 WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		conn.commit()

	def newUser(self, user_id, Name):
		command = "SELECT * FROM Attendence WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		record = cur.fetchone()
		if record is None:
			stmt = "INSERT INTO Attendence VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			zerovalue = 0
			args = (user_id, Name, zerovalue, zerovalue, zerovalue, zerovalue, zerovalue, zerovalue, zerovalue)
			cur.execute(stmt, args)
			conn.commit()

	def updatelec(self, user_id):
		command = "UPDATE Attendence SET TotalAttendedlecture = TotalAttendedlecture+1 WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		conn.commit()

	def updateall(self, user_id):
		command = "UPDATE Attendence SET Totallecture = Totallecture+4 WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		conn.commit()

	def percent(self, user_id):
		command = "SELECT TotalAttendedlecture FROM Attendence WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		record = cur.fetchone()
		result = int(record[0])
		command1 = "SELECT Totallecture FROM Attendence WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command1, args)
		record1 = cur.fetchone()
		result1 = int(record1[0])
		x = ((1.0*result/result1)*100.0)
		command2 = "UPDATE Attendence SET Percentage =%s WHERE user_id = (%s)"
		args = (x, user_id)
		cur.execute(command2, args)
		conn.commit()

	def add_item(self, Name, DATE):
		stmt = "INSERT INTO Events (Name,DATE) VALUES (%s,%s)"
		args = (Name, DATE)
		cur = conn.cursor()
		cur.execute(stmt, args)
		conn.commit()


	def delete_item(self, Name):
		stmt = "DELETE FROM Events WHERE Name = (%s)"
		args = (Name, )
		cur = conn.cursor()
		cur.execute(stmt, args)
		conn.commit()

	def get_item(self):
		stmt = "SELECT * FROM Events"
		cur = conn.cursor()
		cur.execute(stmt)
		record = cur.fetchall()
		return record

	def getitems(self, user_id):
		command = "SELECT Percentage FROM Attendence WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		record = cur.fetchone()
		result = round(float(record[0]), 2)
		return result

	def get_item1(self):
		stmt = "SELECT * FROM Experiments"
		cur = conn.cursor()
		cur.execute(stmt)
		record = cur.fetchall()
		return record

	def getpdf(self, user_id):
		stmt = "SELECT * FROM Attendence WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(stmt, args)
		record = cur.fetchone()
		return record

	def newEmail(self, user_id):
		command = "SELECT Email_id FROM Attendence WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		result = cur.fetchone()
		return result

	def updateemail(self, user_id, Email_id):
		command = "SELECT Email_id FROM Attendence WHERE user_id = (%s)"
		args = (user_id, )
		cur = conn.cursor()
		cur.execute(command, args)
		result = cur.fetchone()
		result = list(result)
		if result is None:
			command2 = "INSERT OR REPLACE INTO Attendence (user_id,Name,Physics,Chemistry,Maths,CPrograming,TotalAttendedlecture,Totallecture,Percentage,Email_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			args = (result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],Email_id)
			cur.execute(command2, args)
			conn.commit()
		else:
			command1 = "UPDATE Attendence SET Email_id = %s WHERE user_id = %s"
			args = (Email_id, user_id)
			cur.execute(command1, args)
			conn.commit()
	

