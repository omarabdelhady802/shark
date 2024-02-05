from flask import Flask, render_template, request, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///limo.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Models
class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    orders = db.relationship('Orders', backref='cars', lazy=True ,cascade='all, delete-orphan')

class Drivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    add = db.Column(db.String(100), nullable=False, unique=True)
    typee = db.Column(db.String(50), nullable=False, unique=True)
    num = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Orders', backref='drivers', lazy=True,cascade='all, delete-orphan')
    
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(50))
    typee = db.Column(db.String(100))
    day = db.Column(db.String(50))
    price = db.Column(db.Integer, )
    date = db.Column(db.Date, nullable=False)
    
class Edit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    typee = db.Column(db.String(100))
    killo = db.Column(db.String(100))
    company = db.Column(db.String(50))
    price = db.Column(db.Integer, )
    date = db.Column(db.Date, nullable=False)
    
class Customers(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    number = db.Column(db.Integer, nullable=False)
    number1 = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Orders', backref='customers', lazy=True,cascade='all, delete-orphan')

class Companies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    credit = db.Column(db.Integer, nullable=False)
    depit = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Orders', backref='companies', lazy=True,cascade='all, delete-orphan')
    fatoras = db.relationship('Fatoras', backref='companies', lazy=True,cascade='all, delete-orphan')

class Fatoras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pickup_time = db.Column(db.Date, nullable=False)
    company_name = db.Column(db.String(50), nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    depit = db.Column(db.Integer, nullable=False)
    final = db.Column(db.Integer, nullable=False)
    company_id =db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    from_ = db.Column(db.String(50), nullable=False)
    typee = db.Column(db.String(50), nullable=False)
    way = db.Column(db.String(50), nullable=False)
    to = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(50), nullable=False)
    num = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time =  db.Column(db.String(50), nullable=False)
    
   

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='user')
    orders = db.relationship('Orders', backref='users', lazy=True,cascade='all, delete-orphan')
    
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(750), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pickup_time = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    fromm = db.Column(db.String(70))
    to = db.Column(db.String(70))
    typee = db.Column(db.String(70))
    company_name = db.Column(db.String(50), nullable=False)
    driver_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    customer_name = db.Column(db.String(50), nullable=False)
    car_name = db.Column(db.String(50), nullable=False)
    office_name = db.Column(db.String(70))
    payment = db.Column(db.String(50))
    note = db.Column(db.String(50))
    total = db.Column(db.Integer, nullable=False)
    car = db.Column(db.Integer, nullable=False)
    sub = db.Column(db.Integer, nullable=False)
    office = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.Integer, nullable=False)
    driver = db.Column(db.Integer, nullable=False)
    final = db.Column(db.Integer, nullable=False)
    company_id =db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    driver_id =db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    user_id =db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    car_id =db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    customer_id =db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    
    
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
# Routes
@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username =request.form.get('username')
        password =request.form.get('password')
        
        user = Users.query.filter_by(name=username, password=password).first()

        if user:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('cars'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('index.html')

@app.route('/cars')
@login_required
def cars():
        cars_list = Cars.query.order_by(Cars.id.desc()).limit(10).all()

        return render_template('cars.html', cars=cars_list)
    
@app.route('/edits')
@login_required
def edits():
        cars_list = Edit.query.order_by(Edit.id.desc()).limit(10).all()

        return render_template('edits.html', cars=cars_list)
    
@app.route('/work')
@login_required
def work():
        cars_list = Work.query.order_by(Work.id.desc()).limit(10).all()

        return render_template('work.html', cars=cars_list)
   
        

@app.route('/books')
@login_required
def books():
    now = datetime.utcnow()
    five_days_from_now = now + timedelta(days=5)

    now_str = now.strftime('%Y-%m-%d')
    five_days_from_now_str = five_days_from_now.strftime('%Y-%m-%d')
    booking_list = Booking.query.filter(Booking.date.between(now_str, five_days_from_now_str)).all()
    return render_template('booking.html', cars=booking_list)

@app.route('/drivers')
@login_required
def drivers():
    drivers_list = Drivers.query.order_by(Drivers.id.desc()).limit(10).all()

    return render_template('drivers.html', drivers=drivers_list)

@app.route('/customers')
@login_required
def customers():
    customers_list = Customers.query.order_by(Customers.id.desc()).limit(10).all()

    return render_template('customers.html', customers=customers_list)

@app.route('/companies')
@login_required
def companies():
    companies_list = Companies.query.order_by(Companies.id.desc()).limit(10).all()

    return render_template('companies.html', companies=companies_list)



@app.route('/fatoras')
@login_required
def fatoras():
    fatoras_list = Fatoras.query.order_by(Fatoras.id.desc()).limit(10).all()

    return render_template('fatoras.html', fatoras=fatoras_list)
@app.route('/users')
@login_required
def users():
    users_list = Users.query.all()
    return render_template('users.html', users=users_list)
@app.route('/notes')
@login_required
def notes():
    notes_list = Notes.query.all()
    return render_template('notes.html', notes=notes_list)

@app.route('/orders')
@login_required
def orders():
    orders_list = Orders.query.order_by(Orders.id.desc()).limit(10).all()

    return render_template('orders.html', orders=orders_list)

@app.route('/cars/new', methods=['GET', 'POST'])
@login_required
def new_car():
    if request.method == 'POST':
        name = request.form.get('name')
        new_car = Cars(name=name)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('cars'))

    return render_template('new_car.html')

