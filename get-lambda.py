import os
import json
import boto3

table = boto3.resource('dynamodb', region_name='us-east-1').Table('order-up')

def lambda_handler(event, context):
    order_id = event.get('id')

    try:
        item = table.get_item(Key={'id': order_id})
        owner = item.get('Item').get('owner')
        restaurant = item.get('Item').get('restaurant')
        restaurant_link = item.get('Item').get('restaurant_link')
        orders = item.get('Item').get('orders')

    except:
        return {
            'statusCode': 400,
            'message': 'Order not found!'
        }

    return {
        "statusCode": 200,
        "owner": owner,
        "restaurant": restaurant,
        "restaurant_link": restaurant_link,
        "orders": orders
    }