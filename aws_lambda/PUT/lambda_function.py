import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

class BadRequest(Exception):
    pass


def lambda_handler(event, context):
    
    table = dynamodb.Table('PDGT-Wines')

    try:
        
        verb = event.get("Verb")
        
        if (verb == "Insert"):
        
            data = event.get("Data")
            msg = "inserted or updated"
            
            table.put_item(
                Item={
                        "WineId"          : data.get("WineId"),
                        "WinePrice"       : data.get("WinePrice"),
                        "WineAlchohol"    : data.get("WineAlchohol"),
                        "WineDescription" : data.get("WineDescription"),
                        "WineDishes"      : data.get("WineDishes"),
                        "WineImgURL"      : data.get("WineImgURL"),
                        "WineName"        : data.get("WineName"),
                        "WineType"        : data.get("WineType")
                    }
            )        

        elif (verb == "Delete"):
            
            data = event.get("Data")
            msg = "deleted"
            
            table.delete_item(
                Key={
                        'WineId': data.get("WineId")
                    }
            )
            
        else:
            raise BadRequest("Unknown Verb {}".format(verb))
            

        strmsg = "Data correctly {}".format(msg)
        response = {
            "statusCode": 200,
            "body": json.loads('{"Success": "' + strmsg + '"}')
        }                    
        
    except Exception as e:
        response = {
            "statusCode": 403,
            "msg": str(e),
            "body": json.loads('{"Error":"An error occurred. No data have been modified."}')
    }

    return response




