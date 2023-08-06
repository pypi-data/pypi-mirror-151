# -*- coding: utf-8 -*-
'''
@Time    : 2022/5/18 10:46 AM
@Author  : oujiewen2@shoplineapp.com
@File    : mcHelper.py
'''
import json

from mcHelpers import loginHelper
import sqlUtil

class mcHelper:
    def __init__(self,parmas):
        self.parmas=parmas
        self.hp= loginHelper.loginHelper(self.parmas)
        self.users=json.loads(self.parmas["users"])

    def login(self,userName):
        return self.hp.login_main(self.users[userName],userName)

    def login_all(self):
        for key in self.users:
            self.login(key)
        return self.parmas

    def query_execute(self,sqlStr,storeId=None,mId=None):
        db_config=self.parmas['db_config']
        if storeId!=None:
            tableId=sqlUtil.tableId(storeId,self.parmas['maxID'])
            print(sqlStr)
            sqlStr=sqlStr.format(tableId=tableId)
            print(sqlStr)
            pass
        if mId!=None:
            dbId=2
        # self.db = sqlHelper.MysqlUtil(db_config['dbHost'], int(db_config['dbPort']), db_config['dbUser'],
        #                        db_config['dbPassword'],
        #                        db_config['dbName'])

        # return self.db.query_execute(sqlStr)



if __name__ == '__main__':
    dict={'user_list': '[{"acct":"oujiewen2+xiaohei@shoplineapp.com","pwd":"9baca9a3b4cb6a6195fe559c118d8bcd2f5e9a398a1c486cb571d7cc6f6ae26257e4dda78f85ce1c86f09408d93fb1c5cb830870f45c4c5c51e16528d89545573d41028bdc42290f500ae681a074e31da00b81f29f846f611efd6b182cf8058a4a264ef0e4ef1ee4046fca6ca66283d972173f6a969f5b6cb428564b3b6b94c5","handel":"interface-automation","cookiesName":"小黑"}, { "acct":"oujiewen2+0001@shoplineapp.com", "pwd":"9baca9a3b4cb6a6195fe559c118d8bcd2f5e9a398a1c486cb571d7cc6f6ae26257e4dda78f85ce1c86f09408d93fb1c5cb830870f45c4c5c51e16528d89545573d41028bdc42290f500ae681a074e31da00b81f29f846f611efd6b182cf8058a4a264ef0e4ef1ee4046fca6ca66283d972173f6a969f5b6cb428564b3b6b94c5","handel":"interface-automation","cookiesName":"店长"}, { "acct":"oujiewen2+auto@shoplineapp.com", "pwd":"9baca9a3b4cb6a6195fe559c118d8bcd2f5e9a398a1c486cb571d7cc6f6ae26257e4dda78f85ce1c86f09408d93fb1c5cb830870f45c4c5c51e16528d89545573d41028bdc42290f500ae681a074e31da00b81f29f846f611efd6b182cf8058a4a264ef0e4ef1ee4046fca6ca66283d972173f6a969f5b6cb428564b3b6b94c5","handel":"interface-automation","cookiesName":"商家"}]', 'storeId': '1638944951560', 'users': '{"oujiewen2+xiaohei@shoplineapp.com":{"pwd":"9baca9a3b4cb6a6195fe559c118d8bcd2f5e9a398a1c486cb571d7cc6f6ae26257e4dda78f85ce1c86f09408d93fb1c5cb830870f45c4c5c51e16528d89545573d41028bdc42290f500ae681a074e31da00b81f29f846f611efd6b182cf8058a4a264ef0e4ef1ee4046fca6ca66283d972173f6a969f5b6cb428564b3b6b94c5","handel":"interface-automation","cookiesName":"小黑"},"oujiewen2+0001@shoplineapp.com":{"pwd":"9baca9a3b4cb6a6195fe559c118d8bcd2f5e9a398a1c486cb571d7cc6f6ae26257e4dda78f85ce1c86f09408d93fb1c5cb830870f45c4c5c51e16528d89545573d41028bdc42290f500ae681a074e31da00b81f29f846f611efd6b182cf8058a4a264ef0e4ef1ee4046fca6ca66283d972173f6a969f5b6cb428564b3b6b94c5","handel":"interface-automation","cookiesName":"店长"}}', 'maxID': '64', 'handel': 'https://interface-automation.myshoplinestg.com', 'appid': '1163336839', 'host': 'https://admin.myshoplinestg.com', 'db_config': '{"dbHost":"10.130.84.60","dbPort":6306,"dbUser":"sl_root","dbPassword":"qDoxncq4FI","dbName":"sl_sc_mc_test"}'}
    h=mcHelper(dict)
    # print(h.login_all())
    # # print(h.query_execute("select * from mc_catalog{tableId}"))
    h.query_execute('select * from mc_catalog{tableId}',storeId=2345345345345)
    # print(json.loads(dict["users"]))