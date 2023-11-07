from flask import Flask,render_template, redirect, url_for,flash
import pyodbc as odbc
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] ='clés_flash'
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



@app.route("/produit/")
def produit():
    conn = odbc.connect(connection_string)
    cur = conn.cursor()
    cur.execute("select * from produit")
    base = cur.fetchall()
    return render_template("produit.html", mybase=base)
    
@app.route("/formulaire_produit/", methods=['GET', 'POST'])
def formulaire_produit():
    if request.method == 'POST':
        NomProduit = request.form['NomProduit']
        CategorieProduit = request.form['CategorieProduit']
        PrixUnitaire = request.form['PrixUnitaire']
        conn = odbc.connect(connection_string)
        cur = conn.cursor()
        cur.execute('''
              INSERT INTO Produit(NomProduit, CategorieProduit,PrixUnitaire)
              VALUES(?, ?, ?) ''', (NomProduit, CategorieProduit, PrixUnitaire))
        conn.commit()
        conn.close()
        flash('produit bien enregistré','succès')
        return redirect(url_for("produit"))
    base = ''
    return render_template("formulaire_produit.html", mybase=base )


@app.route("/table_produit/")
def table_produit():
    return render_template("table_produit.html")

@app.route('/form_modif_p/<int:Prod_id>', methods=['POST', 'GET'])
def form_modif_p(Prod_id):
    
    if request.method == 'POST':
            NomProduit = request.form['NomProduit']
            CategorieProduit = request.form['CategorieProduit']
            PrixUnitaire = request.form['PrixUnitaire']
            conn = odbc.connect(connection_string)
            cur = conn.cursor()
            cur.execute('''
                        update Produit set NomProduit=?,CategorieProduit=?, PrixUnitaire=? where ProduitID=?''',
                        (NomProduit, CategorieProduit, PrixUnitaire, Prod_id))
            conn.commit()
            conn.close()
            flash('produit bien modifié','succès')
            return redirect(url_for("produit"))
    Prod_id = int(Prod_id)
    conn = odbc.connect(connection_string)
    cur = conn.cursor()
    cur.execute("select * from Produit where ProduitID=?", (Prod_id,))
    base = cur.fetchone()
    return render_template("form_modif_p.html", mybase=base)


@app.route("/suppression_form_p/")
def suppression_form_p():
    return render_template("suppression_form_p.html")


@app.route("/sup_produit/<int:sup>", methods=['POST','GET'])
def sup_produit(sup):
    conn = odbc.connect(connection_string)
    cur = conn.cursor()
    cur.execute("delete from produit where ProduitID=?", (sup,))
    conn.commit()
    flash(' votre produit a été supprimé','succès')
    return redirect(url_for("produit"))


@app.route("/liste_stock/")
def liste_stock():
    conn = odbc.connect(connection_string)
    cur = conn.cursor()
    cur.execute("select StockID,QuantiteEnStock, NomMagasin,NomProduit from Stock inner join Magasin on Stock.MagasinID = Magasin.MagasinID inner join Produit on Stock.ProduitID = Produit.ProduitID")
    base = cur.fetchall()
    return render_template("liste_stock.html", mybase=base)



# @app.route("/produit/")
# def produit():
#     conn = odbc.connect(connection_string)
#     cur = conn.cursor()
#     cur.execute("select * from produit")
#     base = cur.fetchall()
#     return render_template("produit.html", mybase=base)



# @app.route('/form_modif_stock/<int:stock>', methods=['POST', 'GET'])
# def form_modif_stock(stock):
    
#     if request.method == 'POST':
#             QuantiteEnStock = request.form['QuantiteEnStock']
#             MagasinID = request.form[' MagasinID']
#             ProduitID = request.form['ProduitID']
#             conn = odbc.connect(connection_string)
#             cur = conn.cursor()
#             cur.execute('''
#                         update Stock set QuantiteEnStock=?,MagasinID=?, ProduitID=? where StockID=?''',
#                         (QuantiteEnStock, MagasinID, ProduitID, stock))
#             conn.commit()
#             conn.close()
#             flash('produit bien modifié','succès')
#             return redirect(url_for("produit"))
#     stock = int(stock)
#     conn = odbc.connect(connection_string)
#     cur = conn.cursor()
#     cur.execute("select * from Produit where ProduitID=?", (stock,))
#     base = cur.fetchone()
#     return render_template("form_modif_stock.html", mybase=base)


if __name__ == "__main__":
    app.run(debug=True)