import os

from fastapi import APIRouter
from xmlCache import  cache
from pydantic import BaseModel
from soapConnector import SoapConector
import xml.etree.ElementTree as ET

current_filename = os.path.basename(__file__).split('.')[0]
print(current_filename)
template = cache.get_xml_string(current_filename)

class Subscribe(BaseModel):
    CustomerId: str #is MSISDN of the customer
    Package:  str #the bundle for subscription 
    MessageId: str #subscription extra optional info
def get_auth_credentials(template):
    root = ET.fromstring(template)
    
    # XML namespaces required to find elements within the provided XML string
    namespaces = {
        'wsse': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd',
    }
    
    # Extract Username and Password
    username_path = './/wsse:Username'
    password_path = './/wsse:Password'
    
    username_element = root.find(username_path, namespaces=namespaces)
    password_element = root.find(password_path, namespaces=namespaces)
    
    username = username_element.text if username_element is not None else None
    password = password_element.text if password_element is not None else None
    print(username, password)
    return username, password

def requestHandler( subscribe):
        req =template.replace('MSISD', subscribe.CustomerId).replace('Bundlename', subscribe.Package).replace('test', subscribe.MessageId)
        print(req)
        pass
def onSucess(resp:str):
    pass
def onError(err:str):
    return{
         "status": err
    }
connector = SoapConector('43.250.139.33:10415/TisService', template, get_auth_credentials(template), onSucess,onError)
router = APIRouter()
@router.get("/subscription")
def subscriptions():
    return [{'name':'sub1', 'value':999}]


    
    
@router.post("/subscription")
def subscription(subscribe:Subscribe):
    print(subscribe)
    resp=connector.despatch(requestHandler(subscribe))
    return resp
