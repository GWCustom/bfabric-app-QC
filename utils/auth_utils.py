
import requests
import json
import datetime
import bfabric
from dash import html
import os
import dash_bootstrap_components as dbc

VALIDATION_URL = "https://fgcz-bfabric.uzh.ch/bfabric/rest/token/validate?token="
HOST = "fgcz-bfabric.uzh.ch"

def token_to_data(token: str) -> str: 

    if not token:
        return None

    validation_url = VALIDATION_URL + token
    res = requests.get(validation_url, headers={"Host": HOST})
    
    if res.status_code != 200:
        res = requests.get(validation_url)
    
        if res.status_code != 200:
            return None
    try:
        master_data = json.loads(res.text)
    except:
        return None
    
    if True: 

        userinfo = json.loads(res.text)
        expiry_time = userinfo['expiryDateTime']
        current_time = datetime.datetime.now()
        five_minutes_later = current_time + datetime.timedelta(minutes=5)

        # Comparing the parsed expiry time with the five minutes later time

        if not five_minutes_later <= datetime.datetime.strptime(expiry_time, "%Y-%m-%d %H:%M:%S"):
            return "EXPIRED"
        
        token_data = dict(
            environment = userinfo['environment'],
            user_data = userinfo['user'],
            token_expires = expiry_time,
            entity_id_data = userinfo['entityId'],
            entityClass_data = userinfo['entityClassName'],
            webbase_data = validation_url.split('rest')[0],
            application_params_data = {},
            application_data = str(userinfo['applicationId']),
            userWsPassword = userinfo['userWsPassword']
        )

        return json.dumps(token_data)
    

def token_response_to_bfabric(token_response: dict) -> str:

    bfabric_wrapper = bfabric.Bfabric(login=token_response['user_data'], password=token_response['userWsPassword'], webbase=token_response['webbase_data'])

    return bfabric_wrapper


    
def entity_data(token_data: dict) -> str: 

    """
    This function takes in a token from bfabric, and returns the entity data for the token.
    Edit this function to change which data is stored in the browser for this entity.
    """

    entity_class_map = {
        "Run": "run",
        "Sample": "sample",
        "Project": "container",
        "Order": "container",
        "Container": "container",
        "Plate": "plate"
    }

    if not token_data:
        return None

    wrapper = token_response_to_bfabric(token_data)
    entity_class = token_data.get('entityClass_data', None)
    endpoint = entity_class_map.get(entity_class, None)
    entity_id = token_data.get('entity_id_data', None)

    if wrapper and entity_class and endpoint and entity_id:
        xml = wrapper.read_object(endpoint=endpoint, obj={"id":entity_id})[0]
        
        if type(xml) == type(None):
            pass # TODO
        elif xml.type != "Quality Control":
            pass # TODO
        elif xml.status == "finished":
            pass # TODO

        bfabric_positions = []
        bfabric_ids = []

        for x in range(len(xml.sample)):  #for all samples on plate
            bfabric_positions.append(xml.sample[x]._gridposition)  # get sample plate position
            bfabric_ids.append(xml.sample[x]._id) # get sample id

    else:
        return None

    json_data = json.dumps({
        "createdby": xml.createdby, 
        "created": xml.created,
        "modified": xml.modified,
        "name": xml.name,
        "sample_data":{
            "Well":bfabric_positions, 
            "ids":bfabric_ids
        },
        "type":xml.type,
    })
    return json_data


def send_bug_report(token_data, entity_data, description):

    mail_string = f"""
    BUG REPORT FROM QC-UPLOADER
        \n\n
        token_data: {token_data} \n\n 
        entity_data: {entity_data} \n\n
        description: {description} \n\n
        sent_at: {datetime.datetime.now()} \n\n
    """

    mail = f"""
        echo "{mail_string}" | mail -s "Bug Report" gwtools@fgcz.system
    """

    print("MAIL STRING:")
    print(mail_string)

    print("MAIL:")
    print(mail)

    os.system(mail)

    return True