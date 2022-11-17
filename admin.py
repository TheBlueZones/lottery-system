import os

from base import Base
from common.error import NotUserError, UserActiveError,RoleError


class Admin(Base):

    def __init__(self, username, user_json, gift_json):
        self.username = username
        super().__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()
        current_user = users.get(self.username)
        if not current_user:
            raise NotUserError('%s user is not exists' % self.username)

        if current_user.get('active') == False:
            raise UserActiveError('%s user is not active' % self.username)

        if current_user.get('role') != 'admin':
            raise RoleError('permission by admin')

        self.user = current_user
        self.role = current_user.get('role')
        self.name = current_user.get('username')
        self.active = current_user.get('active')

    def __check(self, message):
        self.get_user()
        if self.role != 'admin':
            raise Exception(message)

    def add_user(self, username, role):
        self.get_user()
        self.__check('permission')
        self._Base__write_user(username=username, role=role)

    def update_user_active(self, username):
        self.get_user()
        self.__check('permission')
        self._Base__change_active(username=username)

    def update_user_role(self, username, role):
        self.get_user()#动态获取用户信息
        self.__check('permission')
        self._Base__change_role(username=username, role=role)

    def change_gift(self, first_level, second_level,
                 gift_name, gift_count, change):
        self.get_user()
        self.__check('permission')
        self._Base__write_gift(first_level=first_level, second_level=second_level,
                               gift_name=gift_name, gift_count=gift_count,change=change)


if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')

    admin = Admin('001', user_path, gift_path)
    # # admin.update_user_role(username='小慕', role='normals')
    # admin.update_gift(first_level='level1', second_level='level2',
    #                   gift_name='iphone11', gift_count=1000)
    # admin.add_user(username='002', role='normals')
    # admin.update_user_active(username='002')
    admin.change_gift(first_level='level1', second_level='level2',gift_name='iphone12', gift_count=10,change='delete')
    print(admin.user)
