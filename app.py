from flask import Flask,render_template,url_for
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("page_connexion.html")


@app.route("/accueil/")
def accueil():
    return render_template("accueil.html")


@app.route("/formulaire/")
def formulaire():
    return render_template("formulaire.html")
@app.route("/magasin/")
def magasin():
    return render_template("./magasin.html")

@app.route("/ajout_magasin/")
def ajout_magasin():
    return render_template("ajout_magasin.html")


@app.route("/form_modif/")
def form_modif():
    return render_template("form_modif.html")



@app.route("/magasin_modif/")
def magasin_modif():
    return render_template("magasin_modif.html")



@app.route("/suppression_form/")
def suppression_form():
    return render_template("suppression_form.html")



@app.route("/sup_magasin/")
def sup_magasin():
    return render_template("sup_magasin.html")


if __name__ == "__main__":
    app.run(debug=True)