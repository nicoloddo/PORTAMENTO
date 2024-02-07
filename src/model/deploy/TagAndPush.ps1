# Define AWS account ID and region
$awsAccountId = Read-Host "Please enter your AWS Account ID"
$awsRegion = "eu-west-3"

# Define the path to your template.yml file
$templateFilePath = "..\template.yml"

# Read the contents of the template.yml file
$templateFileContent = Get-Content -Path $templateFilePath

# Process each line to find and handle ImageUri entries
foreach ($line in $templateFileContent) {
    if ($line.Trim().StartsWith("ImageUri:")) {
        # Extract the full ECR image name
        $fullEcrImageName = $line.Trim().Substring("ImageUri:".Length).Trim()

        # Extract just the image name (repository and tag) from the full ECR image name
        $imageName = $fullEcrImageName -replace "$awsAccountId\.dkr\.ecr\.$awsRegion\.amazonaws\.com\/", ""

        # Print the image names
        Write-Host "Local Image Name: $imageName"
        Write-Host "Full ECR Image Name: $fullEcrImageName"

        # Wait for user confirmation to continue
        Read-Host -Prompt "Press Enter to continue or Ctrl+C to abort"

        # Retagging the local image with the ECR image name
        docker tag $imageName $fullEcrImageName

        # Push the image to ECR
        docker push $fullEcrImageName
    }
}
