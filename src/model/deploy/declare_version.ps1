# Define the path to your template.yml file
$templateFilePath = "..\template.yml"

# Check if the template file exists
if (-not (Test-Path -Path $templateFilePath)) {
    Write-Host "The template.yml file does not exist in the specified directory."
    pause
    exit
}

# Read the contents of the template.yml file
$templateContent = Get-Content -Path $templateFilePath

# Initialize an empty array to store the full ECR image names
$fullEcrImageNames = @()

# Iterate over each line in the template file
foreach ($line in $templateContent) {
    if ($line.Trim().StartsWith("ImageUri:")) {
        # Extract the full ECR image name
        $fullEcrImageName = $line.Trim().Substring("ImageUri:".Length).Trim()
        
        # Add the extracted image name to the array
        $fullEcrImageNames += $fullEcrImageName
    }
}

# If no ImageUri found, exit
if ($fullEcrImageNames.Count -eq 0) {
    Write-Host "No ImageUri found in the template."
    exit
}

# Display current ImageUris and ask for new tag
foreach ($uri in $fullEcrImageNames) {
    Write-Host "Found ImageUri: $uri"
}

$newTag = Read-Host -Prompt "Enter new tag"

# Update ImageUri tags in the template content
foreach ($uri in $fullEcrImageNames) {
    $parts = $uri -split ':'
    $baseUri = $parts[0..($parts.Count - 2)] -join ':'
    $newUri = "${baseUri}:$newTag"
    $templateContent = $templateContent -replace [regex]::Escape($uri), $newUri
}

# Write the updated content back to the template file
$templateContent | Set-Content -Path $templateFilePath

Write-Host "All ImageUri tags have been updated in the template.yml file."

pause
