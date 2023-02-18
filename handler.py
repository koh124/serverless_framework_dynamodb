import json

# boto3はAWSで使えるSDK
import boto3
from boto3.dynamodb.conditions import Key, Attr

boto3.client
boto3.resource

dynamodb = boto3.resource('dynamodb')

def lambdaHandler(event, context):
    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        'body': json.dumps({
            "message": "helloworld"
        })
    }

    # DynamoDBテーブルからデータを取得する

    tableName = "usersTable"

    # 【テスト用】イベントjsonにキー名"email","address"で値を指定
    # ソートキーも指定しないと絞り込みできない模様
    # Key = { "email": event["email"], "address": event["address"] }

    Key = { "email": "sample@test.com", "address": "東京都" }
    dynamoTable = dynamodb.Table(tableName)
    fetchData = dynamoTable.get_item(Key=Key)

    print(fetchData) # get_itemすると色んな情報が詰まっている

    item = fetchData["Item"]

    # 【update】updateにはいくつかルールがある
    # ・set
    # フィールドが存在すれば更新する。存在しなければカラムを追加する。
    option = {
        # Keyを指定してupdateするデータを絞り込み
        'Key': Key,

        # UpdateExpressionに更新式（クエリ）を記述する
        # "#SSS"はExpressionAttributeNamesのプロパティを参照する変数,
        # ":TTT"はExpressionAttributeValuesのプロパティを参照する変数
        # 変数名に"-"を含めることはできない
        # DynamoDBの予約語でなければ、AttributeNameはUpdateExpressionに直書きできる
        # しかし、AttributeValuesは直接UpdateExpressionに書くことはできない
        # パーティションキー、ソートキーは更新できない
        # 'UpdateExpression': 'set age = :age', # 可
        'UpdateExpression': 'set #age = :age',
        'ExpressionAttributeNames': {
            "#age": "age",
        },
        'ExpressionAttributeValues': {
            ":age": "25",
        }
    }

    # update_itemはキーワード引数のみを受け付ける
    dynamoTable.update_item(**option) # **はjsのスプレッド構文みたいにdictの引数を分割して渡せる

    # 【delete】
    # deleteはセット型に対してのみ使用可能
    # "#a"が示すプロパティの値から、":a"が示すset型の値を削除する
    # セット型の中身が空になるとプロパティごと消滅する
    # option1 = {
    #     "UpdateExpression": "delete #a :a, #b :a",
    #     "ExpressionAttributeNames": {
    #         "#a": "a",
    #         "#b": "b"
    #     },
    #     "ExpressionAttributeValues": {
    #         ":a": {2}
    #     }
    #     ===before===
    #     {
    #         "a": {1, 2, 3},
    #         "b": {2}
    #     }
    #     ===after===
    #     {
    #         "a": {1, 3}
    #     }
    # }


    body = {
        "input": event,
        "data": item
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
