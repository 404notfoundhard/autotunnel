from app import app, ConnectlistSchema, Connectlist, time_on_status, db
from flask import render_template, flash, request, redirect, url_for    
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


connect_list = ConnectlistSchema(strict=True)
connect_lists = ConnectlistSchema(strict=True, many=True)


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])


@app.route('/delete', methods=['GET'])
@app.route('/delete/<id>', methods=['GET'])
def delete_host_get(id):
    return redirect('/')


@app.route('/delete/<id>', methods=['POST'])
def delete_host(id):
    Connectlist.query.filter_by(id=id).delete()
    # print(host)
    # Connectlist.query.get(id).delete()
    # db.session.delete(host)
    db.session.commit()
    return redirect('/')


@app.route('/', methods=['GET','POST'])
def index():
    # form = ReusableForm(request.form)
    # if request.method == 'POST':
    #     print(request.form['ssh_port_input'])
    #     print(request.form['mysql_port_input'])
    #     print(request.form['vnc_port_input'])
    #     print(request.form['hostname'])
    all_info = connect_lists.dump(Connectlist.query.all())[0]
    all_info = list(filter(None, all_info))
    hosts_status = []
    for info in all_info:
        # print(info)
        host_status = {}
        status = time_on_status(info['date_time'])
        host_status['status'] = status
        host_status['hostname'] = info['hostname']
        host_status['index'] = info['id']
        hosts_status.append(host_status)
    # {'db_port': 50002, 'vnc_port': 50003, 'ssh_port': 50001,
    #  'date_time': '2019-08-07 04:44:50.274444',
    #  'hostname': 'test',
    #  'server': '11.22.33.44'}
    # print(hosts_status)
    return render_template('index.html', all_info=all_info, hosts_status=hosts_status)


@app.route('/login')
def login():
    return 'auth success'
