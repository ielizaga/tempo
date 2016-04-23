import requests
import os
import time
import datetime
import dateutil.parser

def get_url(url):
    response = requests.get(url, auth=(os.getenv('ZDUSERNAME'), os.getenv('ZDPASSWORD')))
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print(url, ' Status:', response.status_code, 'Problem with the request . Exiting.')
        raise Exception()

    return response.json()


def get_tickets(userid):
    # Format http request
    url = 'https://%s/api/v2/users/%s/tickets/assigned.json' % (os.getenv('ZDADDRESS'), userid)
    data = get_url(url)
    tickets = data['tickets']

    now = dateutil.parser.parse((datetime.datetime.utcnow()).isoformat("T") + "Z")

    updated_tickets = []
    for ticket in tickets:

        updated_at = dateutil.parser.parse(ticket['updated_at'])
        time_diff = int((now - updated_at).total_seconds() / 60 / 60)

        # Only get tickets updated within the last 12 hours
        if time_diff < 13:
            updated_tickets.append(ticket)

    return updated_tickets


def get_time_spent(userid, ticketid):
    url = 'https://%s/api/v2/tickets/%s/audits.json' % (os.getenv('ZDADDRESS'), ticketid)
    data = get_url(url)
    audits = data['audits']

    total = 0
    now = dateutil.parser.parse((datetime.datetime.utcnow()).isoformat("T") + "Z")

    for audit in audits:
        created_at = dateutil.parser.parse(audit['created_at'])
        time_diff = int((now - created_at).total_seconds() / 60 / 60)

        if time_diff < 13 and audit['author_id'] == int(userid):
                for event in audit['events']:
                    if 'field_name' in event and event['field_name'] == '23991343':
                        total += int(event['value'])

    return total


def get_total_time_spent(userid):
    total = 0
    tickets = get_tickets(userid)
    for ticket in tickets:
        ts = get_time_spent(userid, ticket['id'])
        print "USER:%s TICKET:%s TS:%s" % (userid,ticket['id'],ts)
        total += ts

    print "USER:%s TOTALTS:%s" % (userid, total)
    return total


def get_userid(email):
    # Format http request
    url = 'https://%s/api/v2/users/search.json?query=%s' % (os.getenv('ZDADDRESS'), email)
    data = get_url(url)
    users = data['users']

    userid = users[0]['id']

    return userid


def get_email(userid):
    # Format http request
    url = 'https://%s/api/v2/users/%s.json' % (os.getenv('ZDADDRESS'), userid)
    data = get_url(url)
    users = data['users']

    email = users[0]['email']

    return email