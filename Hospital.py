# app.py

import streamlit as st
import sqlite3

# Establish SQLite connection and create a table if not exists
conn = sqlite3.connect('hospital.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS patients
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              age INTEGER,
              gender TEXT)''')
conn.commit()

def add_patient(name, age, gender):
    c.execute('''INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)''', (name, age, gender))
    conn.commit()
    return c.lastrowid

def view_patient(patient_id):
    c.execute('''SELECT * FROM patients WHERE id = ?''', (patient_id,))
    return c.fetchone()

def main():
    st.title('Hospital Management System')

    menu = ['Add Patient', 'View Patient']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Add Patient':
        st.subheader('Add New Patient')
        name = st.text_input('Enter patient name')
        age = st.number_input('Enter patient age', min_value=0, max_value=150, step=1)
        gender = st.selectbox('Select patient gender', ['Male', 'Female', 'Other'])

        if st.button('Add Patient'):
            if name and age and gender:
                patient_id = add_patient(name, age, gender)
                st.success(f'Patient Added with ID: {patient_id}')
            else:
                st.warning('Please fill in all fields.')

    elif choice == 'View Patient':
        st.subheader('View Patient Details')
        patient_id = st.number_input('Enter Patient ID', min_value=1, value=1)
        if st.button('View Details'):
            patient = view_patient(patient_id)
            if patient:
                st.write(f'**Name:** {patient[1]}')  # patient[1] is the name field in SQLite query result
                st.write(f'**Age:** {patient[2]}')   # patient[2] is the age field in SQLite query result
                st.write(f'**Gender:** {patient[3]}') # patient[3] is the gender field in SQLite query result
            else:
                st.warning('Patient not found.')

if __name__ == '__main__':
    main()
