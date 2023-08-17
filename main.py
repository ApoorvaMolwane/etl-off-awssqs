import boto3
import psycopg2
import json

sqs = boto3.client('sqs', region_name='us-east-1', endpoint_url='http://localhost:4566')

conn = psycopg2.connect(
    host='localhost',
    port='5432',
    user='postgres',
    password='postgres',
    database='postgres'
)
cur = conn.cursor()

def mask_duplicate_value(value):
    return 'MASKED_' + value

def process_message(message):
    data = json.loads(message['Body'])
    
    data['masked_ip'] = mask_duplicate_value(data['ip'])
    data['masked_device_id'] = mask_duplicate_value(data['device_id'])
    
    cur.execute("""
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['user_id'],
        data['device_type'],
        data['masked_ip'],
        data['masked_device_id'],
        data['locale'],
        data['app_version'],
        data['create_date']
    ))
    conn.commit()

def main():
    queue_url = 'http://localhost:4566/000000000000/login-queue'
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10
    )
   
    if 'Messages' in response:
        for message in response['Messages']:
            process_message(message)
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
        print(f"Processed and inserted {len(response['Messages'])} messages.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
