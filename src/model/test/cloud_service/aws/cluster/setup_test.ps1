# Start LocalStack in detached mode
localstack start -d

# Create bucket
aws --endpoint-url=http://localhost:4566 s3 mb s3://portamento-bucket

# Create queues
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name portamento-fetch-queue
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name portamento-merge-queue

# Load the data.csv to try the plain clusterer
$key = "34ec81b9-33be-4ff4-95c8-262f22957ed6-1703073359/data.csv"
aws s3 cp ./data.csv s3://portamento-bucket/$key --endpoint-url=http://localhost:4566

# Load the half_model.pkl to try the online learning clusterer
aws s3 cp ./second_half_data.csv s3://portamento-bucket/online-learning-test/data.csv --endpoint-url=http://localhost:4566
aws s3 cp ./half_model.pkl s3://portamento-bucket/default/model.pkl --endpoint-url=http://localhost:4566

# Set the template path and start the testing shell

# Link the original template path
$TEMPLATE_PATH = "../../../../template.yml"
# Link the new modified copy saving path
$TEST_TEMPLATE_PATH = "./template.yml"
# Set the path to call inside the folders of this test
$NEW_RELATIVE_TEMPLATE_PATH = "../template.yml"

# Create a template file with no ecr image uri to invoke locally
& "..\CreateTestTemplate.ps1" -originalTemplatePath $TEMPLATE_PATH -newTemplatePath $TEST_TEMPLATE_PATH

# Start a new PowerShell process, setting the new TEST_TEMPLATE_PATH as TEMPLATE_PATH in that process
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "`$TEMPLATE_PATH = '$NEW_RELATIVE_TEMPLATE_PATH'; Write-Host `"TEMPLATE_PATH is set to: `$TEMPLATE_PATH that contains a modified copy of the original template.`"; Write-Host 'You can use this shell to perform the tests, enter in the respective folder to execute the test because they do not work from the root path of the tests.'; ls; pause"