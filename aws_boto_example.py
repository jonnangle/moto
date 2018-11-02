import boto3
import time
from moto import mock_sqs, mock_dynamodb2


def get_populated_dynamodb_table(tablename):
    client = boto3.client('dynamodb')
    response = client.create_table(
        TableName=tablename,
        KeySchema=[{
            'AttributeName': 'message',
            'KeyType': 'HASH'
        }, {
            'AttributeName': 'delay',
            'KeyType': 'RANGE'
        }],
        AttributeDefinitions=[{
            'AttributeName': 'message',
            'AttributeType': 'S'
        }, {
            'AttributeName': 'delay',
            'AttributeType': 'N'
        }],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        })
    print("Magic DynamoDB table created at", response["TableDescription"]["TableArn"])

    # vvv This is not needed on moto, but definitely needed on real AWS!
    waiter = client.get_waiter('table_exists')
    waiter.wait(
        TableName=tablename, WaiterConfig={
            'Delay': 5,
            'MaxAttempts': 20
        })

    for i in range(1, 11):
        client.put_item(
            TableName=tablename,
            Item={
                'message': {
                    'S': '{} green bottle{}'.format(i, '' if i == 1 else 's')
                },
                'delay': {
                    'N': str(10 - i)
                }
            })


def push_dynamodb_records_to_sqs(table, queuename):
    sqs = boto3.client('sqs')
    dynamodb = boto3.resource('dynamodb')
    queue_url = sqs.create_queue(
        QueueName=queuename
    )['QueueUrl']
    print("Magic SQS queue created at", queue_url)

    results = dynamodb.Table(table).scan()["Items"]

    for entry in results:
        print("--> Pushing message '{}' to SQS with delay={}s".
            format(entry["message"],entry["delay"]))
        sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=int(entry["delay"]),
            MessageBody=entry["message"],
        )
    return queue_url


def poll_sqs(queue_url):
    client = boto3.client('sqs')

    print("Polling SQS...")

    messages_to_read = 10
    while messages_to_read > 0:
        time.sleep(0.2)
        messages = client.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=2)
        if 'Messages' in messages:
            for message in messages['Messages']:
                print(message['Body'])
                client.delete_message(
                    QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
                messages_to_read -= 1
    print("No more green bottles!")


def cleanup(table, queue):
    boto3.resource('dynamodb').Table(table).delete()
    boto3.resource('sqs').get_queue_by_name(QueueName=queue).delete()


@mock_dynamodb2
@mock_sqs
def run(table, queue):
    get_populated_dynamodb_table(table)
    queue_url = push_dynamodb_records_to_sqs(table, queue)
    poll_sqs(queue_url)
    cleanup(table, queue)


if __name__ == "__main__":
    run('bottles', 'bottles_queue')
