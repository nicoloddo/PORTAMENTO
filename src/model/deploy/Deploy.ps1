# ENTRIRE IMPLEMENTATION AND DEPLOYING PIPELINE

$rebuild = Read-Host -Prompt "Rebuild? (y/N)"
# Check if the input is empty and set the default value
if ([string]::IsNullOrWhiteSpace($rebuild)) {
    $rebuild = "N"  # Default value
} else {
    $rebuild = "Y"  # Alternative value
}

if ($rebuild -eq "Y") {
    # Build the containers
    & "./build_all_containers.ps1"
}




$push = Read-Host -Prompt "New Push? Wait for the builds to have finished before starting! (y/N)"
# Check if the input is empty and set the default value
if ([string]::IsNullOrWhiteSpace($push)) {
    $push = "N"  # Default value
} else {
    $push = "Y"  # Alternative value
}

if ($push -eq "Y") {
    # Versioning and push
    & "./declare_version.ps1"
    & "./tag_push"
}




$deploy = Read-Host -Prompt "Deploy? (Y/n)"
# Check if the input is empty and set the default value
if ([string]::IsNullOrWhiteSpace($deploy)) {
    $deploy = "Y"  # Default value
} else {
    $deploy = "N"  # Alternative value
}

if ($deploy -eq "Y") {
    & "./build_deploy"
}

pause