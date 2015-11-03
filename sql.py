import sqlite3

with sqlite3.connect("blog.db") as connection:
	c = connection.cursor()

	c.execute("""CREATE TABLE posts
				(title TEXT, post TEXT)
			  """)

	#insert dummy data
	c.execute('INSERT INTO posts VALUES("First", "First post")')
	c.execute('INSERT INTO posts VALUES("2nd", "I\'m the second post")')
	c.execute('INSERT INTO posts VALUES("Threee", "3rd post goes here")')

	