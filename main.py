import boto3
import psycopg2
import json

# Initialize AWS SQS client
sqs = boto3.client('sqs', region_name='us-east-1', endpoint_url='http://localhost:4566')

# Initialize PostgreSQL connection
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    user='postgres',
    password='postgres',
    database='postgres'
)
cur = conn.cursor()

def mask_duplicate_value(value):
    # Mask the value while retaining the original value for duplicate detection
    return 'MASKED_' + value

def process_message(message):
    data = json.loads(message['Body'])
    
    # Apply data transformation: mask ip and device_id fields
    data['masked_ip'] = mask_duplicate_value(data['ip'])
    data['masked_device_id'] = mask_duplicate_value(data['device_id'])
    
    # Insert masked data into PostgreSQL table
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
    # Receive messages from the SQS queue
    queue_url = 'http://localhost:4566/000000000000/login-queue'
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10
    )
    
    # Process and insert messages into PostgreSQL
    if 'Messages' in response:
        for message in response['Messages']:
            process_message(message)
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
        print(f"Processed and inserted {len(response['Messages'])} messages.")

    # Close PostgreSQL connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