@app.route('/work/new', methods=['GET', 'POST'])
@login_required
def new_work():
    if request.method == 'POST':
        name = request.form.get('name')
        typee = request.form.get('type')
        day = request.form.get('day')
        price = request.form.get('price')
        date = request.form.get('date')
        my_date = datetime.strptime(date, '%Y-%m-%d').date()
        new_car = Work(car_name=name ,typee =typee ,day = day , price =price ,date = my_date )
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('work'))

    return render_template('new_work.html')

@app.route('/edit/new', methods=['GET', 'POST'])
@login_required
def new_edit():
    if request.method == 'POST':
        name = request.form.get('name')
        typee = request.form.get('type')
        day = request.form.get('day')
        price = request.form.get('price')
        killo = request.form.get('killo')
        company = request.form.get('company')
        date = request.form.get('date')
        my_date = datetime.strptime(date, '%Y-%m-%d').date()
        new_car = Edit(name=name ,typee =typee , price =price ,date = my_date, killo = killo ,company = company )
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('edits'))

    return render_template('new_edit.html')

@app.route('/books/new', methods=['GET', 'POST'])
@login_required
def new_book():
    if request.method == 'POST':
        name = request.form.get('name')
        from_ = request.form.get('from')
        to = request.form.get('to')
        num = request.form.get('num')
        date = request.form.get('date')
        typee = request.form.get('typee')
        way = request.form.get('way')
        price = request.form.get('price')
        time = request.form.get('time')
        note = request.form.get('note')
        my_date = datetime.strptime(date, '%Y-%m-%d').date()
        new_book = Booking(name=name,from_ = from_ , to = to ,date = my_date, num = num,way = way,typee =typee,
                           price = price , time = time , note =note)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books'))

    return render_template('new_book.html')

@app.route('/search/book', methods=['GET', 'POST'])
@login_required
def search_book():
    if request.method == 'POST':
        from_ = request.form.get('from')
        to = request.form.get('to')
        my_date_from = datetime.strptime(from_, '%Y-%m-%d').date()
        my_date_to = datetime.strptime(to, '%Y-%m-%d').date()
        result = Booking.query.filter(Booking.date.between(my_date_from, my_date_to)).all()
        return render_template('search_result.html' , result = result)

    return render_template('search_book.html')

@app.route('/search/work', methods=['GET', 'POST'])
@login_required
def work_report():
    if request.method == 'POST':
        from_ = request.form.get('from')
        to = request.form.get('to')
        my_date_from = datetime.strptime(from_, '%Y-%m-%d').date()
        my_date_to = datetime.strptime(to, '%Y-%m-%d').date()
        result = Work.query.filter(Work.date.between(my_date_from, my_date_to)).all()
        f = 0
        for i in result :
            f += i.price
        return render_template('search_work.html' , result = result , f = f)

    return render_template('search_woorks.html')

