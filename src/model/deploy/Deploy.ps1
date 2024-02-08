# Entire implementation and deployment pipeline

$rebuild = Read-Host -Prompt "Rebuild? (y/N)"
# Check if the input is empty and set the default value
if ([string]::IsNullOrWhiteSpace($rebuild)) {
    $rebuild = "N"  # Default value
} else {
    $rebuild = "Y"  # Alternative value
}

if ($rebuild -eq "Y") {
    # Build the containers
    & "./build_all.ps1"
}

& "./declare_version.ps1"
& "./tag_push"

$deploy = Read-Host -Prompt "Deploy? (Y/n)"
# Check if the input is empty and set the default value
if ([string]::IsNullOrWhiteSpace($deploy)) {
    $deploy = "Y"  # Default value
} else {
    $deploy = "N"  # Alternative value
}

if ($deploy -eq "Y") {
    sam build
    sam deploy
}

pause