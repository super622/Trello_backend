from decimal import Decimal
import graphene
import boto3
from graphene_sqlalchemy import SQLAlchemyObjectType
from boto3.dynamodb.conditions import Key

from models import *

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2', endpoint_url='http://localhost:8000')

class ListType(SQLAlchemyObjectType):
    class Meta:
        model = List

class CardType(SQLAlchemyObjectType):
    class Meta:
        model = Card

class CommentType(SQLAlchemyObjectType):
    class Meta:
        model = Comment

class DescriptionType(SQLAlchemyObjectType):
    class Meta:
        model = Description

class Query(graphene.ObjectType):
    cards = graphene.List(CardType)
    comments = graphene.List(CommentType)
    descriptions = graphene.List(DescriptionType)
    lists = graphene.List(ListType)
    
    def resolve_lists(self, info):
        table = dynamodb.Table('tbl_list')
        items = table.scan()['Items']
        if not items:
            return []
        return [List(**item) for item in items]

    def resolve_cards(self, info):
        table = dynamodb.Table('tbl_card')
        items = table.scan()['Items']
        if not items:
            return []
        return [Card(**item) for item in items]

    def resolve_comments(self, info):
        table = dynamodb.Table('tbl_comments')
        items = table.scan()['Items']
        if not items:
            return []
        return [Comment(**item) for item in items]
    def resolve_descriptions(self, info):
        table = dynamodb.Table('tbl_descriptions')
        items = table.scan()['Items']
        if not items:
            return []
        return [Description(**item) for item in items]


class CreateList(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    lists = graphene.Field(ListType)

    def mutate(self, info, name):
        table = dynamodb.Table('tbl_list')
        print(table.scan()['Items'])
        list = List(id=10, name=name)
        return CreateList(lists=list)

class CreateCard(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        listId = graphene.String(required=True)

    card = graphene.Field(CardType)

    def mutate(self, info, title, listId):
        table = dynamodb.Table('tbl_card')
        max_key = table.item_count
        print(title, (max_key + 1), listId)
        table.put_item(
            Item ={
                'id': (max_key + 1),
                'parentId': listId,
                'title': title
            }
        )
        card = Card(id=(max_key + 1), title=title, parentId=listId)
        return CreateCard(card=card)

class UpdateCard(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=True)
        list_id = graphene.String(required=True)

    card = graphene.Field(CardType)

    def mutate(self, info, id, title, list_id):
        card = Card.query.get(id)
        if card:
            card.title = title
            card.list_id = list_id
            print(f"update card => title : {title} = list id : {list_id}")
            return UpdateCard(card=card)
        return None

class UpdateList(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    id = graphene.ID()
    name = graphene.String()

    def mutate(self, info, id, name):
        table = dynamodb.Table('tbl_list')
        response = table.scan(
            FilterExpression=Key('id').eq(Decimal(id))
        )
        item_to_delete = response.get('Items', [])[0] if response.get('Items') else None
        print(item_to_delete)
        if item_to_delete:
            # Delete the item
            response = table.update_item(
                Key={
                    "id": item_to_delete['id']
                },
                UpdateExpression="set #name = :n",
                ExpressionAttributeNames={
                    "#name": "name",
                },
                ExpressionAttributeValues={
                    ":n": name,
                },
                ReturnValues="UPDATED_NEW",
            )
            print(response)

            print(table.scan()['Items'])
            if response:
                print(f"Update list id: {id}")
                return DeleteList(success=True)

        print(f"Failed to Update list id: {id}")
        return DeleteList(success=False)

class DeleteCard(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        card = Card.query.get(id)
        if card:
            print(f"delete card id : {id}")
            return DeleteCard(success=True)
        return DeleteCard(success=False)

class DeleteList(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        print(id)
        table = dynamodb.Table('tbl_list')
        response = table.scan(
            FilterExpression=Key('id').eq(Decimal(id))
        )
        item_to_delete = response.get('Items', [])[0] if response.get('Items') else None
        print(item_to_delete)
        if item_to_delete:
            # Delete the item
            response = table.delete_item(
                Key={
                    'name': item_to_delete['name'],
                    'id': item_to_delete['id']
                }
            )
            print(response)

            print(table.scan()['Items'])
            if response:
                print(f"Delete card id: {id}")
                return DeleteList(success=True)

        print(f"Failed to delete card id: {id}")
        return DeleteList(success=False)

class Mutation(graphene.ObjectType):
    createList = CreateList.Field()
    deleteList = DeleteList.Field()
    updateList = UpdateList.Field()
    createCard = CreateCard.Field()
    updateCard = UpdateCard.Field()
    deleteCard = DeleteCard.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(query=Query)