@app.route('/search/edit', methods=['GET', 'POST'])
@login_required
def edit_report():
    if request.method == 'POST':
        from_ = request.form.get('from')
        name = request.form.get('name')
        to = request.form.get('to')
        my_date_from = datetime.strptime(from_, '%Y-%m-%d').date()
        my_date_to = datetime.strptime(to, '%Y-%m-%d').date()
        result = Edit.query.filter(Edit.date.between(my_date_from, my_date_to),Edit.name == name).all()
        f = 0
        for i in result :
            f += i.price
        return render_template('result_edit.html' , result = result , f = f)

    return render_template('search_edit.html')

@app.route('/users/new', methods=['GET', 'POST'])
@login_required
def new_user():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role')
        new_car = Users(name=name , password = password,role=role)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('users'))

    return render_template('new_user.html')

@app.route('/companies/new', methods=['GET', 'POST'])
@login_required
def new_company():
    if request.method == 'POST':
        name = request.form.get('name')
        depit = request.form.get('rec')
        credit = request.form.get('pay')
        total = (int(credit) - int(depit))
        new_car = Companies(name=name , credit=credit ,depit=depit , total =total  )
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('companies'))

    return render_template('new_company.html')

@app.route('/fatoras/new', methods=['GET', 'POST'])
@login_required
def new_fatora():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        depit = request.form.get('rec')
        credit = request.form.get('pay')
        my_date = datetime.strptime(date, '%Y-%m-%d').date()
        total = (int(depit) - int(credit))
        company_id = Companies.query.filter(Companies.name.like(name)).first()
        new_car = Fatoras(pickup_time = my_date ,company_name=name , credit=credit ,depit=depit , final =total,company_id=company_id.id )
        car = Companies.query.filter(Companies.name.like(f"%{name}%")).first()
        car.depit = int(car.depit) - int(credit)
        car.credit = int(car.credit) - int(depit)
        car.total = int(car.credit) - int(car.depit)
        
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('fatoras'))
    companies_list = Companies.query.all()

    return render_template('new_fatora.html',company = companies_list)


@app.route('/orders/new', methods=['GET', 'POST'])
@login_required
def new_order():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        from_ = request.form.get('from')
        to = request.form.get('to')
        type_ = request.form.get('type')
        driver_name = request.form.get('driver_name')
        user_name = current_user.name
        customer_name = request.form.get('customer_name')
        car_name = request.form.get('car_name')
        office_name = request.form.get('office_name')
        total_mony = request.form.get('total_mony')
        car_money = request.form.get('car_money')
        office_money = request.form.get('office_money')
        fuel = request.form.get('fuel')
        driver_money = request.form.get('driver_money')
        date = request.form.get('date')
        payment = request.form.get('payment')
        note = request.form.get('note')
        
        
        my_date = datetime.strptime(date, '%Y-%m-%d').date()
        # car = Companies.query.filter(Companies.name == name).first()
        company_id = Companies.query.filter(Companies.name.like(f"%{company_name}%")).first()
        driver_id =  Drivers.query.filter(Drivers.name.like(f"%{driver_name}%")).first()
        user_id =Users.query.filter(Users.name.like(f"%{user_name}%")).first()
        car_id =Cars.query.filter(Cars.name.like(f"%{car_name}%")).first()
        customer_id = Customers.query.filter(Customers.name.like(f"%{customer_name}%")).first()
        if payment == "اجل":
            company_id.credit += int(total_mony)
            company_id.total = int(company_id.credit) - int(company_id.depit)
            
            db.session.commit()
        
        new_car = Orders(pickup_time = my_date ,
                         fromm = from_ ,
                         to = to ,
                         typee = type_ ,
                         note = note,
                         company_name = company_name,
                         driver_name = driver_name,
                         user_name = user_name,
                         customer_name = customer_name,
                         car_name = car_name,
                         office_name = office_name,
                         payment = payment,
                         total = int(total_mony),
                         car = int(car_money),
                         sub = (int(total_mony)-int(car_money)),
                         office = int(office_money),
                         fuel = int(fuel),
                         driver = int(driver_money),
                         final = (int(car_money)-int(office_money)-int(fuel)-int(driver_money)),
                         company_id =company_id.id,
                         driver_id =driver_id.id,
                         user_id =user_id.id,
                         car_id =car_id.id,
                         customer_id =customer_id.id,)
        
        
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('orders'))
    companies_list = Companies.query.all()
    cars_list = Cars.query.all()
    drivers_list = Drivers.query.all()
    cust_list = Customers.query.all()
    users_list = Users.query.all()
    return render_template('new_order.html',company = companies_list , car = cars_list , driver = drivers_list
                           ,customer = cust_list,user = users_list)


