import json
import psycopg2
from datetime import datetime

# Received message body from AWS SQS
received_message = '''
{
    "user_id": "123",
    "device_id": "device123",
    "ip": "192.168.0.1",
    "locale": "en_US",
    "app_version": 1,
    "create_date": "2023-08-15"
}
'''

# Load received message as JSON
message_data = json.loads(received_message)

# Mask device_id and ip, while preserving their uniqueness
masked_device_id = f"device_{hash(message_data['device_id'])}"
masked_ip = f"ip_{hash(message_data['ip'])}"

# PostgreSQL connection parameters
db_params = {
    "dbname": "user_logins",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Connect to PostgreSQL
try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Insert masked data into the user_logins table
    insert_query = """
    INSERT INTO user_logins
    (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        message_data['user_id'],
        masked_device_id,
        masked_ip,
        message_data['locale'],
        message_data['app_version'],
        datetime.strptime(message_data['create_date'], "%Y-%m-%d").date()
    ))

    connection.commit()
    print("Data inserted successfully.")

except (Exception, psycopg2.Error) as error:
    print("Error:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection closed.")

