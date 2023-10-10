param(
    [string]$m = "updated using POSH"
)

Get-ChildItem -Path ".\dist" -Filter "*.tar.gz" | Remove-Item

$content = Get-Content -Path .\setup.py

$content | Where-Object { $_ -match "version='(\d+\.\d+)'" }
$currentVersion = $matches[1]

$versionParts = $currentVersion -split "\." #splits version into two 
$newMinorVersion = [int]$versionParts[1] + 1
$newVersion = "$($versionParts[0]).$newMinorVersion"

$newContent = $content -replace "version='$currentVersion'", "version='$newVersion'"

$newContent | Set-Content -Path .\setup.py

Invoke-Expression "python setup.py sdist"
Invoke-Expression "git add ."   
Invoke-Expression "git commit -m '$m'"
Invoke-Expression "git push"
Invoke-Expression "twine upload dist/*"

# Execute setup.py
