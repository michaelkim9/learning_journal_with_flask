from flask import (Flask, g, render_template, flash, redirect,
                   url_for, request, abort)


import forms
import models


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'


app = Flask(__name__)
app.secret_key = 'HO@R_*%()#JFIOfeg43hhrFEJ'


@app.before_request
def before_request():
    '''Connect to database before each request'''
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    '''Close the database connection after each request'''
    g.db.close()
    return response


@app.route('/add', methods=('GET', 'POST'))
def add_entry():
    '''Adding new entry'''
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data,
            date=form.date.data,
            spent=form.spent.data,
            learned=form.learned.data,
            resources=form.resources.data)
        flash('Entry created!', 'success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/detail/<int:entry_id>')
def detail(entry_id):
    '''Route to see entry details'''
    try:
        entry = models.Entry.select().where(models.Entry.id == entry_id).get()
    except models.Entry.DoesNotExist:
        abort(404)
    return render_template('detail.html', entry=entry)


@app.route('/edit/<int:entry_id>', methods=('GET', 'POST'))
def edit_entry(entry_id):
    '''Route to edit entry'''
    try:
        entry = models.Entry.select().where(models.Entry.id == entry_id).get()
    except models.DoesNotExist:
        abort(404)
    else:
        form = forms.EntryForm(obj=entry)
        if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(entry)
                entry.save()
                flash('Entry updated!', 'success')
                return redirect(url_for('detail', entry_id=entry.id))
    return render_template('edit.html', form=form, entry=entry)


@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    '''Route to delete entry'''
    try:
        entry = models.Entry.select().where(models.Entry.id == entry_id).get()
    except models.DoesNotExist:
        abort(404)
    else:
        entry.delete_instance()
        flash('Entry deleted!', 'success')
    return redirect(url_for('index'))


@app.route('/')
def index():
    '''Main page to view entries and dates'''
    entries = models.Entry.select().limit(100)
    return render_template('index.html', entries=entries)


@app.errorhandler(404)
def not_found(error):
    '''404 error route'''
    return render_template('404.html', error=error), 404


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
