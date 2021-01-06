from connector.connectMysql import db

cursor = db.cursor()


def insert_user(username, password, name, user_type):
    cursor.execute("insert into user (username, password, name, user_type)"
                   " values ('%s', '%s', '%s', '%s')" % (username, password, name, user_type))
