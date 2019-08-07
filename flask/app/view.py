from app import app, ConnectlistSchema, Connectlist, time_on_status
from flask import render_template

connect_list = ConnectlistSchema(strict=True)
connect_lists = ConnectlistSchema(strict=True, many=True)


@app.route('/')
def index():
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
