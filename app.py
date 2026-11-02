from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__, template_folder='templates', static_folder='src')

def init_db():
  fleet = sqlite3.connect('fleet.db')
  cursor = fleet.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      regs TEXT NOT NULL,
      type TEXT NOT NULL,
      status TEXT NOT NULL
    )
  ''')
  fleet.commit()
  fleet.close()
  
@app.route('/')
def home():
  return render_template("home.html")

@app.route("/Fuhrparkliste")
def fleet():
    edit_id = request.args.get('edit')
    edit_vehicle = None
    
    fleet = sqlite3.connect('fleet.db')
    fleet.row_factory = sqlite3.Row
    cursor = fleet.cursor()

    if edit_id:
        cursor.execute("SELECT * FROM vehicles WHERE id = ?", (edit_id,))
        edit_vehicle = cursor.fetchone()
        
    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()
    fleet.close()
    
    return render_template('Fuhrparkliste.html', fuhrpark_liste=vehicles, edit_vehicle=edit_vehicle)

@app.route('/Fahrzeug-hinzufuegen', methods=['POST'])
def add():
    regs = request.form['regs']
    type = request.form['type']
    status = request.form['status']
    
    fleet = sqlite3.connect('fleet.db')
    cursor = fleet.cursor()
    cursor.execute("INSERT INTO vehicles (regs, type, status) VALUES (?, ?, ?)", (regs, type, status))
    fleet.commit()
    fleet.close()
    
    return redirect(url_for('fleet'))
  
@app.route('/Fahrzeug-aktualisieren/<int:id>', methods=['POST'])
def update(id):
    regs = request.form['regs']
    type = request.form['type']
    status = request.form['status']
    
    fleet = sqlite3.connect('fleet.db')
    cursor = fleet.cursor()
    cursor.execute("""
        UPDATE vehicles 
        SET regs = ?, type = ?, status = ? 
        WHERE id = ?
    """, (regs, type, status, id))
    fleet.commit()
    fleet.close()
    
    return redirect(url_for('fleet'))

@app.route('/LindenhagenPLUS')
def plus():
  return render_template("PlusTicket.html")

@app.route('/Karriere')
def career():
  return render_template("Karriere.html")

@app.route('/Partner')
def coop():
  return render_template("Partner.html")
  
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
