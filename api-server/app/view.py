from app import Connectlist, db, app, request, datetime, connect_list
from app import add_new_host


@app.route('/get_info/<hostname>', methods=['POST'])
def get_ports_info(hostname):
    if request.form['token'] == '12345':
        ports_info = Connectlist.query.filter_by(hostname=hostname).first()
        if ports_info is None:
            add_new_host(hostname)
            ports_info = Connectlist.query.filter_by(hostname=hostname).first()
            return connect_list.jsonify(ports_info)
        ports_info.last_connect_time = str(datetime.utcnow())
        db.session.commit()
    return connect_list.jsonify(ports_info)
