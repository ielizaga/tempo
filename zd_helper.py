import requests
import os
import time


def get_url(url):
    response = requests.get(url, auth=(os.getenv('ZDUSERNAME'), os.getenv('ZDPASSWORD')))
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request . Exiting.')
        raise Exception()

    return response.json()


def get_tickets(userid):
    # Format http request
    url = 'https://discuss.zendesk.com/api/v2/users/%s/tickets/assigned.json' % userid
    data = get_url(url)
    tickets = data['tickets']

    updated_tickets = []
    for ticket in tickets:
        # Only get tickets updated today
        if time.strftime("%Y-%m-%d") in ticket['updated_at']:
            updated_tickets.append(ticket)

    print "### User %s has updated %s tickets today" % (userid, len(updated_tickets))
    return updated_tickets


def get_time_spent(userid, ticketid):
    url = 'https://discuss.zendesk.com/api/v2/tickets/%s/audits.json' % ticketid
    data = get_url(url)
    audits = data['audits']

    total = 0

    for audit in audits:
        if time.strftime("%Y-%m-%d") in audit['created_at'] and audit['author_id'] == int(userid):
                for event in audit['events']:
                    if 'field_name' in event and event['field_name'] == '23991343':
                        total += int(event['value'])

    return total


def get_total_time_spent(userid):
    total = 0
    tickets = get_tickets(userid)
    for ticket in tickets:
        ts = get_time_spent(userid, ticket['id'])
        print "ts %s" % ts
        total += ts

    print "### User %s has logged %s seconds today" % (userid,total)
    return total


def get_userid(email):
    # Format http request
    url = 'https://discuss.zendesk.com/api/v2/users/search.json?query=%s' % email
    data = get_url(url)
    users = data['users']

    userid = users[0]['id']

    return userid


def get_email(userid):
    # Format http request
    url = 'https://discuss.zendesk.com/api/v2/users/%s.json' % userid
    data = get_url(url)
    users = data['users']

    email = users[0]['email']

    return email