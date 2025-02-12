from testflask import Flask, render_template, redirect, url_for

#init variable app avec flask
app = Flask(__name__)


#route racine
@app.route('/')
def home():
    name = 'Alice'
    return render_template('home.html', nom = name )

#page profil
@app.route('/profil/<nom>')
def profil(nom):
    #return f'Bienvenue sur le profil de {nom}'
    return render_template('view/profil/profil.html', nom = nom)

#redirect
@app.route('/redirect_profil')
def go_to_profil():
    return redirect(url_for('profil', nom = 'Alice'))


if __name__ == '__main__':
    app.run(debug=True)