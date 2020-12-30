import json
import boto3

from string import ascii_letters, digits
from random import choice

table = boto3.resource('dynamodb', region_name='us-east-1').Table('order-up')
string_format = ascii_letters + digits
url_base = 'http://orderUp/order/'


def ttl():
    # 7 days
    return 60 * 60 * 24 * 7


def generate_order_id(order_id=None):
    if not order_id:
        order_id = "".join(choice(string_format) for x in range(4))
        print(f'{order_id} generated')
    response = check_order_id(order_id)
    return response


def check_order_id(order_id):
    if 'Item' in table.get_item(Key={'order_id': order_id}):
        order_id = generate_order_id()
    return order_id


def lambda_handler(event, context):
    print('Starting a new group order')
    order_id = generate_order_id()
    response = table.put_item(
        Item={
            'order_id': order_id,
            'ttl': ttl(),
            'owner': event.owner,
            'restaurant': event.restaurant,
            'restaurant_link': event.link,
            'orders': json.dumps({})
        }
    )
    print(f'Wrote order {order_id} to the orderUp table. Status: {response}')

    return {
        'statusCode': 200,
        'body': json.dumps(url_base + order_id)
    }
