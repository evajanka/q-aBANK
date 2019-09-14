import data_manager
import psycopg2
from forms import RegsitrationForm, LoginForm
from flask import Flask, render_template, request, redirect, url_for, flash, session
import bcrypt

app = Flask(__name__)
app.secret_key = 'f55b0595286fcfa85e6592f09e07cef4'

@app.route('/', methods=['POST', 'GET'])
def homepage():
    sort = 'submission_time'
    if request.args:
        if 'id' in request.args:
            return render_template('answer.html')
        if "search" in request.args:
            search = request.args['search']
            result = data_manager.search_by_title(search)
            return render_template('/delete_question_by_id.html', result=result)
        else:
            sort = request.args['order_by']
    header = ["ID", "SUBMISSION TIME", "VIEW NUMBER", "VOTE NUMBER", "TITLE", "USERNAME", "ANSWER"]
    questions = data_manager.display(sort, limit=5)

    return render_template('new_display.html', sort=sort, questions=questions, header=header, title="homepage")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegsitrationForm()
    if form.is_submitted():
        try:
            hashed_password = (bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
            username = form.username.data
            data_manager.register_new_account(username, hashed_password)
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))
        except psycopg2.Error as error:
            flash('Username already taken!', 'danger')
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        usernames = data_manager.display_users()
        existing_users = [user["username"] for user in usernames]
        if username in existing_users:
            password = form.password.data
            hashed_password = data_manager.get_pw(username)
            for element in hashed_password:
                hashed_password = element['password']
            hashed_bytes_password = hashed_password.encode('utf-8')
            verify_password = bcrypt.checkpw(password.encode('utf-8'), hashed_bytes_password)
            if verify_password is True:
                flash('You are logged in!', 'success')
                session['logged in'] = True
                session['username'] = username
                return redirect('homepage')
            else:
                flash('Login Failed! Please check username and password', 'danger')
        else:
            flash('Login Failed! Please check username and password', "danger")
    return render_template('login.html', form=form, title='Login')


@app.route("/logout")
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    flash('You logged out!', 'success')
    return redirect(url_for('homepage'))


@app.route('/search_bar', methods=['POST', 'GET'])
def search():
    if "search" in request.args:
        search = request.args['search']
        result = data_manager.search_by_title(search)
        return render_template('/delete_question_by_id.html', result=result)
    return render_template('search_bar.html')


@app.route('/homepage')
def list_all_questions():
    header = ["ID", "SUBMISSION TIME", "VIEW NUMBER", "VOTE NUMBER", "TITLE", "USERNAME", "ANSWER"]
    questions = data_manager.display(limit=None)
    return render_template('new_display.html', questions=questions, header=header, title="All questions")


@app.route('/add_question', methods=['POST', 'GET'])
def add_question():
    s = session.get('logged_in', False)
    if request.method == 'POST':
        if s is True:
            title = request.form['title']
            message = request.form['message']
            data_manager.add_question(title, message, session['username'])
            return redirect(url_for('homepage'))
        else:
            flash('You are not logged in!', 'danger')
    return render_template('add_question.html', title="Ask new question")


@app.route('/?search=', methods=['POST', 'GET'])
def delete():
    if session.get('logged_in', True):
        if request.method == 'POST':
            username = session['username']
            id_for_delete = int(request.form['delete'])
            data_manager.delete_answers_by_id(id_for_delete)
            data_manager.delete_question_by_id(id_for_delete, username)
            flash(f'Question with id {id_for_delete} is deleted', 'success')
            return redirect(url_for('homepage'))
    else:
        flash('Please log in!', 'danger')
        return redirect(url_for('login'))

@app.route('/answer', methods=['POST', 'GET'])
def disp_answers():
    id = request.args['id']
    header = ["ID", "QUESTION ID", "VIEW NUMBER", "VOTE NUMBER", "ANSWER"]
    answer = data_manager.display_answers_by_id(id)
    question = data_manager.display_question(id)
    return render_template('answer.html', answer=answer, header=header, id=id, question=question)


@app.route('/add_answer', methods=['POST', 'GET'])
def add_answer():
    question_id = request.args['id']
    s = session['logged_in']
    if request.method == 'POST':
        if s is True:
            message = request.form['message']
            data_manager.add_answer(question_id, message, session['username'])
            return redirect(url_for("disp_answers", id=question_id))
        else:
            flash('You are not logged in!', 'danger')

    return render_template('answer.html', question_id=question_id)


@app.route("/users")
def all_users():
    users = data_manager.display_users()
    return render_template('users.html', users=users, title='users')


@app.route("/user_data")
def user_data():
    username = request.args["username"]
    questions = data_manager.questions_of_user(username)
    answers = data_manager.answers_of_user(username)
    header = ["QUESTION ID", "QUESTION TITLE", "MESSAGE", "SUBMISSION TIME"]
    return render_template("user_data.html", username=username, header=header, questions=questions, answers=answers, title='user_data')


if __name__ == '__main__':
    app.run(debug=True)