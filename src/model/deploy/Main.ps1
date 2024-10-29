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




$push = Read-Host -Prompt "Push? Wait for the builds to have finished before starting! (Y/n)"
# Check if the input is empty and set the default value
if ([string]::IsNullOrWhiteSpace($push) -or $push -eq "Y" -or $push -eq "y") {
    $push = "Y"  # Default value
} else {
    $push = "N"  # Alternative value
}

$newversion = Read-Host -Prompt "Create new version? (Y/n)"
# Check if the input is empty and set the default value
if ([string]::IsNullOrWhiteSpace($newversion) -or $newversion -eq "Y" -or $newversion -eq "y") {
    $newversion = "Y"  # Default value
} else {
    $newversion = "N"  # Alternative value
}

if ($push -eq "Y") {
    if ($newversion -eq "Y") {
        # Versioning
        & "./declare_version.ps1"
    }
    # Push
    & "./tag_push.ps1"
}



$deploy = Read-Host -Prompt "Deploy? (Y/n)"
# Check if the input is empty and set the default value
if ([string]::IsNullOrWhiteSpace($deploy) -or $deploy -eq "Y" -or $deploy -eq "y") {
    $deploy = "Y"  # Default value
} else {
    $deploy = "N"  # Alternative value
}

if ($deploy -eq "Y") {
    & "./build_deploy.ps1"
}

pause