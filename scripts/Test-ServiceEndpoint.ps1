<#
.SYNOPSIS
Tests one explicitly selected TCP endpoint without changing local configuration.
.DESCRIPTION
Use only on authorized systems. TCP success does not verify TLS or application login.
No credentials, firewall changes, route changes or certificate changes are performed.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$ComputerName,

    [Parameter(Mandatory)]
    [ValidateRange(1, 65535)]
    [int]$Port
)

$ErrorActionPreference = 'Stop'
$result = Test-NetConnection -ComputerName $ComputerName -Port $Port `
    -InformationLevel Detailed -WarningAction SilentlyContinue

[pscustomobject]@{
    ComputerName = $result.ComputerName
    RemoteAddress = [string]$result.RemoteAddress
    RemotePort = $result.RemotePort
    TcpReachable = $result.TcpTestSucceeded
    Scope = 'TCP only; TLS and application authentication are not tested'
}

if (-not $result.TcpTestSucceeded) {
    exit 1
}
