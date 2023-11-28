localstack start -d

# Create bucket
aws --endpoint-url=http://localhost:4566 s3 mb s3://portamento-bucket

# Create queue
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name portamento-queue