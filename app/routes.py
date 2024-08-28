from modules import *
from modules import db_functions as db 
from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

db_path = 'app/instance/game.db'

@main.errorhandler(400) # bad request
def err400(error):
    return render_template('error.html', error_type="Bad Request", error_title="Sorry! We cannot process your request.", error_subtitle="Double check your inputs and try again.")

@main.errorhandler(401) # no authorisation
def err401(error):
    return render_template('error.html', error_type="Unauthorised Access", error_title="You do not have authorisation to view this content.", error_subtitle="Please log in to access this page.")

@main.errorhandler(403) # forbidden resource
def err403(error):
    return render_template('error.html', error_type="Forbidden", error_title="You do not have access to view this content.", error_subtitle="Please contact us if you believe this to be a mistake.")

@main.errorhandler(404) # resource not found
def err404(error):
    return render_template('error.html', error_type="Resource Not Found", error_title="Sorry! We could not find that page.", error_subtitle="Check the URL or return to the &nbsp;<a href='" + url_for('home') + "'>home page</a>.")

@main.errorhandler(500) # internal server error
def err500(error): # !!! REPLACE MY EMAIL WITH SITE EMAIL ONCE SET UP !!!
    return render_template('error.html', error_type="Internal Server Error", error_title="Sorry, something went wrong on our end.", error_subtitle="Check back later or report the issue &nbsp; <a href='mailto: dylan.bullock.965@accesscreative.ac.uk'>here</a> &nbsp; by email.")


# --- PAGE ROUTES ---

@main.route('/')
@main.route('/home')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/wiki')
def wiki():
    return render_template('wiki.html')


# --- GET ROUTES ---

@main.route('/category/<category>', methods=['GET'])
def get_category_data(category):
    if request.method == 'GET':
        try:
            with db.connect(db_path) as conn:
                data = db.read_table_data(conn, category)

                return jsonify({"status": 200, "data": data})
        except Exception as e:
            print(f"An error occured: {e}")

            return jsonify({"status": 500, "error": e})
    else:
        return redirect('wiki.html')

# --- CRUD OPERATIONS ---

@main.route('/upload/<category>', methods=['GET', 'POST'])
def upload_category_data(category):
    if request.method == 'POST':
        try:
            with db.connect(db_path) as conn:
                form_data = request.form.items()
                form_columns = request.form.keys()

                columns = []
                values = []

                for column in form_columns:
                    columns.append(column)
                for i in form_data:
                    values.append(i[1])

                lastrowid = db.create_table_data(conn=conn, table=category, columns=columns, values=values)

                return jsonify({"status": 200, "lastrowid": lastrowid}), 201
        except Exception as e:
            print(f"An error occured: {e}")

            return jsonify({"status": 500, "error": e}),500
    else:
        return redirect('wiki.html')

@main.route('/edit/<category>/<int:id>', methods=['GET', 'POST'])
def edit_category_data(category, id):
    if request.method == 'POST':
        try:
            with db.connect(db_path) as conn:
                form_data = request.form.items()
                values = []

                for i in form_data:
                    values.append(i[1])

                rowcount = db.update_table_data(conn=conn, table=category, id=id, data=values)

                return jsonify({"status": 201, "rowcount": rowcount})
        except Exception as e:
            print(f"An error occured: {e}")

            return str(e)

@main.route('/delete/<category>/<int:id>', methods=['GET', 'POST'])
def delete_category_data(category, id):
    if request.method == 'POST':
        try:
            with db.connect(db_path) as conn:
                print(category, id)
                rowcount = db.delete_table_data(conn=conn, table=category, id=id)
                print(f"rowcount: {rowcount}")

                return jsonify({"status": 201, "rowcount": rowcount})
        except Exception as e:
            print(f"An error occured: {e}")

            return jsonify({"status": 500, "error": e})
    else:
        return redirect('wiki.html')