from app import app, ConnectlistSchema, Connectlist, db, hosts_info
from flask import render_template, redirect  # , flash, request,
# from wtforms import Form, TextField, TextAreaField, validators, StringField


connect_list = ConnectlistSchema(strict=True)
connect_lists = ConnectlistSchema(strict=True, many=True)


# class ReusableForm(Form):
#     name = TextField('Name:', validators=[validators.required()])


@app.route('/delete', methods=['GET'])
@app.route('/delete/<id>', methods=['GET'])
def delete_host_get(id):
    return redirect('/')


@app.route('/delete/<id>', methods=['POST'])
def delete_host(id):
    Connectlist.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def index():
    all_info = connect_lists.dump(Connectlist.query.all())[0]
    hosts_status = hosts_info(all_info)  # output is list
    return render_template('index.html', all_info=all_info, hosts_status=hosts_status)


@app.route('/login')
def login():
    return 'auth success'
