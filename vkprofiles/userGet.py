__author__ = 'yuranich'

import requests
from time import sleep
from vkprofiles.settings import *

def getUsersInfo(ids, fields):
    # reqUrl = 'https://api.vk.com/method/users.get?user_id=11837213&v=5.28&access_token={}'.format(myAccessToken)
    r = requests.get(buildUrl('users.get', 'user_ids=%s&fields=%s' % (','.join((map(str, ids))), ','.join(fields)))).json()
    if 'error' in r.keys():
        raise ReferenceError('Error: %s Code: %s' % (r['error']['error_msg'], r['error']['error_code']))
    r = r['response']
    # if 'deactivated' in r[0].keys():
    #     raise FileNotFoundError("User is deactivated")
    return r


def buildUrl(method_name, parameters):
    """read https://vk.com/dev/api_requests"""
    req_url = 'https://api.vk.com/method/{method_name}?{parameters}&v={api_v}'.format(
        method_name=method_name, api_v=apiVersion, parameters=parameters)
    req_url = '{}&access_token={token}'.format(req_url, token=getToken('sergeyToken'))
    req_url = '{}&scope={scp}'.format(req_url, scp='friends')
    return req_url


def getLists(id):
    r = requests.get(buildUrl('friends.getLists', 'user_id=%s' % id)).json()
    if 'error' in r.keys():
        raise ReferenceError('Error: %s Code: %s' % (r['error']['error_msg'], r['error']['error_code']))
    r = r['response']
    # if 'deactivated' in r[0].keys():
    # raise FileNotFoundError("User is deactivated")
    r = r['items']
        # for user_id in r:
        #     result.append(user_id['id'])
    return r


def getUsersInList(user_id, list_id):
    r = requests.get(buildUrl('friends.get', 'user_id=%s&order=name&list_id=%s' % (user_id, list_id))).json()
    if 'error' in r.keys():
        raise ReferenceError('Error: %s Code: %s' % (r['error']['error_msg'], r['error']['error_code']))
    r = r['response']
    return r


def parseUserCircles(user_id):
    lists = getLists(user_id)
    f = open('sergey.circles', 'w', encoding='utf-8')

    for next_list in lists:
        f.write(next_list['name'] + ':')
        users = getUsersInList(user_id, next_list['id'])
        for uid in users['items']:
            f.write(' ' + str(uid))
        f.write('\n')
        sleep(0.2)

    f.close()


def getAllFriendsInfo(user_id):
    r = requests.get(buildUrl('friends.get', 'user_id=%s' % user_id)).json()
    if 'error' in r.keys():
        raise ReferenceError('Error: %s Code: %s' % (r['error']['error_msg'], r['error']['error_code']))
    r = r['response']
    return getUsersInfo(r['items'], fields)

def getEdges(user_id):
    r = requests.get(buildUrl('friends.get', 'user_id=%s' % user_id)).json()
    if 'error' in r.keys():
        raise ReferenceError('Error: %s Code: %s' % (r['error']['error_msg'], r['error']['error_code']))
    r = r['response']
    ids = r['items']
    r = requests.get(buildUrl('friends.getMutual', 'source_uid=%s&target_uids=%s' % (user_id, ','.join((map(str, ids)))))).json()
    if 'error' in r.keys():
        raise ReferenceError('Error: %s Code: %s' % (r['error']['error_msg'], r['error']['error_code']))
    r = r['response']
    result = {}
    f = open('sergey.edges', 'w')
    for x in r:
        key = x['id']
        value = x['common_friends']
        result[key] = value
        for y in value:
            if y not in result:
                f.write(str(key))
                f.write(' ')
                f.write(str(y))
                f.write('\n')
    f.close()


if __name__ == '__main__':
    parseUserCircles(sergeyId)
    result = getAllFriendsInfo(sergeyId)
    result.append(getUsersInfo([sergeyId], fields))
    with open('sergey_friends.json', 'w', encoding='utf-8') as f:
        f.write(str(result))

    getEdges(sergeyId)
