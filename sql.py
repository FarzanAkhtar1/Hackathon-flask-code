import sqlite3
from mysql.connector import connect, Error

global superHost, superUser, superPassword

superHost = "localhost"
superUser = "farzan"
superPassword = "farzan"

def execQuery(host, user, password, database, sqlQuery):
    try:
        with connect( 
            host= host,
            user= user,
            password = password,
            database= database
        ) as connection: #formulates a query to write to the database 
            queryToWrite = sqlQuery  #forming query
            with connection.cursor() as cursor:
                cursor.execute(queryToWrite)
                connection.commit() #commiting query. Required.    
    except Exception as e:
        print(e)

def fetchQuery(host, user, password, database, sqlQuery):
    try:
        with connect( 
            host= host,
            user= user,
            password = password,
            database= database
        ) as connection: #formulates a query to write to the database 
            queryToWrite = sqlQuery  #forming query
            with connection.cursor() as cursor:
                cursor.execute(queryToWrite)
                posts = [dict(title=row[0], description=row[1]) for row in cursor]
                #print(posts)
                return posts
                for x in cursor:
                    print(x)
                #connection.commit() #commiting query. Required.   
    except Exception as e:
        print(e)

#results = fetchQuery("locahost", "farzan", "farzan", "circle", "select * from posts")
#results = fetchQuery(superHost, superUser, superPassword, "circle", "select * from posts")

#print(results)
# print(results)
# for x in results:
#     print(x)

#execQuery(superHost, superUser, superPassword, "circle", """CREATE TABLE posts(title TEXT, description TEXT)""")
#execQuery(superHost, superUser, superPassword, "circle", 'INSERT INTO posts VALUES("Good", "I am good.")')

# with sqlite3.connect("sample.db") as connection:
#     c = connection.cursor()
#     c.execute("""DROP TABLE posts""")
#     c.execute("""CREATE TABLE posts(title TEXT, description TEXT)""")
#     c.execute('INSERT INTO posts VALUES("Good", "I am good.")')
#     c.execute('INSERT INTO posts VALUES("Well", "I am well.")')
