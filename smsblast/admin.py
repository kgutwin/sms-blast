import os

from smsblast import templates, sms


def render():
    return templates.admin_login()

def main_page(response=''):
    return templates.admin_page(
        os.environ['LEADER_KEY'],
        sms.list_numbers(),
        response=response
    )

def update(data):
    print(data)
    if data.get('leaderkey') != os.environ['LEADER_KEY']:
        return templates.admin_login('Leader key is incorrect')
    elif data.get('action') == 'Send':
        try:
            r = sms.send(data['message'])
            r = f'Message sent!<br>Message ID: {r}'
        except sms.Exception as ex:
            r = str(ex)
        return main_page(response=r)
    elif data.get('number'):
        try:
            r = sms.remove(data['number'])
            r = 'Success' if r else 'Failed...'
        except sms.Exception as ex:
            r = str(ex)
        return main_page(response=r)
    elif data.get('action') == 'Add numbers':
        messages = []
        for number in data['numbers'].split():
            try:
                sms.add(number)
                messages.append(f'Added {number}')
            except sms.Exception as ex:
                messages.append(f'Failed to add {number}: {str(ex)}')
        return main_page(response='<br>'.join(messages))
    else:
        return main_page()        
