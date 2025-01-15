from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': 'root',  # Your MySQL password
    'database': 'login'  # Your database name
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        if not name or not phone or not email:
            flash('All fields are required!', 'error')
        else:
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()
                query = "INSERT INTO users (name, phone, email) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, phone, email))
                connection.commit()
                flash('Data submitted successfully!', 'success')
            except mysql.connector.Error as err:
                flash(f"Database error: {err}", 'error')
            finally:
                cursor.close()
                connection.close()

        return redirect('/')

    return render_template('index.html')

@app.route('/view', methods=['GET', 'POST'])
def view():
    user_data = None

    if request.method == 'POST':
        user_id = request.form['user_id']

        if not user_id:
            flash('ID is required to view details!', 'error')
        else:
            try:
                # Connect to the database
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor(dictionary=True)

                # Fetch data by ID
                query = "SELECT * FROM users WHERE id = %s"
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone()

                if not user_data:
                    flash('No user found with the given ID.', 'error')
            except mysql.connector.Error as err:
                flash(f"Database error: {err}", 'error')
            finally:
                cursor.close()
                connection.close()

    return render_template('view.html', user_data=user_data)

@app.route('/view-update', methods=['GET', 'POST'])
def view_update():
    if request.method == 'POST':
        user_id = request.form.get('id')

        if not user_id:
            flash('ID is required to fetch data!', 'error')
            return redirect('/view-update')

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            if not user:
                flash('No record found with the given ID.', 'error')
                return redirect('/view-update')

            return render_template('view_update.html', user=user)

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'error')
        finally:
            cursor.close()
            connection.close()

    return render_template('view_update.html', user=None)


@app.route('/view-update/submit', methods=['POST'])
def view_update_submit():
    user_id = request.form['id']
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']

    if not user_id or not name or not phone or not email:
        flash('All fields are required!', 'error')
        return redirect('/view-update')

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "UPDATE users SET name = %s, phone = %s, email = %s WHERE id = %s"
        cursor.execute(query, (name, phone, email, user_id))
        connection.commit()
        flash('Data updated successfully!', 'success')
    except mysql.connector.Error as err:
        flash(f"Database error: {err}", 'error')
    finally:
        cursor.close()
        connection.close()

    return redirect('/view-update')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        user_id = request.form.get('id')

        if not user_id:
            flash('ID is required to delete a record!', 'error')
            return redirect('/delete')

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Check if the record exists
            check_query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(check_query, (user_id,))
            record = cursor.fetchone()

            if not record:
                flash('No record found with the given ID.', 'error')
                return redirect('/delete')

            # Delete the record
            delete_query = "DELETE FROM users WHERE id = %s"
            cursor.execute(delete_query, (user_id,))
            connection.commit()

            flash('Record deleted successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'error')
        finally:
            cursor.close()
            connection.close()

        return redirect('/delete')

    return render_template('delete.html')



if __name__ == '__main__':
    app.run(debug=True)