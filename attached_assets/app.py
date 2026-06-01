from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

app = Flask(__name__)
app.secret_key = 'click2drive_secret_2026'

# ── DB CONFIG ──
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': '',
    'database': 'click2drive',
    'charset':  'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)


# ── HOME ──
@app.route('/')
def home():
    return render_template('home.html')


# ── CARS ──
@app.route('/CARS')
def cars():
    cars_list = [
        {"img": "Fortuner.png",              "name": "TOYOTA FORTUNER",        "price": "₱1,775,000"},
        {"img": "Mitsubishi Montero Sport.png","name": "MITSUBISHI MONTERO SPORT","price": "₱1,568,000"},
        {"img": "Ford Everest.png",           "name": "FORD EVEREST",            "price": "₱1,864,000"},
        {"img": "BAIC B30e Dune.png",         "name": "BAIC B30e DUNE",          "price": "₱1,599,000"},
        {"img": "Jaecoo EJ6.png",             "name": "JAECOO EJ6",              "price": "₱1,649,000"},
        {"img": "Suzuki Jimny 5-Door.png",    "name": "SUZUKI JIMMY 5-DOOR",     "price": "₱6,100,000"},
        {"img": "VinFast VF.png",             "name": "VinFast VF",              "price": "₱590,000"},
        {"img": "JETOUR T2.png",              "name": "JETOUR T2",               "price": "₱2,498,000"},
        {"img": "GAC AION V.png",             "name": "GAC AION V",              "price": "₱1,498,000"},
        {"img": "KIA SORENTO.png",            "name": "KIA SORENTO",             "price": "₱2,188,000"},
    ]
    return render_template('cars.html', cars_list=cars_list)


# ── AUTH PAGE (GET) ──
@app.route('/login', methods=['GET'])
def login_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('auth.html', active_tab='login')

@app.route('/signup', methods=['GET'])
def signup_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('auth.html', active_tab='signup')


# ── LOGIN (POST) ──
@app.route('/login', methods=['POST'])
def login():
    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        return render_template('auth.html', active_tab='login',
                               login_error='Please fill in all fields.')

    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cur.fetchone()
        conn.close()
    except Exception as e:
        return render_template('auth.html', active_tab='login',
                               login_error='Database error. Make sure XAMPP MySQL is running.')

    if not user or not check_password_hash(user['password'], password):
        return render_template('auth.html', active_tab='login',
                               login_error='Invalid email or password.')

    session.permanent = 'remember' in request.form
    session['user_id']   = user['id']
    session['user_name'] = user['first_name']

    return render_template('auth.html', active_tab='login', login_success=True)


# ── SIGNUP (POST) ──
@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.form.get('first_name', '').strip()
    last_name  = request.form.get('last_name', '').strip()
    email      = request.form.get('signup_email', '').strip()
    password   = request.form.get('signup_password', '')
    confirm    = request.form.get('confirm_password', '')

    # Validation
    if not all([first_name, last_name, email, password, confirm]):
        return render_template('auth.html', active_tab='signup',
                               signup_error='Please fill in all fields.')

    if len(password) < 8:
        return render_template('auth.html', active_tab='signup',
                               signup_error='Password must be at least 8 characters.')

    if password != confirm:
        return render_template('auth.html', active_tab='signup',
                               signup_error='Passwords do not match.')

    hashed = generate_password_hash(password)

    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM users WHERE email = %s', (email,))
            if cur.fetchone():
                conn.close()
                return render_template('auth.html', active_tab='signup',
                                       signup_error='An account with that email already exists.')

            cur.execute(
                'INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)',
                (first_name, last_name, email, hashed)
            )
            conn.commit()
            user_id = cur.lastrowid
        conn.close()
    except Exception as e:
        return render_template('auth.html', active_tab='signup',
                               signup_error='Database error. Make sure XAMPP MySQL is running.')

    session['user_id']   = user_id
    session['user_name'] = first_name

    return render_template('auth.html', active_tab='signup', signup_success_redirect=True)


# ── LOGOUT ──
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)
