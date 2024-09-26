from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from opencage.geocoder import OpenCageGeocode
import psycopg2

app = Flask(__name__)

# OpenCage API key
OPENCAGE_API_KEY = 'd5406154fc92457aaec554ceae5b51e3' 

# Database connection setup
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',  
        database='crime_alert',
        user='postgres',  
        password='arpit'  
    )
    return conn

# Function to create tables if they don't exist
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # users_info table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_info (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255),
            address VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(255),
            pin_code VARCHAR(10),
            contact_number VARCHAR(15),
            email VARCHAR(255),
            aadhar_number VARCHAR(20)
        );
    ''')

    # crime_reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crime_reports (
            id SERIAL PRIMARY KEY,
            incident_type VARCHAR(255),
            description TEXT,
            location VARCHAR(255),
            date DATE,
            time TIME,
            witness_name VARCHAR(255),
            victim_info TEXT,
            suspect_info TEXT,
            latitude DECIMAL,
            longitude DECIMAL
        );
    ''')

    conn.commit()
    cursor.close()
    conn.close()

create_tables()  # Call the function to create tables

# Function to get location coordinates using OpenCage
def get_location(location, retries=3):
    geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
    for attempt in range(retries):
        try:
            print(f"Attempting to geocode: {location}")
            result = geocoder.geocode(location)
            if result:
                loc = result[0]['geometry']
                print(f"Successfully geocoded: {location} -> ({loc['lat']}, {loc['lng']})")
                return loc['lat'], loc['lng']
            else:
                print(f"No location found for: {location}")
                return None
        except Exception as e:
            print(f"Geocoding failed: {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(1)  # Optional: wait before retrying
    print("All retries failed.")
    return None  # Return None if all attempts fail

# Route for home page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission from index.html
@app.route('/submit_user_info', methods=['POST'])
def submit_user_info():
    if request.method == 'POST':
        # Get user information from the form
        user_info = {
            'full_name': request.form['full_name'],
            'address': request.form['address'],
            'city': request.form['city'],
            'state': request.form['state'],
            'pin_code': request.form['pin_code'],
            'contact_number': request.form['contact_number'],
            'email': request.form['email'],
            'aadhar_number': request.form['aadhar_number']
        }
        
        # Store the information in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users_info (full_name, address, city, state, pin_code, contact_number, email, aadhar_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        ''', (user_info['full_name'], user_info['address'], user_info['city'], 
              user_info['state'], user_info['pin_code'], user_info['contact_number'], 
              user_info['email'], user_info['aadhar_number']))
        
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect to the crime reporting page
        return redirect(url_for('report'))

# Route for the crime reporting page (report.html)
@app.route('/report')
def report():
    return render_template('report.html')

# Handle crime report submission
@app.route('/submit_report', methods=['POST'])
def submit_report():
    if request.method == 'POST':
        # Get crime details from the form
        incident_type = request.form['incident_type']
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']
        time = request.form['time']
        witness_name = request.form.get('witness_name')  
        victim_info = request.form['victim_info']
        suspect_info = request.form.get('suspect_info')  

        # Use geopy to get coordinates based on location
        loc = get_location(location)

        if loc is not None:
            print(f"Crime reported: {incident_type} at {location}, Coordinates: ({loc[0]}, {loc[1]})")

            # Store the crime report in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO crime_reports (incident_type, description, location, date, time, witness_name, victim_info, suspect_info, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (incident_type, description, location, date, time, witness_name, victim_info, suspect_info, loc[0], loc[1]))
            
            conn.commit()
            cursor.close()
            conn.close()

            return "Crime reported successfully!"
        else:
            print(f"Geocoding failed for location: {location}")
            return "Invalid location, try again."

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/citizen')
def citizen():
    return render_template('citizen.html')

@app.route('/police')
def police():
    return render_template('police.html')

@app.route('/units')
def units():
    return render_template('units.html')

@app.route('/track')
def track():
    return render_template('track.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
