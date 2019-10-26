from app import Connectlist, db, app, request, datetime, connect_list
from app import add_new_host, kill_socket
from config import Configuration

conf_obj = Configuration()


@app.route('/get_info/<hostname>', methods=['POST'])
def get_ports_info(hostname):
    print(request.form)
    if request.form['token'] == conf_obj.secret_token:
        ports_info = Connectlist.query.filter_by(hostname=hostname).first()
        if ports_info is None:
            add_new_host(hostname)
            ports_info = Connectlist.query.filter_by(hostname=hostname).first()
            return connect_list.jsonify(ports_info)

        if request.form['reconnect_status'] == 'True':
            kill_socket(hostname)
            return connect_list.jsonify(ports_info)

        # print('NOT THIS!')
        ports_info.last_connect_time = str(datetime.utcnow())
        db.session.commit()
        return connect_list.jsonify(ports_info)
    else:
        return exit(-1)
