from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key for production

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Inside the signup route
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name', '')
        last_name = request.form['last_name']
        email = request.form['email']
        account_type = request.form['account_type']
        password = request.form['password']

        print(f"Received form data: {first_name}, {middle_name}, {last_name}, {email}, {account_type}")

        conn = get_db_connection()

        try:
            if account_type == 'Advocate':
                conn.execute('INSERT INTO advocate (first_name, middle_name, last_name, email, account_type, password) VALUES (?, ?, ?, ?, ?, ?)',
                            (first_name, middle_name, last_name, email, account_type, password))
                conn.commit()
                flash('Sign up successful! You can log in now.')
                print(f"Advocate {email} inserted into the database")
                return redirect(url_for('login'))

            elif account_type == 'Client':
                conn.execute('INSERT INTO client (first_name, middle_name, last_name, email, account_type, password) VALUES (?, ?, ?, ?, ?, ?)',
                            (first_name, middle_name, last_name, email, account_type, password))
                conn.commit()
                flash('Sign up successful! You can log in now.')
                print(f"Client {email} inserted into the database")
                return redirect(url_for('login'))

            else:
                return redirect(url_for('index')) 

        except sqlite3.IntegrityError as e:
            flash('Email already exists!')
            print(f"IntegrityError: {e}")
        finally:
            conn.close()

    return render_template('signup.html')



# Advocate dashboard route
@app.route('/advocate_dashboard')
def advocate_dashboard():
    if 'user_email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

    user_email = session['user_email']
    
    conn = get_db_connection()
    advocate = conn.execute('SELECT * FROM advocate WHERE email = ?', (user_email,)).fetchone()
    conn.close()

    if advocate:
        # Pass advocate details to the template
        return render_template('advocate_dashboard.html', advocate=advocate)
    else:
        flash('User not found')
        return redirect(url_for('login'))




@app.route('/edit_adv', methods=['GET', 'POST'])
def edit_adv():
    if 'user_email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

    user_email = session['user_email']

    conn = get_db_connection()

    if request.method == 'POST':
        # Get form data from edit_adv.html
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        pincode = request.form['pincode']
        specialization = request.form['specialization']

        # Update the advocate record in the database
        conn.execute('''
            UPDATE advocate
            SET first_name = ?, phone = ?, address_line = ?, address_line2 = ?, city = ?, pincode = ?, specialization = ?
            WHERE email = ?
        ''', (name, phone, address1, address2, city, pincode, specialization, user_email))

        conn.commit()
        conn.close()

        flash('Profile updated successfully.')
        return redirect(url_for('advocate_dashboard'))

    # Prepopulate the form with advocate details for GET request
    advocate = conn.execute('SELECT * FROM advocate WHERE email = ?', (user_email,)).fetchone()
    conn.close()

    return render_template('edit_adv.html', advocate=advocate)








@app.route('/client_dashboard')
def client_dashboard():
    if 'user_email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

    user_email = session['user_email']
    
    conn = get_db_connection()
    client = conn.execute('SELECT * FROM client WHERE email = ?', (user_email,)).fetchone()

    advocates = conn.execute('SELECT * FROM advocate').fetchall()


    conn.close()

    if client:
        # Pass advocate details to the template
        return render_template('client_dashboard.html', client=client , advocates=advocates)
    else:
        print("user not found")
        flash('User not found')
        return redirect(url_for('login'))




@app.route('/edit_client', methods=['GET', 'POST'])
def edit_client():
    if 'user_email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

    user_email = session['user_email']

    conn = get_db_connection()

    if request.method == 'POST':
        # Get form data from edit_adv.html
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        pincode = request.form['pincode']

        # Update the advocate record in the database
        conn.execute('''
            UPDATE client
            SET first_name = ?, phone = ?, address_line = ?, address_line2 = ?, city = ?, pincode = ?
            WHERE email = ?
        ''', (name, phone, address1, address2, city, pincode, user_email))

        conn.commit()
        conn.close()

        flash('Profile updated successfully.')
        return redirect(url_for('client_dashboard'))

    # Prepopulate the form with advocate details for GET request
    client = conn.execute('SELECT * FROM client WHERE email = ?', (user_email,)).fetchone()
    conn.close()

    return render_template('edit_client.html', client=client)




# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        client = conn.execute('SELECT * FROM client WHERE email = ? AND password = ?', (email, password)).fetchone()
        advocate = conn.execute('SELECT * FROM advocate WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        
        if client:
            account_type = client['account_type']  # Assuming your table has this column
            
            flash('Login successful!')

            if account_type == 'Client':
                session['user_email'] = client['email']
                return redirect(url_for('client_dashboard'))  # Redirect to client dashboard
            else:
                return redirect(url_for('index'))  # Redirect to homepage for unknown account types
            
        elif advocate:
            account_type = advocate['account_type']  # Assuming your table has this column
            flash('Login successful!')

            if account_type == 'Advocate':
                session['user_email'] = advocate['email']
                return redirect(url_for('advocate_dashboard'))  # Redirect to advocate dashboard
            else:
                return redirect(url_for('index'))  # Redirect to homepage for unknown account types
        else:
            flash('Invalid credentials, please try again.')
    
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
