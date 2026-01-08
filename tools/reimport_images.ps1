# Godot Image Reimport Helper
# Run this script if images aren't loading properly in Godot

Write-Host "Godot Image Reimport Helper" -ForegroundColor Cyan
Write-Host "============================`n" -ForegroundColor Cyan

# Check if Godot is running
$godotProcess = Get-Process -Name "Godot*" -ErrorAction SilentlyContinue
if ($godotProcess) {
    Write-Host "[WARN] Godot is currently running!" -ForegroundColor Yellow
    Write-Host "       Please close Godot before continuing.`n" -ForegroundColor Yellow
    
    $response = Read-Host "Close Godot and press Enter to continue (or 'q' to quit)"
    if ($response -eq 'q') {
        exit
    }
}

# Step 1: Run image fixer
Write-Host "[1/3] Validating and fixing image imports..." -ForegroundColor Green
python fix_godot_images.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[ERROR] Image fixer failed!" -ForegroundColor Red
    exit 1
}

# Step 2: Clear import cache
Write-Host "`n[2/3] Clearing Godot import cache..." -ForegroundColor Green
if (Test-Path ".godot\imported") {
    Remove-Item -Path ".godot\imported" -Recurse -Force
    Write-Host "       Cache cleared successfully" -ForegroundColor Green
}
else {
    Write-Host "       No cache to clear" -ForegroundColor Yellow
}

# Step 3: Instructions
Write-Host "`n[3/3] Next steps:" -ForegroundColor Green
Write-Host "       1. Open Godot" -ForegroundColor White
Write-Host "       2. Wait for assets to reimport" -ForegroundColor White
Write-Host "       3. Check FileSystem panel for your images`n" -ForegroundColor White

Write-Host "[SUCCESS] Image reimport preparation complete!" -ForegroundColor Cyan
Write-Host "`nAll images are now ready to be imported by Godot.`n" -ForegroundColor Cyan
