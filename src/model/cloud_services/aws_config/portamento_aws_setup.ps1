# Create bucket
aws --endpoint-url=http://localhost:4566 s3 mb s3://portamento-bucket

# Create queue
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name portamento-queue

# Add notification configuration of s3
aws --endpoint-url=http://localhost:4566 s3api put-bucket-notification-configuration `
  --bucket portamento-bucket `
  --notification-configuration file://notificationConfig.json # remember to have the notificationConfig.json