from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'passenger_name': request.form.get('passenger_name', ''),
        'phone_number': request.form.get('phone_number', ''),
        'address': request.form.get('address', ''),
        'flight_date': request.form.get('flight_date', ''),
        'flight_no': request.form.get('flight_no', ''),
        'flight_route': request.form.get('flight_route', ''),
        'items_weight': request.form.get('items_weight', ''),
        'bag_color': request.form.get('bag_color', ''),
        'bag_type': request.form.get('bag_type', ''),
        'bag_tag': request.form.get('bag_tag', ''),
        'file_no': request.form.get('file_no', ''),
        'receiving_datetime': request.form.get('receiving_datetime', ''),
        'signature': request.form.get('signature', ''),
        'nas_agent': request.form.get('nas_agent', ''),
        'staff_number': request.form.get('staff_number', '')
    }

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deliveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_name TEXT,
            phone_number TEXT,
            address TEXT,
            flight_date TEXT,
            flight_no TEXT,
            flight_route TEXT,
            items_weight TEXT,
            bag_color TEXT,
            bag_type TEXT,
            bag_tag TEXT,
            file_no TEXT,
            receiving_datetime TEXT,
            signature TEXT,
            nas_agent TEXT,
            staff_number TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO deliveries (passenger_name, phone_number, address, flight_date, flight_no, flight_route, 
        items_weight, bag_color, bag_type, bag_tag, file_no, receiving_datetime, signature, nas_agent, staff_number)
        VALUES (:passenger_name, :phone_number, :address, :flight_date, :flight_no, :flight_route, :items_weight, 
        :bag_color, :bag_type, :bag_tag, :file_no, :receiving_datetime, :signature, :nas_agent, :staff_number)
    ''', data)

    conn.commit()
    conn.close()

    return redirect(url_for('records'))

@app.route('/records')
def records():
    bag_tag_query = request.args.get('bag_tag')
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    if bag_tag_query:
        cursor.execute('SELECT * FROM deliveries WHERE bag_tag LIKE ?', ('%' + bag_tag_query + '%',))
    else:
        cursor.execute('SELECT * FROM deliveries')
    rows = cursor.fetchall()
    conn.close()
    return render_template('records.html', rows=rows)
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM deliveries')
    rows = cursor.fetchall()
    conn.close()
    return render_template('records.html', rows=rows)

@app.route('/debug')
def debug():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM deliveries')
    rows = cursor.fetchall()
    return f"عدد السجلات: {len(rows)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
