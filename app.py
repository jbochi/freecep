from PIL import Image
import tempfile
import os

from flask import Flask, redirect, request, render_template, url_for
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.wtf import Form, TextField, Required

import cep

app = Flask(__name__)
app.config.from_object('freecep.default_settings')
app.config.from_envvar('FREECEP_SETTINGS')

db = SQLAlchemy(app)

class Search(db.Model):
    __tablename__ = 'search'
    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.Unicode(50))
    filename = db.Column(db.String(30))
    text = db.Column(db.UnicodeText())
    boxes = db.Column(db.UnicodeText())


class SearchForm(Form):
    query = TextField("Endereco ou CEP", validators=[Required()])


@app.route("/", methods=("GET", "POST"))
def main():
    form = SearchForm()

    if form.validate_on_submit():
        correios = cep.Correios()
        correios.consulta(form.query.data)
        im = correios.detalhe(format='image')
        im_improved = correios.improve_image(im)
        text = correios.to_text(im_improved, improve=False)
        boxes = correios.to_text(im_improved, improve=False, boxes=True)

        filename = tempfile.mkstemp(dir=app.config['IMAGES_PATH'], text=True, suffix='.png')[1]
        filename = os.path.relpath(filename, app.config['IMAGES_PATH'])
        im_improved.save(os.path.join(app.config['IMAGES_PATH'], filename))

        search = Search(search=unicode(form.query.data),
                        filename=filename,
                        text=unicode(text),
                        boxes=unicode(boxes))
        db.session.add(search)
        db.session.commit()

        return redirect(url_for('edit_record', id=search.id))

    return render_template('default.html', form=form)


@app.route("/<int:id>", methods=['GET', 'POST'])
def edit_record(id):
    search = Search.query.get_or_404(id)
    if request.method == 'POST':
        search.boxes = request.form['boxes']
        db.session.add(search)
        db.session.commit()

    im = Image.open(os.path.join(app.config['IMAGES_PATH'], search.filename))
    width, height = im.size

    image_data = {'path': '/static/images/%s' % search.filename,
                  'width': width,
                  'height': height}
    return render_template('trainer.html', search=search, image_data=image_data)


if __name__ == "__main__":
    app.secret_key = 'as_seen_on_github'
    app.debug = True
    app.run(host='0.0.0.0', port=57814)
