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

    if request.args.get('email'):
        email = request.args.get('email')
        userid = zd_helper.get_userid(email)
    else:
        return render_template('error.html', code=1, message="Please provide a valid email.")

    try:
        time = zd_helper.get_total_time_spent(userid)
    except:
        return render_template('error.html', code=2)

    return render_template('layout.html', ts=time, email=email)


@app.route('/<email>')
def time(email):
    try:
        userid = zd_helper.get_userid(email)
        time = zd_helper.get_total_time_spent(userid)
    except IndexError:
        return render_template('error.html', code=2, message="User not found in Zendesk. If you think this is not "
                                                             "right please report this issue to ielizaga@pivotal.io")
    except Exception:
        return render_template('error.html', code=3, message="Could not access one or more tickets. Please report this"
                                                             " issue to ielizaga@pivotal.io")

    return render_template('layout.html', ts=time, email=email)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
