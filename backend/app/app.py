from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_bcrypt import Bcrypt
import models
import datetime
from models import Tenants, Guards, Visits
import send_sms
from send_sms import send_sms
from flask_cors import CORS

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(tenant_id):
    return Tenants.query.get(int(tenant_id))

CORS(app)

class TenantsRegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    first_name = StringField(validators=[
                             InputRequired(), Length(max=50)], render_kw={"placeholder": "First Name"})
    last_name = StringField(validators=[
                            InputRequired(), Length(max=50)], render_kw={"placeholder": "Last Name"})
    email = StringField(validators=[
                        InputRequired(), Length(max=50)], render_kw={"placeholder": "Email"})
    phone = StringField(validators=[
                        InputRequired(), Length(max=20)], render_kw={"placeholder": "Phone Number"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    estate = StringField(validators=[
                        InputRequired(), Length(max=50)], render_kw={"placeholder": "Estate"})
    block = StringField(validators=[
                        InputRequired(), Length(max=20)], render_kw={"placeholder": "Block"})
    floor = IntegerField(validators=[
                         InputRequired()], render_kw={"placeholder": "Floor"})
    house_number = IntegerField(validators=[
                                InputRequired()], render_kw={"placeholder": "House Number"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = Tenants.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class GuardsRegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    first_name = StringField(validators=[
                             InputRequired(), Length(max=50)], render_kw={"placeholder": "First Name"})
    last_name = StringField(validators=[
                            InputRequired(), Length(max=50)], render_kw={"placeholder": "Last Name"})
    email = StringField(validators=[
                        InputRequired(), Length(max=50)], render_kw={"placeholder": "Email"})
    phone = StringField(validators=[
                        InputRequired(), Length(max=20)], render_kw={"placeholder": "Phone Number"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    employee_id = IntegerField(validators=[
                             InputRequired()], render_kw={"placeholder": "Employee ID"})
    submit = SubmitField('Register')
    def validate_employee_id(self, employee_id):
        existing_guard = Guards.query.filter_by(employee_id=employee_id.data).first()
        if existing_guard:
            raise ValidationError('An account with that employee ID already exists.')

    def validate_employee_id(self, employee_id):
        existing_guard = Guards.query.filter_by(employee_id=employee_id.data).first()
        if existing_guard:
            raise ValidationError('An account with that employee ID already exists.')

    # Rest of the form definition and validation logic

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class LogVisitForm(FlaskForm):
    visitor_first_name = StringField('First Name', validators=[DataRequired()])
    visitor_last_name = StringField('Last Name', validators=[DataRequired()])
    nickname = StringField('Nickname')
    phone = StringField('Phone Number', validators=[DataRequired()])
    visitor_destination = StringField('Visitor Destination', validators=[DataRequired()])
    # vehicle_plate = StringField('Vehicle Plate', validators=[DataRequired()])
    submit = SubmitField('Log Visitor')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        tenant = Tenants.query.filter_by(username=form.username.data).first()
        if tenant:
            if bcrypt.check_password_hash(tenant.password, form.password.data):
                login_user(tenant)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register/tenant', methods=['GET', 'POST'])
def register_tenant():
    form = TenantsRegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Tenants(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password,
            estate=form.estate.data,
            block=form.block.data,
            floor=form.floor.data,
            house_number=form.house_number.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register_tenant.html', form=form)

@app.route('/register/guard', methods=['GET', 'POST'])
def register_guard():
    form = GuardsRegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_guard = Guards(
            employee_id=form.employee_id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password
        )
        db.session.add(new_guard)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register_guard.html', form=form)

@app.route('/log-visitor', methods=['GET', 'POST'])
def log_visitor():
    form = LogVisitForm()
    if form.validate_on_submit():
        # Get the visitor details from the form
        visitor_first_name = form.visitor_first_name.data
        visitor_last_name = form.visitor_last_name.data
        nickname = form.nickname.data
        phone = form.phone.data
        visitor_destination = form.visitor_destination.data
        # vehicle_plate = form.vehicle_plate.data  # Access vehicle plate data

        # Create a new Visit object and save it to the database
        new_visit = Visits(
            visitor_first_name=visitor_first_name,
            visitor_last_name=visitor_last_name,
            nickname=nickname,
            phone=phone,
            visitor_destination=visitor_destination
        )
        db.session.add(new_visit)
        db.session.commit()

        # Get the most recent visit (assuming 'visit_id' is the primary key)
        most_recent_visit = Visits.query.order_by(Visits.visit_id.desc()).first()

        # Extract and format the visit time for the SMS (if needed)
        if most_recent_visit:
            most_recent_visit_time = most_recent_visit.visit_time.strftime("%d/%m/%Y %H:%M:%S")  # Example format
        # Send the SMS to the visitor's phone number (implementation details omitted)
        visitor_name = visitor_first_name + " " + visitor_last_name
        
        send_sms_instance = send_sms()
        send_sms_instance.sending(visitor_name, visitor_destination, phone, most_recent_visit_time)

        flash('Visitor logged successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('logvisitor.html', form=form)


if __name__ == "__main__":
    #create all tables
    db.create_all()
    app.run(debug=True)
