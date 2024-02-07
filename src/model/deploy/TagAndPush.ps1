# Define AWS account ID and region
$awsAccountId = Read-Host "Please enter your AWS Account ID"
$awsRegion = "eu-west-3"

# Define the path to your template.yml file
$templateFilePath = "..\template.yml"

# Read the contents of the template.yml file
$templateFileContent = Get-Content -Path $templateFilePath

# Login to docker-aws
aws ecr get-login-password --region $awsRegion | docker login --username AWS --password-stdin "$awsAccountId.dkr.ecr.$awsRegion.amazonaws.com"

# Process each line to find and handle ImageUri entries
foreach ($line in $templateFileContent) {
    if ($line.Trim().StartsWith("ImageUri:")) {
        # Extract the full ECR image name
        $fullEcrImageName = $line.Trim().Substring("ImageUri:".Length).Trim()

        # Extract just the image name (repository and tag) from the full ECR image name
        $imageName = $fullEcrImageName -replace "$awsAccountId\.dkr\.ecr\.$awsRegion\.amazonaws\.com\/", ""

        # Extract the repository name from the image name
        $repositoryName = $imageName.Split(":")[0]

        # Print the image names
        Write-Host "Local Image Name: $imageName"
        Write-Host "Full ECR Image Name: $fullEcrImageName"
        Write-Host "Repository Name: $repositoryName"

        # Wait for user confirmation to continue
        Read-Host -Prompt "Press Enter to continue or Ctrl+C to abort"

        # Check if the repository exists
        $repoExists = aws ecr describe-repositories --region $awsRegion --repository-names $repositoryName 2>&1
        if ($repoExists -like "*RepositoryNotFoundException*") {
            # Create repository if it doesn't exist
            Write-Host "Creating repository: $repositoryName"
            aws ecr create-repository --repository-name $repositoryName --region $awsRegion
        }

        # Retagging the local image with the ECR image name
        docker tag $imageName $fullEcrImageName

        # Push the image to ECR
        docker push $fullEcrImageName
    }
}
