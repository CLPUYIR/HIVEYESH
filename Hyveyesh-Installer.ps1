<#
.SYNOPSIS
    Hyveyesh Stage 1: The One-Liner Bootstrapper.
    Verifies admin rights, sets up the portable Hyveyesh environment, and launches profiling.

.DESCRIPTION
    1. Elevation check.
    2. Portable Python environment setup in C:\ProgramData\Hyveyesh.
    3. Initialization of Stage 2.
#>

$ErrorActionPreference = "Stop"
$HYVEYESH_ROOT = "C:\ProgramData\Hyveyesh"
$PYTHON_URL = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"

Function Write-Hyveyesh-Art {
    Write-Host @"
    
  _    _  _               _      
 | |  | |(_)             | |     
 | |__| | _ __   __ ___  | |__   
 |  __  || |\ \ / // _ \ | '_ \  
 | |  | || | \ V /|  __/ | | | | 
 |_|  |_||_|  \_/  \___| |_| |_| 
                                 
      UNLEASHING THE SWARM...
"@ -ForegroundColor Cyan
}

# --- 1. Verify Admin ---
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "[!] Admin privileges required. Please run as Administrator." -ForegroundColor Red
    exit
}

Write-Hyveyesh-Art
Write-Host "[+] Initializing Hyveyesh Ecosystem at $HYVEYESH_ROOT" -ForegroundColor Gray

# --- 2. Directory Setup ---
if (-not (Test-Path $HYVEYESH_ROOT)) {
    New-Item -Path $HYVEYESH_ROOT -ItemType Directory | Out-Null
}
$RuntimeDir = Join-Path $HYVEYESH_ROOT "Runtime"
if (-not (Test-Path $RuntimeDir)) {
    New-Item -Path $RuntimeDir -ItemType Directory | Out-Null
}

# --- 3. Portable Python Setup ---
$ZipPath = Join-Path $HYVEYESH_ROOT "python_embed.zip"
if (-not (Test-Path (Join-Path $RuntimeDir "python.exe"))) {
    Write-Host "[+] Downloading Portable Python Environment..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $PYTHON_URL -OutFile $ZipPath
    Write-Host "[+] Extracting Runtime..." -ForegroundColor Yellow
    Expand-Archive -Path $ZipPath -DestinationPath $RuntimeDir -Force
    Remove-Item $ZipPath
    
    # Fix for embedded python: Enable site-packages
    $pthFile = Get-ChildItem -Path $RuntimeDir -Filter "*._pth" | Select-Object -First 1
    if ($pthFile) {
        $content = Get-Content $pthFile.FullName
        $content = $content -replace "#import site", "import site"
        Set-Content -Path $pthFile.FullName -Value $content
    }
} else {
    Write-Host "[+] Portable Python environment already exists." -ForegroundColor Green
}

# --- 4. Launch Stage 2 (Staging) ---
Write-Host "[+] Hyveyesh Bootstrapper Complete. Passing control to Profiler..." -ForegroundColor Green
# In a real scenario, we would copy the Stage 2 scripts into $HYVEYESH_ROOT and launch them.
# For now, we simulate the handover.
Write-Host "`nReady to map the nervous system." -ForegroundColor Cyan
