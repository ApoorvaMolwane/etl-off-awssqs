ETL OFF A SQS QUEUE

PROJECT GOAL:
The project typically focuses on building an application that can read from AWS, SQS Queue, transform that data and then write to Postgres database. 

REQUIREMENTS:
For building this application the tools and technologies that we will need our Docker, AWSCLI, PSQL, and PYTHON.

PRE-REQUISITES:
The URL we are going to use is: http://localhost:4566/000000000000/login-queue and the PORT is 5432 (Please ensure the PORT number is the same in all the 3 files)
I have used a Windows machine and terminal for running commands

EXECUTION STEPS:

1. Since Docker is being used locally, it has localstack and postgres images we can use locally.
2. Clone the repository:
   git clone https://github.com/ApoorvaMolwane/etl-off-awssqs.git
3. Access the cloned repository:
   cd etl-off-awssqs
4. Run Docker:
   docker-compose up
5. We will be able to see the localstack and postgres images in the Docker
6. Configure if AWSCLI is installed on your local machine
7. I began by configuring the location of my AWSCLI:
   aws configure set default.region us-east-1
8. Create a SQS Queue:
   awslocal sqs create-queue --queue-name login-queue --region us-east-1
9. To test reading a message from the SQS Queue:
   awslocal sqs receive-message --queue-url  http://localhost:4566/000000000000/login-queue --region us-east-1
10. To test the Postgres database and verify the user_logins table:
    psql -d postgres -U postgres -p 5432 -h localhost -W
    postgres=# select * from user_logins;
11. To install the boto library:
    pip install boto3 psycopg2
13. To run the Python code:
    python main.py



How would you deploy this application in production?
For the application to be deployed in production, the best way is to utilize Docker for containerization, since it's cost-effective as we have already installed it in our local machine. Secondly, we could also use Kubernetes along with Docker as it helps tremendously in container orchestration. If the company already has a cloud infrastructure, we could utilize AWS to manage the scalability of the application.

What other components would you want to add to make this production ready?
To make this production ready we need to implement testing, if automated testing is chosen it would be the best. I also strongly feel CI/CD pipelines should be configured so that we can make continuous integrations and deployments possible. Azure DevOps will also be beneficial to use, and also we will be able to track application health better. We can also make certain modifications to the code such as including error handling and logging for better debugging.

How can this application scale with a growing dataset?
The growing dataset is something we should be prepared for as we can't predict the incoming data flow for a certain application. We can make use of Amazon S3 storage options for better scalability of the application. We could also use a distributed queue for better handling of the messages. AWS storage and scalability options are immense and this application will scale best with a growing dataset.

How can PII be recovered later on?
For the PII to be recovered later on, we need to keep the encryption files safe. We need to use proper encryption techniques and implement data retention policies to manage data recovery.

What are the assumptions you made?
The assumptions I made were:
Every installation would be easy ex. Docker, AWSCLI would take up less time and no issues would be given. The time actually taken with errors was different than what I actually assumed. I had to install Docker, and AWSCLI, and double check the images were working on the local machine.






    
   


    
