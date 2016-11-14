"""
 Class Puzzle.
 This class is used to read data from text file and insert in database.
 
 @author Sanjeev Kumar <sanju.sci9@gmail.com>
"""
import sys, traceback
import string, MySQLdb, random, sys

class Puzzle:
	fileName = ''
	host_name = 'localhost'
	user_name = 'root'
	password = 'a'
	database = 'puzzle'
	
	"""
	 This is default constructor to assign file when class object inicate 
	"""
	def __init__(self, file_name):
		Puzzle.filename = file_name
	
	"""
	 Function db_connection
	 This function is used to connect database and return db connection object
	 
	 @author Sanjeev Kumar <sanju.sci9@gmail.com>
	"""
	def db_connection(self):
		 db = MySQLdb.connect(self.host_name, self.user_name, self.password, self.database)
		 return db

	'''
	  Function store_data
	  This function is used to read data from file and store data in db.
	  and get store data from db and calculate the wine assign to the person
	  
	  @author Sanjeev Kumar <sanju.sci9@gmail.com>
	'''
	def store_data(self):
		count = 0
		row = []
		wine_wishes = {}
		final_assignments = {}
		db = self.db_connection()
		# prepare a cursor object using cursor() method
		cursor = db.cursor()
		cursor.execute("""TRUNCATE TABLE wishlist""")
		with open(Puzzle.filename, 'r') as data:
			for index in data: 
				rows = index.split()
				person_id = int(string.replace(rows[0].lower(), 'person', ''))
				wine_id = int(string.replace(rows[1].lower(), 'wine', ''))
				row.append((person_id, wine_id))
				count += 1
				try:
				   if (count == 1000):
					   # Execute the SQL command
					   cursor.executemany("""INSERT INTO wishlist(pid,wid) VALUES (%s,%s)""", row)
					   count = 0;
					   row = []
					   # Commit your changes in the database
					   db.commit()
				except Exception, e:
					print 'Errors', e.args
				   # Rollback in case there is any error
					db.rollback()
		if count > 0:
			try:
				# Execute the SQL command
			    cursor.executemany("""INSERT INTO wishlist(pid,wid) VALUES (%s,%s)""", row)
			    count = 0;
			    row = []
			    # Commit your changes in the database
			    db.commit()
			except Exception, e:
				print 'Errors', e.args
			   # Rollback in case there is any error
				db.rollback()
		data.close()
		cursor.execute("""SELECT wid, count(wid) as `count` FROM wishlist group by wid ORDER BY `count` ASC""")
		sorted_wines = cursor.fetchall()
		cursor.execute("""SELECT wid, pid FROM wishlist ORDER BY wid ASC""")
		wines_data = cursor.fetchall()
		for row in wines_data:
			if int(row[0]) not in wine_wishes: #make wines as keys and people as values 
				wine_wishes[int(row[0])] = [] 
			wine_wishes[int(row[0])].append(int(row[1]))
		sorted_wines_count = []
		for row in sorted_wines:
			sorted_wines_count.append((int(row[0]),int(row[1])))
		wine_num = len(sorted_wines_count)
		wines_sold = 0
		while wine_num > 0:
			assign_wine = sorted_wines_count[0][0]
			random_index = random.randrange(len(wine_wishes[assign_wine]))
			sql = """SELECT count(pid) FROM assigment where pid = (%d)""" % (wine_wishes[assign_wine][random_index])
			cursor.execute(sql)
			result_count=cursor.fetchone()
			if int(result_count[0]) < 3:
					sql = """INSERT INTO assigment(pid,wid) VALUES (%d,%d)""" % (wine_wishes[assign_wine][random_index], assign_wine)
					try:
						cursor.execute(sql)
						db.commit()
					except Exception, e:
						print "Error", e.args
						db.rollback()
					wines_sold += 1 #unique wines sold for this sample dataset
			sorted_wines_count.pop(0) #delete lowest-frequent wine_wish. Every wine can only be assigned once.
			del wine_wishes[assign_wine] #delete the wine. Every wine can only be assigned once.
			wine_num -= 1
		
		# Write each element in final_assignments_sorted into a separate text file:"final_assignments.txt"
		f = open('final_assignments.txt', 'w')
		f.write("Total Unique Wines Sold:" + str(wines_sold) + "\n")
		cursor.execute("""SELECT wid, pid FROM wishlist ORDER BY pid ASC""")
		final_data = cursor.fetchall()
		for row in final_data:
			f.write('person' + str(row[0]) + "\t" + 'wine' + str(row[1]) + "\n") #row[0] is person_id, row[1] are wine_ids
		f.close()

file_name = sys.argv[1]
p = Puzzle(file_name)
p.store_data()
