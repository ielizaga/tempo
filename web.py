from flask import Flask
from flask import render_template
from flask import request
import os
import zd_helper

app = Flask(__name__)
port = int(os.getenv("PORT"))
MAX_TIME_LOGGED = 28800


@app.route('/')
def chart():
    if request.args.get('userid'):
        userid = request.args.get('userid')
        email = zd_helper.get_email(userid)
    elif request.args.get('email'):
        email = request.args.get('email')
        userid = zd_helper.get_userid(email)
    else:
        return 'You need to specify a userid or email'

    total_ts = zd_helper.get_total_time_spent(userid)
    remaining_ts = MAX_TIME_LOGGED-total_ts
    m, s = divmod(total_ts, 60)
    h, m = divmod(m, 60)
    m1, s1 = divmod(remaining_ts, 60)
    h1, m1 = divmod(m1, 60)

    labels = ['%sh %sm %ss logged' % (h, m, s),'%sh %sm %ss remaining' % (h1, m1, s1)]
    colors = ["#58FA82", "#FE2E2E"]
    values = [total_ts, remaining_ts]

    return render_template('layout.html', set=zip(values, labels, colors), email=email)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
