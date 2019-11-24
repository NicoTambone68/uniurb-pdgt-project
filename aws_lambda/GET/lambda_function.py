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
        if ( event["searchCriteria"] == "Key" ):
            result = table.query(KeyConditionExpression=Key('WineId').eq(event["WineId"]))
            
        elif ( event["searchCriteria"] == "All" ):
            result = table.scan()
            
        elif ( event["searchCriteria"] == "Filter" ):
            
            searchFilter = event['searchFilter']

            if ( searchFilter.get("WineName", "_not_found_") != "_not_found_" ):
                exp=Attr("WineName").contains(event["searchFilter"]["WineName"])
            else:    
                exp=Attr("WineName").exists()

            if ( searchFilter.get("WineType", "_not_found_") != "_not_found_"):
                exp&=Attr("WineType").eq(event["searchFilter"]["WineType"])
            else:
                exp&=Attr("WineType").exists()

            if ( searchFilter.get("WineDishes", "_not_found_") != "_not_found_" ):
                exp&=Attr("WineDishes").contains(event["searchFilter"]["WineDishes"])
            else:
                exp&=Attr("WineDishes").exists()
                
            if ( searchFilter.get("WinePrice", "_not_found_") != "_not_found_" ):
                exp&=Attr("WinePrice").between(event["searchFilter"]["WinePrice"]["From"], event["searchFilter"]["WinePrice"]["To"])
            else:
                exp&=Attr("WineDishes").exists()                

            result=table.scan(FilterExpression=exp)                

        else:
            raise BadRequest("searchCriteria not specified!")
            
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Items'])
        }            
        
    except Exception as e:
        response = {
            "statusCode": 403,
            "msg": str(e),
            "body": json.loads('{"Error":"no data found"}')
    }

    return response




