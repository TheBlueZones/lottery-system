import os
import json
import time
from common.utils import check_file, timestamp_to_string
from common.error import UserExistsError, RoleError
from common.consts import ROLES


class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json

        self.__check_user_json()
        self.__check_gift_json()

    def __check_user_json(self):
        check_file(self.user_json)

    def __check_gift_json(self):
        check_file(self.gift_json)

    def __read_users(self, time_to_str=False):
        with open(self.user_json, 'r') as f:
            # print(f.read())
            data = json.loads(f.read())

        if time_to_str == True:
            for username, v in data.items():
                v['create_time'] = timestamp_to_string(v['create_time'])
                v['update_time'] = timestamp_to_string(v['update_time'])
                data[username] = v
        # print(data)
        return data

    def __write_user(self, **user):
        if 'username' not in user:
            raise ValueError('missing username')  # 我说怎么有bug，大小写错了
        if 'role' not in user:
            raise ValueError('missing role')

        user['active'] = True
        user['create_time'] = time.time()
        user['update_time'] = time.time()
        user['gifts'] = []

        users = self.__read_users()

        if user['username'] in users:
            raise UserExistsError('username %s had exits' % user['username'])

        users.update({
            user['username']: user
        })

        json_user = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_user)  # 覆盖了

    def __change_role(self, username, role):
        users = self.__read_users()
        # print(users)
        # t1 = users.values()
        # print(t1)
        # t2 = t1.get(username)
        # print(t2)
        # print(users)
        user = users.get(username)
        # print(users.get(username))
        print(user)
        if not user:
            return False

        if role not in ROLES:
            raise RoleError('not use role %s' % role)

        user['role'] = role
        user['update_time'] = time.time()
        users[username] = user

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)
        return True




if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')

    print(gift_path)
    print(user_path)

    # base = Base(user_path, gift_path)
    base = Base(user_json=user_path, gift_json=gift_path)  #

    # base.write_user(username='001', role='admin')  # json文件提前要加{}
    result = base.change_role(username='001', role='normal')

    print(result)
