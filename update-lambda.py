import json
import boto3

table = boto3.resource('dynamodb', region_name='us-east-1').Table('order-up')

def lambda_handler(event, context):
    order_id = event.id
    new_order = {'main': event.main, 'sides': event.sides, 'drink': event.drink}

    try:
        # super redundant, need to work with boto3 update more or switch to pynamo
        item = table.get_item(Key={'id': order_id})
        ttl = item.get('Item').get('ttl')
        owner = item.get('Item').get('owner')
        restaurant = item.get('Item').get('restaurant')
        restaurant_link = item.get('Item').get('restaurant_link')
        orders = json.load(item.get('Item').get('orders'))
        orders[event.name] = new_order
        json_orders = json.dumps(orders)

        response = table.put_item(
            Item={
                'order_id': order_id,
                'ttl': ttl,
                'owner': event.owner,
                'restaurant': event.restaurant,
                'restaurant_link': event.link,
                'orders': json_orders
            }
        )
        print(f'Overwrote order {order_id} to the orderUp table. Status: {response}')

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
        "orders": json_orders
    }