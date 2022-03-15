from flask import Flask, render_template, redirect, request, make_response, jsonify
from data import db_session, jobs_api, users_api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from forms.login import LoginForm
from forms.registration import RegisterForm
from data.jobs import Job
from forms.add_job import AddJob
from forms.edit_job import EditJob
from forms.add_departament import AddDepartment
from forms.edit_department import EditDepartment
from data.departments import Department
from flask_restful import Api
from data import users_resource
from data import jobs_resource
from waitress import serve
from os import environ
from data.categories import Category

app = Flask(__name__)
api = Api(app)
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('db/Mars_colonization_mission.sqlite')
app.register_blueprint(jobs_api.blueprint)
app.register_blueprint(users_api.blueprint)
db_sess = db_session.create_session()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Incorrect login or password", form=form, title='Authorization',
                               login=1)
    return render_template('login.html', title='Authorization', form=form, login=1)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration', form=form, message="Passwords do not match",
                                   register=1)
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration', form=form, message="This user already exists",
                                   register=1)
        user = User(surname=form.surname.data, name=form.name.data, age=form.age.data, position=form.position.data,
                    speciality=form.speciality.data, address=form.address.data, email=form.email.data,
                    city_from=form.city_from.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form, register=1)


@app.route('/jobs')
@login_required
def jobs():
    users = {}
    for i in db_sess.query(User):
        users[i.id] = f'{i.surname} {i.name}'
    access = []
    for job in db_sess.query(Job):
        access += [job.team_leader == current_user.id or current_user.id == 1]
    return render_template("jobs.html", jobs=db_sess.query(Job), users=users, title='Works log', access=access)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    open("users.txt", "w").writelines([f'{user.id} {user.surname} {user.name}\n' for user in db_sess.query(User)])
    form = AddJob()
    if form.validate_on_submit():
        job = Job(team_leader=form.team_leader.data, job=form.job.data, work_size=form.work_size.data,
                  collaborators=form.collaborators.data, start_date=form.start_date.data, end_date=form.end_date.data,
                  is_finished=form.is_finished.data)
        db_sess.add(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/jobs')
    return render_template("add_job.html", title='Adding a job', add_job=1, form=form)


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    open("users.txt", "w").writelines([f'{user.id} {user.surname} {user.name}\n' for user in db_sess.query(User)])
    form = EditJob()
    job = db_sess.query(Job).filter(Job.id == id).first()
    if request.method == "GET":
        if job:
            form.team_leader.data = job.team_leader
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.start_date.data = job.start_date
            form.end_date.data = job.end_date
            form.is_finished.data = job.is_finished
    if form.validate_on_submit():
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/jobs')
    return render_template('edit_job.html', title='Editing a job', form=form)


@app.route('/delete_job/<int:id>')
@login_required
def delete_job(id):
    db_sess.delete(db_sess.query(Job).filter(Job.id == id).first())
    db_sess.commit()
    return redirect('/jobs')


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    open("users.txt", "w").writelines([f'{user.id} {user.surname} {user.name}\n' for user in db_sess.query(User)])
    form = AddDepartment()
    if form.validate_on_submit():
        department = Department(title=form.title.data, chief=form.chief.data, members=form.members.data,
                                email=form.email.data)
        db_sess.add(department)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template("add_department.html", title='Adding a department', add_department=1, form=form)


@app.route('/departments')
@login_required
def departments():
    users = {}
    for i in db_sess.query(User):
        users[i.id] = f'{i.surname} {i.name}'
    access = []
    for department in db_sess.query(Department):
        access += [department.chief == current_user.id or current_user.id == 1]
    return render_template("departments.html", departments=db_sess.query(Department), users=users,
                           title='List of departments', access=access)


@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    open("users.txt", "w").writelines([f'{user.id} {user.surname} {user.name}\n' for user in db_sess.query(User)])
    form = EditDepartment()
    department = db_sess.query(Department).filter(Department.id == id).first()
    if request.method == "GET":
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
    if form.validate_on_submit():
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
    return render_template('edit_department.html', title='Editing a department', form=form)


@app.route('/delete_department/<int:id>')
@login_required
def delete_department(id):
    db_sess.delete(db_sess.query(Department).filter(Department.id == id).first())
    db_sess.commit()
    return redirect('/departments')


@app.route('/')
def base():
    return render_template("base.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.errorhandler(401)
def unauthorized(error):
    return render_template("unauthorized.html")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(environ.get("PORT", 5000)))