@app.route('/drivers/new', methods=['GET', 'POST'])
@login_required
def new_driver():
    if request.method == 'POST':
        name = request.form.get('name')
        num = request.form.get('num')
        add = request.form.get('add')
        typee = request.form.get('typee')
        new_driver = Drivers(name=name,num=num,add=add,typee=typee)
        db.session.add(new_driver)
        db.session.commit()
        return redirect(url_for('drivers'))

    return render_template('new_driver.html')

@app.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    if request.method == 'POST':
        typee = request.form.get('type')
        name = request.form.get('name')
        from_ = request.form.get('from')
        to = request.form.get('to')
        my_date_from = datetime.strptime(from_, '%Y-%m-%d').date()
        my_date_to = datetime.strptime(to, '%Y-%m-%d').date()
        total = 0
        car = 0
        sub = 0
        office = 0
        fuel = 0
        driver = 0
        total_car = 0
        final = 0   
        times = 0
        if typee == "سيارات" :
            result = Orders.query.filter(Orders.pickup_time.between(my_date_from, my_date_to), Orders.car_name == name).all()
                
        elif typee == "شركات" :
            result = Orders.query.filter(Orders.pickup_time.between(my_date_from, my_date_to), Orders.company_name == name).all()
            
        elif typee == "عملاء" :
            result = Orders.query.filter(Orders.pickup_time.between(my_date_from, my_date_to), Orders.customer_name == name).all()
            
        elif typee == "مستخدمين" :
            result = Orders.query.filter(Orders.pickup_time.between(my_date_from, my_date_to), Orders.user_name == name).all()
        else:
            result = Orders.query.filter(Orders.id == -1).all()  
        for i in result:
            total += i.total
            car += i.car
            sub += i.sub
            office += i.office
            fuel += i.fuel
            driver += i.driver
            final += i.final
            times +=1
        return render_template('results.html', result = result, total = total , car = car , sub = sub ,office=office
                               ,fuel = fuel,driver=driver,final = final,times = times)
        

    return render_template('reports.html')

@app.route('/notes/new', methods=['GET', 'POST'])
@login_required
def new_note():
    if request.method == 'POST':
        name = request.form.get('name')
        date1 = request.form.get('date')
        date = datetime.strptime(date1, '%Y-%m-%d').date()
        new_driver = Notes(name=name,date=date)
        db.session.add(new_driver)
        db.session.commit()
        return redirect(url_for('notes'))

    return render_template('new_note.html')


@app.route('/customers/new', methods=['GET', 'POST'])
@login_required
def new_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        num = request.form.get('num')
        num1 = request.form.get('num1')
        new_driver = Customers(name=name , number = num,number1 = num1 )
        db.session.add(new_driver)
        db.session.commit()
        return redirect(url_for('customers'))

    return render_template('new_customer.html')



@app.route('/cars/edit/<int:car_id>', methods=['GET', 'POST'])
@login_required
def edit_car(car_id):
    car = Cars.query.get_or_404(car_id)

    if request.method == 'POST':
        car.name = request.form.get('name')
        db.session.commit()
        return redirect(url_for('cars'))

    return render_template('edit_car.html', car=car)

