$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Manifest = Get-Content (Join-Path $Root "artifacts\MANIFEST.json") -Raw | ConvertFrom-Json
$Parts = Get-ChildItem (Join-Path $Root "artifacts\extension\*.part") | Sort-Object Name
if ($Parts.Count -ne [int]$Manifest.extension.parts) {
    throw "Expected $($Manifest.extension.parts) extension parts, found $($Parts.Count)"
}
$Base64 = ($Parts | ForEach-Object { (Get-Content $_.FullName -Raw).Trim() }) -join ""
$Bytes = [Convert]::FromBase64String($Base64)
$Sha = [BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($Bytes)).Replace("-", "").ToLowerInvariant()
if ($Sha -ne $Manifest.extension.sha256) {
    throw "SHA-256 mismatch: $Sha"
}
$Release = Join-Path $Root "extension\release"
New-Item -ItemType Directory -Force -Path $Release | Out-Null
$Zip = Join-Path $Release $Manifest.extension.output_name
[IO.File]::WriteAllBytes($Zip, $Bytes)
$Unpacked = Join-Path $Root "extension\unpacked"
if (Test-Path $Unpacked) {
    Remove-Item $Unpacked -Recurse -Force
}
Expand-Archive -Path $Zip -DestinationPath $Unpacked -Force
Write-Host "ZIP: $Zip"
Write-Host "Unpacked extension: $Unpacked"
Write-Host "SHA-256: $Sha"
