$scriptsDirectory = ".\"
$selfScriptName = $MyInvocation.MyCommand.Name # Get the name of the current script

# Get all .ps1 files in the directory
$scriptFiles = Get-ChildItem -Path $scriptsDirectory -Filter *.ps1

# Loop through each file and open it in a new PowerShell window, excluding the current script
foreach ($file in $scriptFiles) {
    if ($file.Name -ne $selfScriptName) {
        $filePath = $file.FullName
        Start-Process PowerShell -ArgumentList "-File `"$filePath`""
    }
}
