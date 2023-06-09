import requests

import time


class Paiments:
    def __init__(self, api_access_token, number, sum_pay):
        self.api_access_token = api_access_token
        self.number = number
        self.sum_pay = sum_pay

    def qiwi_com_search_mobile(self):
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        search = s.get('https://edge.qiwi.com/qw-mobile-providers-resolver/v1/providers',
                       params={'phoneNumber': self.number})
        if search.status_code != 200:
            return False

        response = search.json()['mobileOperatorProviderList']

        return response

    def send_mobile(self, prv_id):
        s_headers = {}
        s_headers['Accept'] = 'application/json'
        s_headers['Content-Type'] = 'application/json'
        s_headers['authorization'] = 'Bearer ' + self.api_access_token
        postjson = {"id": "", "sum": {"amount": "", "currency": "643"},
                    "paymentMethod": {"type": "Account", "accountId": "643"}, "comment": "",
                    "fields": {"account": ""}}
        postjson['id'] = str(int(time.time() * 1000))
        postjson['sum']['amount'] = self.sum_pay
        postjson['fields']['account'] = self.number[1:]
        postjson['comment'] = ''
        res = requests.post('https://edge.qiwi.com/sinap/api/v2/terms/' + str(prv_id) + '/payments', json=postjson,
                            headers=s_headers)
        return res.json()


if __name__ == '__main__':
    api_access_token = '67f644303e280f897f05f2c2877e3da2'
    prv_id = '25598'
    to_account = '9648325336'
    comment = ''
    sum_pay = 5

    response = Paiments().send_mobile(api_access_token, prv_id, to_account, comment, sum_pay)

    print(response)
