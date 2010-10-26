from flask import Flask, render_template
from flaskext.wtf import Form, TextField, Required

import cep

app = Flask(__name__)

class SearchForm(Form):
    query = TextField("Endereco ou CEP", validators=[Required()])
    
       
@app.route("/", methods=("GET", "POST"))
def main():
    form = SearchForm()
    resultado = None
    
    if form.validate_on_submit():
        correios = cep.Correios()
        correios.consulta(form.query.data)
        resultado = correios.detalhe(format='text')
        #resultado = form.query.data
        
    return render_template('default.html', form=form, resultado=resultado)
          

if __name__ == "__main__":
    app.secret_key = 'as_seen_on_github'
    app.debug = True
    app.run()
