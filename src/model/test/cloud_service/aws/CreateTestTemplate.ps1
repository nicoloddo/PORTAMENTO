param (
    [string]$originalTemplatePath,
    [string]$newTemplatePath
)

# Read the original template
$content = Get-Content $originalTemplatePath -Raw

# Modify the ImageUri values
$modifiedContent = $content -replace 'ImageUri: .*/', 'ImageUri: '

# Write the modified content to the new template
Set-Content $newTemplatePath $modifiedContent

Write-Host "Modified template.yml has been created."
