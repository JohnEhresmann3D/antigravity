# Convert images to PNG for Godot
Add-Type -AssemblyName System.Drawing

$sourcePath = "C:\Users\ehres\.gemini\antigravity\brain\cce17eb0-eea9-44fc-899d-8c408d30625f"
$projectPath = "d:\GameDevelopment\Godot\Games\antigravity"

$fileMappings = @{
    "cosmo_sprite_sheet_1767766990282.png" = "assets\sprites\characters\cosmo_spritesheet.png"
    "space_station_background_1767767266818.png" = "assets\backgrounds\space_station_bg.png"
    "platform_tileset_1767767292015.png" = "assets\sprites\tilesets\platform_tileset.png"
    "environment_objects_1767767321985.png" = "assets\sprites\environment\objects_static.png"
    "flowers_animated_1767767426586.png" = "assets\sprites\environment\flowers_animated.png"
    "hazards_animated_1767767458150.png" = "assets\sprites\environment\hazards_animated.png"
    "enemy_flyer_spritesheet_1767767825731.png" = "assets\sprites\enemies\flyer_drone.png"
    "enemy_turret_spritesheet_1767767851975.png" = "assets\sprites\enemies\turret.png"
    "enemy_antigrav_spritesheet_1767767880694.png" = "assets\sprites\enemies\antigrav_orb.png"
    "projectiles_updated_1767768439721.png" = "assets\sprites\enemies\projectiles.png"
}

Write-Host "Converting images..." -ForegroundColor Cyan

foreach ($mapping in $fileMappings.GetEnumerator()) {
    $sourceFile = Join-Path $sourcePath $mapping.Key
    $destFile = Join-Path $projectPath $mapping.Value
    
    if (Test-Path $sourceFile) {
        try {
            Write-Host "Converting: $($mapping.Key)" -ForegroundColor Yellow
            $image = [System.Drawing.Image]::FromFile($sourceFile)
            $image.Save($destFile, [System.Drawing.Imaging.ImageFormat]::Png)
            $image.Dispose()
            Write-Host "  Success" -ForegroundColor Green
        }
        catch {
            Write-Host "  Failed: $_" -ForegroundColor Red
        }
    }
}

Write-Host "Done! Reload Godot project." -ForegroundColor Cyan
