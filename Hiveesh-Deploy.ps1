<#
.SYNOPSIS
    Hiveesh Swarm Deployment Master Script.
    Performs discovery, diagnosis, OS configuration, and runtime deployment across institutional nodes.

.DESCRIPTION
    1. Scans subnet for active nodes.
    2. Performs hardware diagnostics via WMI.
    3. Configures Windows Firewall and Registry for performance and compatibility.
    4. Pushes the portable Hiveesh runtime payload via WinRM.

.PARAMETER Subnet
    The subnet prefix to scan (e.g., "192.168.1"). Defaults to the current subnet.

.PARAMETER PayloadPath
    Path to the Hiveesh runtime folder on the admin node.

.EXAMPLE
    .\Hiveesh-Deploy.ps1 -Subnet "192.168.0" -PayloadPath "C:\HiveeshStaging"
#>

Param(
    [Parameter(Mandatory=$false)]
    [string]$Subnet,

    [Parameter(Mandatory=$false)]
    [string]$PayloadPath = "$PSScriptRoot\Runtime"
)

# --- Configuration & Helpers ---
$VerbosePreference = "Continue"
$ErrorActionPreference = "Stop"

Function Write-Header {
    Param([string]$Text)
    Write-Host "`n=== $Text ===" -ForegroundColor Cyan
}

Function Get-LocalSubnet {
    $ip = Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*", "Wi-Fi*" | Select-Object -First 1
    if ($ip) {
        return $ip.IPAddress.Substring(0, $ip.IPAddress.LastIndexOf('.'))
    }
    return "192.168.1"
}

if (-not $Subnet) {
    $Subnet = Get-LocalSubnet
    Write-Host "No subnet provided. Defaulting to: $Subnet.*" -ForegroundColor Yellow
}

# --- 1. Subnet Discovery ---
Write-Header "Scanning Subnet: $Subnet.0/24"
$ActiveNodes = @()
$PingJobs = @()

# Fast Ping Sweep
1..254 | ForEach-Object {
    $IP = "$Subnet.$_"
    $PingJobs += Test-Connection -ComputerName $IP -Count 1 -AsJob -Quiet
}

Write-Host "Ping sweep started. Waiting for responses..." -ForegroundColor Gray
$Results = Wait-Job $PingJobs | Receive-Job
foreach ($Job in $PingJobs) {
    if ($Job.Output -and $Job.Output[0]) {
        $ActiveNodes += $Job.Location
    }
}
Remove-Job $PingJobs

Write-Host "Found $($ActiveNodes.Count) active nodes." -ForegroundColor Green
if ($ActiveNodes.Count -eq 0) {
    Write-Host "No nodes found. Exiting." -ForegroundColor Red
    return
}

# --- 2. Deployment & Config (Parallel via Jobs) ---
Write-Header "Starting Remote Deployment"

$DeploymentJobs = @()
foreach ($Node in $ActiveNodes) {
    $ScriptBlock = {
        Param($Node)
        try {
            # --- Hardware Diagnostic ---
            $CPU = Get-WmiObject Win32_Processor -ComputerName $Node | Select-Object -First 1
            $RAM = Get-WmiObject Win32_ComputerSystem -ComputerName $Node | Select-Object TotalPhysicalMemory
            $RAM_GB = [Math]::Round($RAM.TotalPhysicalMemory / 1GB, 2)
            
            # --- Registry: LongPathsEnabled ---
            Invoke-Command -ComputerName $Node -ScriptBlock {
                Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -ErrorAction SilentlyContinue
            } -ErrorAction Stop

            # --- Firewall: Ports 8000-8100 ---
            Invoke-Command -ComputerName $Node -ScriptBlock {
                if (-not (Get-NetFirewallRule -DisplayName "Hiveesh Swarm" -ErrorAction SilentlyContinue)) {
                    New-NetFirewallRule -DisplayName "Hiveesh Swarm" -Direction Inbound -LocalPort 8000-8100 -Protocol TCP -Action Allow
                }
            } -ErrorAction Stop

            # --- Directory Setup ---
            Invoke-Command -ComputerName $Node -ScriptBlock {
                if (-not (Test-Path "C:\Hiveesh")) { New-Item -Path "C:\Hiveesh" -ItemType Directory }
            }

            return [PSCustomObject]@{
                Node    = $Node
                CPU     = $CPU.Name.Trim()
                Cores   = $CPU.NumberOfCores
                RAM_GB  = $RAM_GB
                Status  = "Configured & Ready"
            }
        }
        catch {
            return [PSCustomObject]@{
                Node   = $Node
                Status = "Failed: $($_.Exception.Message)"
            }
        }
    }
    
    $DeploymentJobs += Start-Job -ScriptBlock $ScriptBlock -ArgumentList $Node
}

$FinalResults = Wait-Job $DeploymentJobs | Receive-Job
Remove-Job $DeploymentJobs

# --- Summary Table ---
Write-Header "Hiveesh Swarm Deployment Summary"
$FinalResults | Format-Table -AutoSize

# Note: Payload push (Copy-Item) is usually better done outside jobs or via BITS if large.
# For this scaffold, we report health. Actual runtime sync will be Task 2/3.