@app.route('/work/edit/<int:work_id>', methods=['GET', 'POST'])
@login_required
def edit_work(work_id):
    car = Work.query.get_or_404(work_id)

    if request.method == 'POST':
        car.car_name = request.form.get('name')
        car.typee = request.form.get('type')
        car.day = request.form.get('day')
        car.price = request.form.get('price')
        car.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        db.session.commit()
        return redirect(url_for('work'))

    return render_template('edit_work.html', car=car)

@app.route('/edit/edit/<int:edit_id>', methods=['GET', 'POST'])
@login_required
def edit_edit(edit_id):
    car = Edit.query.get_or_404(edit_id)

    if request.method == 'POST':
        car.car_name = request.form.get('name')
        car.typee = request.form.get('type')
        car.day = request.form.get('day')
        car.price = request.form.get('price')
        car.company = request.form.get('company')
        car.killo = request.form.get('killo')
        car.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        db.session.commit()
        return redirect(url_for('edits'))

    return render_template('edit_edit.html', car=car)

@app.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
@login_required
def edit_company(company_id):
    car = Companies.query.get_or_404(company_id)

    if request.method == 'POST':
        car.name = request.form.get('name')
        db.session.commit()
        return redirect(url_for('companies'))

    return render_template('edit_company.html', car=car)


@app.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    car = Customers.query.get_or_404(customer_id)

    if request.method == 'POST':
        car.name = request.form.get('name')
        car.number = request.form.get('num')
        car.number1 = request.form.get('num1')
        db.session.commit()
        return redirect(url_for('customers'))

    return render_template('edit_customer.html', car=car)

@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    car = Booking.query.get_or_404(book_id)

    if request.method == 'POST':
        car.name = request.form.get('name')
        car.num = request.form.get('num')
        car.from_ = request.form.get('from')
        car.to = request.form.get('to')
        car.typee = request.form.get('typee')
        car.way = request.form.get('way')
        cardate = request.form.get('date')
        my_date = datetime.strptime(cardate, '%Y-%m-%d').date()
        car.date = my_date
        car.price = request.form.get('price')
        car.time = request.form.get('time')
        car.note = request.form.get('note')

        db.session.commit()
        return redirect(url_for('books'))

    return render_template('edit_book.html', car=car)

@app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    car = Orders.query.get_or_404(order_id)
    if request.method == 'POST':
        company = Companies.query.filter(Companies.name.like(f"%{request.form.get('company_name')}%")).first()
        if car.payment == "اجل":
            company.credit -= car.total
            company.total = int(company.credit) - int(company.depit)
            
        total_mony = request.form.get('total_mony')
        car_money = request.form.get('car_money')
        office_money = request.form.get('office_money')
        fuel = request.form.get('fuel')
        driver_money = request.form.get('driver_money')
        date = request.form.get('date')
        my_date = datetime.strptime(date, '%Y-%m-%d').date()
        car.pickup_time = my_date 
        car.fromm = request.form.get('from') 
        car.to = request.form.get('to') 
        car.typee = request.form.get('type')
        car.company_name = request.form.get('company_name')
        car.driver_name = request.form.get('driver_name')
        car.user_name = current_user.name
        car.customer_name = request.form.get('customer_name')
        car.car_name = request.form.get('car_name')
        car.note = request.form.get('note')
        car.office_name = request.form.get('office_name')
        car.company_id = Companies.query.filter(Companies.name.like(f"%{request.form.get('company_name')}%")).first().id
        car.driver_id = Drivers.query.filter(Drivers.name.like(f"%{request.form.get('driver_name')}%")).first().id
        car.user_id = Users.query.filter(Users.name.like(f"%{request.form.get('user_name')}%")).first().id
        car.car_id = Cars.query.filter(Cars.name.like(f"%{request.form.get('car_name')}%")).first().id
        car.customer_id = Customers.query.filter(Customers.name.like(f"%{request.form.get('customer_name')}%")).first().id
        payment = request.form.get('payment')
        car.payment = payment
        car.total = int(total_mony)
        car.car = int(car_money)
        car.sub = (int(total_mony)-int(car_money))
        car.office = int(office_money)
        car.fuel = int(fuel)
        car.driver = int(driver_money)
        car.final = (int(car_money)-int(office_money)-int(fuel)-int(driver_money))
        if payment == "اجل":
            company.credit += int(total_mony)
            company.total = int(company.credit) - int(company.depit)
            
    
        
       
        db.session.commit()
        return redirect(url_for('orders'))
    companies_list = Companies.query.all()
    cars_list = Cars.query.all()
    drivers_list = Drivers.query.all()
    cust_list = Customers.query.all()
    users_list = Users.query.all()
    return render_template('edit_order.html',car = car,company = companies_list , cars = cars_list , driver = drivers_list
                           ,customer = cust_list,user = users_list)

    

