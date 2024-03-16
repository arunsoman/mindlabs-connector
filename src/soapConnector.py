from urllib.request import HTTPBasicAuthHandler

import requests

class SoapConector():
    def __init__(self, url:str, template:str, auth,  onOK, onKO) -> None:
        self.soap=template
        self.url = url
        self.onOK=onOK
        self.onKO=onKO
        self.auth = auth
        self.soap_action = None

    def despatch(self, req):
        # soap_request=self.requestHandler(self.soap)
        # if(self.auth is None)
        headers = {'Content-Type': 'text/xml;charset=UTF-8', 'SOAPAction': self.soap_action}
        try:
            response = requests.post(self.url, data=req, headers=headers, auth=self.auth)
        except:
            return self.onKO(-1)
        if response.status_code == 200:
            return self.onOK(response.text)
        else:
            # Handle HTTP errors or SOAP faults here
            print(response.status_code )
            print(response.content)
            return self.onKO(response.text)