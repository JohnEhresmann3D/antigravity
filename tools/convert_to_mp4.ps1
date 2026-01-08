<#
.SYNOPSIS
    Converts video files to MP4 format using ffmpeg.

.DESCRIPTION
    This script converts video files to MP4 format with H.264 video codec and AAC audio codec.
    It supports single file conversion or batch conversion of all video files in a directory.

.PARAMETER InputPath
    Path to the input video file or directory containing video files.

.PARAMETER OutputPath
    Optional. Path for the output MP4 file or directory. If not specified, outputs to the same location with _converted suffix.

.PARAMETER Quality
    Optional. Video quality preset: 'high', 'medium', or 'low'. Default is 'high'.

.PARAMETER Overwrite
    Optional. If specified, will overwrite existing output files without prompting.

.EXAMPLE
    .\convert_to_mp4.ps1 -InputPath "video.avi"
    Converts video.avi to video_converted.mp4

.EXAMPLE
    .\convert_to_mp4.ps1 -InputPath "video.avi" -OutputPath "output.mp4" -Quality medium
    Converts video.avi to output.mp4 with medium quality

.EXAMPLE
    .\convert_to_mp4.ps1 -InputPath "C:\Videos" -Overwrite
    Converts all video files in C:\Videos directory to MP4 format
#>

param(
    [Parameter(Mandatory = $true, HelpMessage = "Path to input video file or directory")]
    [string]$InputPath,
    
    [Parameter(Mandatory = $false, HelpMessage = "Path for output MP4 file or directory")]
    [string]$OutputPath = "",
    
    [Parameter(Mandatory = $false, HelpMessage = "Quality preset: high, medium, or low")]
    [ValidateSet('high', 'medium', 'low')]
    [string]$Quality = 'high',
    
    [Parameter(Mandatory = $false, HelpMessage = "Overwrite existing files without prompting")]
    [switch]$Overwrite
)

# Quality presets (CRF values: lower = better quality, larger file)
$qualitySettings = @{
    'high'   = 18
    'medium' = 23
    'low'    = 28
}

$crf = $qualitySettings[$Quality]

# Check if ffmpeg is available
function Test-FFmpeg {
    try {
        $null = ffmpeg -version 2>&1
        return $true
    }
    catch {
        return $false
    }
}

# Convert a single video file
function Convert-VideoToMP4 {
    param(
        [string]$InputFile,
        [string]$OutputFile
    )
    
    Write-Host "Converting: $InputFile" -ForegroundColor Cyan
    Write-Host "Output: $OutputFile" -ForegroundColor Cyan
    
    # Build ffmpeg command
    $ffmpegArgs = @(
        '-i', $InputFile,
        '-c:v', 'libx264',           # H.264 video codec
        '-crf', $crf,                # Quality setting
        '-preset', 'medium',         # Encoding speed/compression ratio
        '-c:a', 'aac',               # AAC audio codec
        '-b:a', '192k',              # Audio bitrate
        '-movflags', '+faststart',   # Enable streaming
        '-pix_fmt', 'yuv420p'        # Pixel format for compatibility
    )
    
    if ($Overwrite) {
        $ffmpegArgs += '-y'
    }
    else {
        $ffmpegArgs += '-n'
    }
    
    $ffmpegArgs += $OutputFile
    
    # Execute ffmpeg
    try {
        & ffmpeg $ffmpegArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Successfully converted: $OutputFile" -ForegroundColor Green
            
            # Show file size comparison
            $inputSize = (Get-Item $InputFile).Length / 1MB
            $outputSize = (Get-Item $OutputFile).Length / 1MB
            Write-Host ("  Input size: {0:N2} MB" -f $inputSize) -ForegroundColor Gray
            Write-Host ("  Output size: {0:N2} MB" -f $outputSize) -ForegroundColor Gray
            return $true
        }
        else {
            Write-Host "✗ Failed to convert: $InputFile" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "✗ Error converting $InputFile : $_" -ForegroundColor Red
        return $false
    }
}

# Main script logic
function Main {
    # Check if ffmpeg is installed
    if (-not (Test-FFmpeg)) {
        Write-Host "ERROR: ffmpeg is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Please install ffmpeg from: https://ffmpeg.org/download.html" -ForegroundColor Yellow
        Write-Host "Or install via chocolatey: choco install ffmpeg" -ForegroundColor Yellow
        exit 1
    }
    
    # Check if input path exists
    if (-not (Test-Path $InputPath)) {
        Write-Host "ERROR: Input path does not exist: $InputPath" -ForegroundColor Red
        exit 1
    }
    
    $inputItem = Get-Item $InputPath
    $successCount = 0
    $failCount = 0
    
    # Handle directory input
    if ($inputItem.PSIsContainer) {
        Write-Host "Processing directory: $InputPath" -ForegroundColor Yellow
        
        # Common video file extensions
        $videoExtensions = @('*.avi', '*.mov', '*.wmv', '*.flv', '*.mkv', '*.webm', '*.m4v', '*.mpg', '*.mpeg', '*.3gp', '*.ogv')
        
        $videoFiles = Get-ChildItem -Path $InputPath -File -Include $videoExtensions
        
        if ($videoFiles.Count -eq 0) {
            Write-Host "No video files found in directory" -ForegroundColor Yellow
            exit 0
        }
        
        Write-Host "Found $($videoFiles.Count) video file(s)" -ForegroundColor Yellow
        
        foreach ($file in $videoFiles) {
            $outputFile = if ($OutputPath) {
                Join-Path $OutputPath ($file.BaseName + "_converted.mp4")
            }
            else {
                Join-Path $file.DirectoryName ($file.BaseName + "_converted.mp4")
            }
            
            if (Convert-VideoToMP4 -InputFile $file.FullName -OutputFile $outputFile) {
                $successCount++
            }
            else {
                $failCount++
            }
            
            Write-Host "" # Blank line between conversions
        }
    }
    # Handle single file input
    else {
        $outputFile = if ($OutputPath) {
            $OutputPath
        }
        else {
            Join-Path $inputItem.DirectoryName ($inputItem.BaseName + "_converted.mp4")
        }
        
        if (Convert-VideoToMP4 -InputFile $inputItem.FullName -OutputFile $outputFile) {
            $successCount++
        }
        else {
            $failCount++
        }
    }
    
    # Summary
    Write-Host "`n========== Conversion Summary ==========" -ForegroundColor Cyan
    Write-Host "Successful: $successCount" -ForegroundColor Green
    Write-Host "Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { 'Red' } else { 'Gray' })
    Write-Host "Quality: $Quality (CRF: $crf)" -ForegroundColor Gray
    Write-Host "========================================`n" -ForegroundColor Cyan
}

# Run the script
Main