@app.route('/books/delete/<int:book_id>', methods=['POST', "GET"])
@login_required
def delete_book(book_id):
    car = Booking.query.filter(Booking.id == book_id).first()
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('books'))

@app.route('/work/delete/<int:work_id>', methods=['POST', "GET"])
@login_required
def delete_work(work_id):
    car = Work.query.filter(Work.id == work_id).first()
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('work'))
@app.route('/edit/delete/<int:edit_id>', methods=['POST', "GET"])
@login_required
def delete_edit(edit_id):
    car = Edit.query.filter(Edit.id == edit_id).first()
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('edits'))

@app.route('/fatora/delete/<int:fatora_id>', methods=['POST', "GET"])
@login_required
def delete_fatora(fatora_id):
    car1 = Fatoras.query.filter(Fatoras.id == fatora_id).first()
    car = Companies.query.filter(Companies.name.like(f"%{car1.company_name}%")).first()
    car.depit = int(car.depit) + int(car1.credit)
    car.credit = int(car.credit) + int(car1.depit)
    car.total = int(car.credit) - int(car.depit)
    db.session.delete(car1)
    db.session.commit()
    return redirect(url_for('fatoras'))

@app.route('/cars/delete/<int:car_id>', methods=['POST', "GET"])
@login_required
def delete_car(car_id):
    car = Cars.query.filter(Cars.id == car_id).first()
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('cars'))

@app.route('/notes/delete/<int:note_id>', methods=['POST', "GET"])
@login_required
def delete_note(note_id):
    car = Notes.query.filter(Notes.id == note_id).first()
    db.session.delete(car)  
    db.session.commit()
    return redirect(url_for('notes'))

@app.route('/users/delete/<int:user_id>', methods=['POST', "GET"])
def delete_user(user_id):
    car = Users.query.filter(Users.id == user_id).first()
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('users'))

@app.route('/orders/delete/<int:order_id>', methods=['POST', "GET"])
def delete_order(order_id):
    car = Orders.query.filter(Orders.id == order_id).first()
    if car.payment == "اجل":
        c = Companies.query.filter(Companies.id == car.company_id).first()
        c.credit -= car.total
        c.total = int(c.credit) - int(c.depit)
        
        
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('orders'))

@app.route('/companies/delete/<int:company_id>', methods=['POST', "GET"])
def delete_company(company_id):
    car = Companies.query.filter(Companies.id == company_id).first()
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('companies'))

@app.route('/drivers/delete/<int:driver_id>', methods=['POST', "GET"])
def delete_driver(driver_id):
    driver = Drivers.query.filter(Drivers.id == driver_id).first()
    db.session.delete(driver)
    db.session.commit()
    return redirect(url_for('drivers'))

@app.route('/customers/delete/<int:customer_id>', methods=['POST', "GET"])
def delete_customer(customer_id):
    driver = Customers.query.filter(Customers.id == customer_id).first()
    db.session.delete(driver)
    db.session.commit()
    return redirect(url_for('customers'))

@app.route('/drivers/edit/<int:driver_id>', methods=['GET', 'POST'])
@login_required
def edit_driver(driver_id):
    car = Drivers.query.get_or_404(driver_id)

    if request.method == 'POST':
        car.name = request.form.get('name')
        car.num = request.form.get('num')
        car.add = request.form.get('add')
        car.typee = request.form.get('typee')
        db.session.commit()
        return redirect(url_for('drivers'))

    return render_template('edit_driver.html', car=car)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
