# Start LocalStack in detached mode
localstack start -d

# Set the template path and start the testing shell

# Link the original template path
$TEMPLATE_PATH = "../../../../template.yml"
# Link the new modified copy saving path
$TEST_TEMPLATE_PATH = "./template.yml"
# Set the path to call inside the folders of this test
$NEW_RELATIVE_TEMPLATE_PATH = "../template.yml"

# Build Stack
aws --endpoint-url=http://localhost:4566 cloudformation create-stack --stack-name PortamentoStack --template-body file://$TEST_TEMPLATE_PATH --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM

# Create a template file with no ecr image uri to invoke locally
& "..\CreateTestTemplate.ps1" -originalTemplatePath $TEMPLATE_PATH -newTemplatePath $TEST_TEMPLATE_PATH

# Start a new PowerShell process, setting the new TEST_TEMPLATE_PATH as TEMPLATE_PATH in that process
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "`$TEMPLATE_PATH = '$NEW_RELATIVE_TEMPLATE_PATH'; Write-Host `"TEMPLATE_PATH is set to: `$TEMPLATE_PATH that contains a modified copy of the original template.`"; Write-Host 'You can use this shell to perform the tests, enter in the respective folder to execute the test because they do not work from the root path of the tests.'; ls; pause"
