param(
  [string]$Source = "backend/db.sqlite3",
  [string]$DestinationDir = "backups"
)

if (!(Test-Path $Source)) {
  Write-Error "SQLite database file not found: $Source"
  exit 1
}

New-Item -ItemType Directory -Force -Path $DestinationDir | Out-Null
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$destination = Join-Path $DestinationDir "db_backup_$timestamp.sqlite3"
Copy-Item -Path $Source -Destination $destination -Force
Write-Host "Backup written to $destination"
