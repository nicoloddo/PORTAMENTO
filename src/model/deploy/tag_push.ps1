# Define AWS account ID and region
$awsAccountId = Read-Host "Please enter your AWS Account ID"
$awsRegion = "eu-west-3"

# Define the path to your template.yml file
$templateFilePath = "..\template.yml"

# Read the contents of the template.yml file
$templateFileContent = Get-Content -Path $templateFilePath

# Login to docker-aws
aws ecr get-login-password --region $awsRegion | docker login --username AWS --password-stdin "$awsAccountId.dkr.ecr.$awsRegion.amazonaws.com"

$pushAll = Read-Host -Prompt "Push all? (Y/n)"
# Check if the input is empty and set the default value
if ([string]::IsNullOrWhiteSpace($pushAll) -or $pushAll -eq "Y" -or $pushAll -eq "y") {
    $pushAll = "Y"  # Default value
} else {
    $pushAll = "N"  # Alternative value
}

# Process each line to find and handle ImageUri entries
foreach ($line in $templateFileContent) {
    if ($line.Trim().StartsWith("ImageUri:")) {
        # Extract the full ECR image name
        $fullEcrImageName = $line.Trim().Substring("ImageUri:".Length).Trim()

        # Extract just the image name (repository and tag) from the full ECR image name
        $tempName = $fullEcrImageName -replace "$awsAccountId\.dkr\.ecr\.$awsRegion\.amazonaws\.com\/", ""

        # Extract the repository name from the image name
        $repositoryName = $tempName.Split(":")[0]
        $imageName = "${repositoryName}:latest" # the docker build always uses latest as tag

        # Print the image names
        Write-Host "Local Image Name: $imageName"
        Write-Host "Full ECR Image Name: $fullEcrImageName"
        Write-Host "Repository Name: $repositoryName"

        if ($pushAll -eq "N") {
            # Prompt the user
            $userInput = Read-Host -Prompt "Press Enter to continue, type 'skip' to skip this iteration, or Ctrl+C to abort"
            
            # Check if the user wants to skip this iteration
            if ($userInput -eq 'skip') {
                Write-Host "Skipping this iteration."
                continue
            }
        }

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

pause
