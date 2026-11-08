# Build the uploadable PoisonLens skill package (PowerShell).
# Windows equivalent of scripts/build-package.sh — keep the two in step.
# Copies ONLY SKILL.md and references/ (the files the UGOS checker allows)
# into dist/poisonlens/, then zips it as dist/poisonlens.zip.
$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $PSScriptRoot
$Dist = Join-Path $Root 'dist'
$Pkg  = Join-Path $Dist 'poisonlens'
$Zip  = Join-Path $Dist 'poisonlens.zip'

if (Test-Path $Pkg) { Remove-Item $Pkg -Recurse -Force }
if (Test-Path $Zip) { Remove-Item $Zip -Force }
New-Item -ItemType Directory -Path (Join-Path $Pkg 'references') -Force | Out-Null

# -Raw / WriteAllText keeps the bytes as committed: no newline rewriting,
# no BOM. The checker reads these files literally.
function Copy-Verbatim($src, $dst) {
  $text = [System.IO.File]::ReadAllText($src)
  [System.IO.File]::WriteAllText($dst, $text, (New-Object System.Text.UTF8Encoding($false)))
}

Copy-Verbatim (Join-Path $Root 'SKILL.md') (Join-Path $Pkg 'SKILL.md')
Get-ChildItem (Join-Path $Root 'references') -Filter *.md | ForEach-Object {
  Copy-Verbatim $_.FullName (Join-Path $Pkg (Join-Path 'references' $_.Name))
}

Compress-Archive -Path $Pkg -DestinationPath $Zip -CompressionLevel Optimal

Write-Output 'Package contents:'
Get-ChildItem $Pkg -Recurse -File | ForEach-Object {
  '{0}  {1} bytes' -f $_.FullName.Substring($Dist.Length + 1), $_.Length
}
Write-Output ('zip: {0} bytes' -f (Get-Item $Zip).Length)
