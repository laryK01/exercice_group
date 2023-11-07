from flask import Flask,render_template, redirect, url_for
import pyodbc as odbc
from flask import request

app = Flask(__name__)

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-3AJUOVH\SQLEXPRESS'
DATABASE_NAME = 'exercice_group'

# uid=<username>;
# pwd=<password>;

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_connection=yes;"""

conn = odbc.connect(connection_string)
cursor = conn.cursor()


@app.route("/")

def index():
    
    return render_template("page_connexion.html")


@app.route("/accueil/")
def accueil():
    return render_template("accueil.html")


@app.route("/formulaire/", methods = ['GET', 'POST'])
def formulaire():
    if request.method=="POST":
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        nom =request.form['nom']
        Adresse =request.form['Adresse']
        Ville= request.form['Ville']
        CodePostal = request.form['CodePostal']
        insert = "insert into Magasin(NomMagasin,Adresse,Ville,CodePostal) values (?,?,?,?)"
        cursor.execute(insert,(nom,Adresse,Ville,CodePostal))
        cursor.commit()
        cursor.close()
        return redirect(url_for('magasin'))
    return render_template("formulaire.html")

@app.route("/magasin/")
def magasin():
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('SELECT * from Magasin')
    listMagasin= cursor.fetchall()
    return render_template("./magasin.html", liste = listMagasin)

@app.route("/ajout_magasin/")
def ajout_magasin(id_mag):
    
    return render_template("ajout_magasin.html")


@app.route("/form_modif/<int:id_item>",methods=['POST','GET'])
def form_modif(id_item):
    id_item = int(id_item)
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("select * from Magasin where MagasinID=?",(id_item))
    data = cursor.fetchall()
    data = data[0]
    if request.method == 'POST':
        Nom = request.form['Nom']
        Adresse = request.form['Adresse']
        Ville = request.form['Ville']
        CodePostal = request.form['CodePostal']
        cursor.execute('''
                    UPDATE Magasin
                    SET NomMagasin=?, Adresse=?, Ville=?, CodePostal=?
                    WHERE MagasinID = ?''',(Nom, Adresse, Ville, CodePostal,id_item))

        conn.commit()
        conn.close()
        Flask('le Magasin numero a été modifier avec succès! info')
        return redirect(url_for('magasin'))
    return render_template("form_modif.html",data=data)
       



@app.route("/magasin_modif/")
def magasin_modif():
    return render_template("magasin_modif.html")



# @app.route("/suppression_form/<int:id_mag>", methods=['GET'])
# def suppression_form(id_mag):
#     id_mag=int(id_mag)
#     conn = odbc.connect(connection_string)
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM magasin WHERE idMagasin =?;",(id_mag))
#     cursor.commit()
#     cursor.close()
#     #return redirect(url_for(magasin))
#     return render_template("suppression_form.html")


@app.route('/suppression_form/<int:item_id>', methods=['GET', 'POST'])
def supprimer(item_id):
    if request.method == 'POST':
        item_id=int(item_id)
        con = odbc.connect(connection_string)
        cur = con.cursor()
        cur.execute(f"DELETE FROM magasin WHERE MagasinID ={item_id};")
        con.commit()
        con.close()
        return redirect(url_for('magasin'))
    return render_template('suppression_form.html')





@app.route("/sup_magasin/")
def sup_magasin():
    
    return render_template("sup_magasin.html")


if __name__ == "__main__":
    app.run(debug=True)