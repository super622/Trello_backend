import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2', endpoint_url='http://localhost:8000')

# def init_db():
#     try:
#         table = dynamodb.Table('tbl_list')
#         table.delete()
#     except Exception as e:
#         print(f"tbl_list delete : {e}")
        
#     try:
#         table = dynamodb.Table('tbl_card')
#         table.delete()
#     except Exception as e:
#         print(f"tbl_card delete : {e}")
    
#     try:
#         table = dynamodb.Table('tbl_comments')
#         table.delete()
#     except Exception as e:
#         print(f"tbl_comments delete : {e}")
    
#     try:
#         table = dynamodb.Table('tbl_descriptions')
#         table.delete()
#     except Exception as e:
#         print(f"tbl_descriptions delete : {e}")

# def init_data():
#     pass


def init_db():
    try:
        table = dynamodb.create_table(
            TableName='tbl_list',
            KeySchema = [
                {
                    'AttributeName': 'name',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput = {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        
        print(f"tbl_list table status: {table != None if table.table_status else 'none'}")
    except Exception as e:
        print(f"tbl_list table status: {e}")
        
    try:
        table = dynamodb.create_table(
            TableName='tbl_card',
            KeySchema = [
                {
                    'AttributeName': 'parentId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'parentId',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput = {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        
        print(f"tbl_card table status: {table != None if table.table_status else 'none'}")
    except Exception as e:
        print(f"tbl_card table status: {e}")
        
    try:
        table = dynamodb.create_table(
            TableName='tbl_comments',
            KeySchema = [
                {
                    'AttributeName': 'card_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'card_id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput = {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        
        print(f"tbl_comments table status: {table != None if table.table_status else 'none'}")
    except Exception as e:
        print(f"tbl_comments table status: {e}")
        
    try:
        table = dynamodb.create_table(
            TableName='tbl_descriptions',
            KeySchema = [
                {
                    'AttributeName': 'card_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'card_id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput = {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        
        print(f"tbl_descriptions table status: {table != None if table.table_status else 'none'}")
    except Exception as e:
        print(f"tbl_descriptions table status: {e}")

def init_data():
    list_data = [
        [1, 'first_list'],
        [2, 'two_list'],
        [3, 'three_list'],
        [4, 'four_list'],
        [5, 'five_list']
    ]
    
    table = dynamodb.Table('tbl_list')
    for data in list_data:
        table.put_item(
            Item={
                'id': data[0],
                'name': data[1],
            }
        )
        
    card_data = [
        [1, 1, 'Card 1'],
        [2, 1, 'Card 2'],
        [3, 1, 'Card 3'],
        [4, 2, 'Card 4'],
        [5, 3, 'Card 5'],
        [6, 2, 'Card 6'],
        [7, 3, 'Card 7'],
        [8, 4, 'Card 8'],
        [9, 4, 'Card 9'],
    ]
    
    table = dynamodb.Table('tbl_card')
    for data in card_data:
        print(data)
        table.put_item(
            Item={
                'id': data[0],
                'parentId': data[1],
                'title': data[2]
            }
        )
