import requests, json
from hesabe import crypt

key = None
iv = None
accessCode = None
base_url = None


class Hesabe(object):
    def __init__(self, data):
        self.data = data

    def checkout(self):
        # print('Original data: ', type(self.data))
        try:
            encrypted = crypt.encrypt(str(json.dumps(self.data)), key, iv)
        except:
            return{'error': 'key or iv is incorrect please check'}
        payload = encrypted
        # print('\nencrypted data: ', payload)
        response = requests.request("POST", base_url+"/checkout", headers={'accessCode': accessCode,
                                                                           'Accept': 'application/json'},
                                    data={'data': payload})
        # print('\nresponse encrypted data: ', response.text)
        try:
            decrypted = crypt.decrypt(response.text, key, iv)
            decrypted_json = json.loads(decrypted)
            payment_token = decrypted_json["response"]["data"]
            response_data = {"payment_url": base_url+"/payment?data="+payment_token}
            return json.dumps(response_data)
        except:
            return {'error': "Authentication failed, please check access code"}
