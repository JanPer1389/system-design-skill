param(
    [Parameter(Mandatory = $true)][string]$SourceRoot,
    [Parameter(Mandatory = $true)][string]$ProfilesRoot
)
# Offline lifecycle only: no prompt, model call, credential copy or live config edits.
$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $SourceRoot).Path
$marketplace = (Get-Content -LiteralPath (Join-Path $sourcePath '.agents/plugins/marketplace.json') -Raw -Encoding UTF8 | ConvertFrom-Json).name
$pluginSelector = "system-design@$marketplace"
$profilesPath = [IO.Path]::GetFullPath($ProfilesRoot)
if (Test-Path -LiteralPath $profilesPath) { throw 'ProfilesRoot must be a new disposable path' }
New-Item -ItemType Directory -Path $profilesPath | Out-Null
$codexBefore = $env:CODEX_HOME
$claudeBefore = $env:CLAUDE_CONFIG_DIR
function Invoke-Checked {
    param([string]$Command, [string[]]$Arguments)
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Command exited $LASTEXITCODE" }
}
try {
    $env:CODEX_HOME = Join-Path $profilesPath 'codex'
    $env:CLAUDE_CONFIG_DIR = Join-Path $profilesPath 'claude'
    New-Item -ItemType Directory -Path $env:CODEX_HOME | Out-Null
    New-Item -ItemType Directory -Path $env:CLAUDE_CONFIG_DIR | Out-Null
    Invoke-Checked 'codex' @('plugin','marketplace','add',$sourcePath,'--json')
    Invoke-Checked 'codex' @('plugin','add',$pluginSelector,'--json')
    Invoke-Checked 'codex' @('plugin','add',$pluginSelector,'--json')
    $codexSkills = @(Get-ChildItem -LiteralPath $env:CODEX_HOME -Recurse -Filter SKILL.md)
    if ($codexSkills.Count -lt 5) { throw 'Codex installed skill payload was not found' }
    $review = $codexSkills | Where-Object { $_.Directory.Name -eq 'system-design-review' } | Select-Object -First 1
    $policies = Join-Path $review.Directory.Parent.FullName 'system-design-enter/references/policies.md'
    if (-not (Test-Path -LiteralPath $policies)) { throw 'Codex shared policies missing after install' }
    Invoke-Checked 'codex' @('plugin','remove',$pluginSelector)
    Invoke-Checked 'codex' @('plugin','marketplace','remove',$marketplace)
    Invoke-Checked 'claude' @('plugin','marketplace','add',$sourcePath)
    Invoke-Checked 'claude' @('plugin','install',$pluginSelector)
    Invoke-Checked 'claude' @('plugin','install',$pluginSelector)
    $claudeSkills = @(Get-ChildItem -LiteralPath $env:CLAUDE_CONFIG_DIR -Recurse -Filter SKILL.md)
    if ($claudeSkills.Count -lt 5) { throw 'Claude installed skill payload was not found' }
    Invoke-Checked 'claude' @('plugin','uninstall',$pluginSelector)
    Invoke-Checked 'claude' @('plugin','marketplace','remove',$marketplace)
    Write-Output 'PASS: isolated Codex and Claude install/reinstall/remove, five skills and policies'
} finally {
    $env:CODEX_HOME = $codexBefore
    $env:CLAUDE_CONFIG_DIR = $claudeBefore
}
