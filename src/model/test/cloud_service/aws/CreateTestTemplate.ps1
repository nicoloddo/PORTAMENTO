param (
    [string]$originalTemplatePath,
    [string]$newTemplatePath
)

# Define the LocalStack replacements
$fetchQueueUrlReplacement = '"http://sqs.eu-west-3.localhost.localstack.cloud:4566/000000000000/portamento-fetch-queue"'
$mergeQueueUrlReplacement = '"http://sqs.eu-west-3.localhost.localstack.cloud:4566/000000000000/portamento-merge-queue"'
$endpointUrlReplacement = '"http://host.docker.internal:4566"'
$roleReplacement = 'Role: arn:aws:iam::000000000000:role/lambda-ex'

# Read the original template
$content = Get-Content $originalTemplatePath -Raw

# Modify the ImageUri values
$modifiedContent = $content -replace 'ImageUri: .*/', 'ImageUri: '

# Modify the Role values
$modifiedContent = $modifiedContent -replace 'Role: .*', $roleReplacement

# Replace the CloudFormation references with LocalStack values
$modifiedContent = $modifiedContent -replace '!GetAtt PortamentoFetchQueue.QueueUrl', $fetchQueueUrlReplacement
$modifiedContent = $modifiedContent -replace '!GetAtt PortamentoMergeQueue.QueueUrl', $mergeQueueUrlReplacement

# Add the ENDPOINT_URL to the Globals section
$globalsPattern = '(Globals:\s+Function:\s+Environment:\s+Variables:)'
$endpointInsertion = "`$1`n        ENDPOINT_URL: $endpointUrlReplacement"
$modifiedContent = $modifiedContent -replace $globalsPattern, $endpointInsertion

# Write the modified content to the new template
Set-Content $newTemplatePath $modifiedContent

Write-Host "Modified template.yml has been created."
