import connect_database
import util

from flask import Flask

app = Flask(__name__)


@connect_database.connection_handler
def display(cursor, sort='submission_time', order='DESC', limit=5):
    if limit == None:
        limit = ""
    else:
        limit = f'LIMIT {limit}'

    query = """SELECT id, submission_time, view_number, vote_number, title, username FROM question
                ORDER BY {0} {1} {2};""".format(sort, order, limit)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@connect_database.connection_handler
def display_question(cursor, id):
    query = """SELECT id, submission_time, view_number, vote_number, title, username, message FROM question
                    WHERE id ='{0}';""".format(id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result



@connect_database.connection_handler
def search_by_title(cursor, search):
    search = str(search)
    query = """SELECT * FROM question
                WHERE title LIKE '%{0}%' ;""".format(search)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


@connect_database.connection_handler
def add_question(cursor, title, message, username):
    submission_time = util.current_time()
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, username)
                 VALUES (%s, 0, 0, %s, %s, %s);""",
                 (submission_time, title, message, username))


@connect_database.connection_handler
def add_answer(cursor, question_id, message, username):
    submission_time = util.current_time()
    cursor.execute("""INSERT INTO answer (submission_time, vote_number, question_id, message, username)
                 VALUES (%s, 0, %s, %s, %s);""",
                 (submission_time, question_id, message, username))


@connect_database.connection_handler
def delete_answers_by_id(cursor,id):
    cursor.execute("""DELETE FROM answer
                    WHERE question_id ='{0}';""".format(id))


@connect_database.connection_handler
def delete_question_by_id(cursor, id, username):
    cursor.execute("""DELETE FROM question
                    WHERE id ='{0}'
                    AND username LIKE '{1}';""".format(id, username))


@connect_database.connection_handler
def register_new_account(cursor, username, password):
        cursor.execute("""INSERT INTO users (created_at, username, password)
                 VALUES (CURRENT_TIMESTAMP, %s, %s);""",
                       (username, password))


@connect_database.connection_handler
def get_pw(cursor, user_name):
        query = """SELECT password FROM users
                                WHERE username = '{0}';""".format(user_name)
        cursor.execute(query)
        result = cursor.fetchall()
        return result


@connect_database.connection_handler
def display_answers_by_id(cursor, id):
    query = """SELECT * FROM answer

                WHERE question_id = '{0}' ;""".format(id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


@connect_database.connection_handler
def display_users(cursor):
    query = """SELECT * FROM users;"""
    cursor.execute(query)
    result = cursor.fetchall()
    return result


@connect_database.connection_handler
def questions_of_user(cursor, username):
    query = """SELECT id, title, message, submission_time FROM question
                WHERE username LIKE '{0}';""".format(username)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


@connect_database.connection_handler
def answers_of_user(cursor, username):
    query = """SELECT answer.question_id, question.title, answer.message, answer.submission_time FROM answer
                JOIN question
                ON answer.question_id = question.id                
                WHERE answer.username LIKE '{0}';""".format(username)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


#@connect_database.connection_handler
#def delete_question_and_answer(cursor, username, id):
#    query = """DELETE FROM question INNER JOIN answer
#                ON question.id = answer.question.id
#               WHERE question.username LIKE '{0}' AND question.id = '{1}';""".format(username, id)
#   cursor.execute(query)




