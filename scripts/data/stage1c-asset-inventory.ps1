param(
    [Parameter(Mandatory = $true)][string]$DataRoot,
    [string]$LockPath = "docs/datasets.lock.json",
    [Parameter(Mandatory = $true)][string]$OutputPath,
    [string]$SnapshotDate = "2026-07-22"
)

$ErrorActionPreference = "Stop"
$sourceCatalog = @{
    "audio2tool" = @("hf:RVtech/Audio2Tool", "f1388da9a3189541ab82adac88824a0661670c43")
    "audiocaps-qa" = @("hf:AudioLLMs/audiocaps_qa_test", "LOCAL_REVISION_UNRESOLVED")
    "auditorybench-plusplus" = @("hf:HJOK/AuditoryBenchpp", "LOCAL_REVISION_UNRESOLVED")
    "full-duplex-bench-v3" = @("gdrive:1SO_4MTazWQ_jvCx0dtmpQ-t40bdd07yz", "sha256:37545bd896f81718136598cf5be25d42ea9aa22efcd91f58370938d05d7d672f")
    "ihbench" = @("hf:bosonai/IHBench", "cbd8280ab59bc4a50c48cbe0511a307fba9945cf")
    "omni-deepsearch" = @("hf:Kirito-Lab/Omni-DeepSearch", "f6fafcd1ee9e5d370379b684bee3957c27dc25ac")
    "squtr" = @("hf:SLLMCommunity/SQuTR", "LOCAL_REVISION_UNRESOLVED")
    "voiceagentbench" = @("hf:krutrim-ai-labs/VoiceAgentBench", "5ec6b7fcdaf25a1ffd5f538214d91dcf653c9ea4")
}

$resolvedDataRoot = (Resolve-Path -LiteralPath $DataRoot).Path
$resolvedLock = (Resolve-Path -LiteralPath $LockPath).Path
$lock = Get-Content -LiteralPath $resolvedLock -Raw | ConvertFrom-Json
$lockedByPath = @{}
$baselineEntries = @()

foreach ($kindSpec in @(@("datasets", "dataset"), @("models", "model"))) {
    $collection = $kindSpec[0]
    $kind = $kindSpec[1]
    foreach ($row in $lock.$collection) {
        $relative = [string]$row.local_subdir -replace "\\", "/"
        $lockedByPath[$relative] = $true
        $path = Join-Path $resolvedDataRoot ($relative -replace "/", [IO.Path]::DirectorySeparatorChar)
        if (-not (Test-Path -LiteralPath $path -PathType Container)) { continue }
        $sourceIdentity = if ($row.source.id) { $row.source.id } elseif ($row.source.hf_id) { $row.source.hf_id } else { "LOCK_SOURCE_UNRECORDED" }
        $revision = if ($row.revision) { $row.revision } else { "LOCK_REVISION_UNRECORDED" }
        $baselineEntries += [ordered]@{
            kind = $kind
            name = Split-Path -Leaf $path
            local_path = "`${SPEECHRL_DATA_DIR}/$relative"
            files = $row.files
            bytes = $row.size_bytes
            source_identity = [string]$sourceIdentity
            revision_or_fingerprint = [string]$revision
            source_status = "FROZEN_LOCK_RECORD"
            layer_status = "LOCAL_BASELINE_LOCKED"
        }
    }
}

$candidateEntries = @()
foreach ($kindSpec in @(@("datasets", "dataset"), @("models", "model"))) {
    $collection = $kindSpec[0]
    $kind = $kindSpec[1]
    $parent = Join-Path $resolvedDataRoot $collection
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) { continue }
    foreach ($directory in Get-ChildItem -LiteralPath $parent -Directory | Sort-Object Name) {
        $relative = "$collection/$($directory.Name)"
        if ($lockedByPath.ContainsKey($relative)) { continue }
        $measure = Get-ChildItem -LiteralPath $directory.FullName -File -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum
        if ($sourceCatalog.ContainsKey($directory.Name)) {
            $sourceIdentity = $sourceCatalog[$directory.Name][0]
            $revision = $sourceCatalog[$directory.Name][1]
            $sourceStatus = if ($revision -match "UNRESOLVED") { "SOURCE_ID_KNOWN_REVISION_UNRESOLVED" } else { "EXACT_CATALOG_ENTRY" }
        } else {
            $metadataPath = Join-Path $directory.FullName ".hfd\repo_metadata.json"
            if (Test-Path -LiteralPath $metadataPath -PathType Leaf) {
                try {
                    $metadata = Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json
                    $sourceIdentity = "hf:$($metadata.id)"
                    $revision = if ($metadata.sha) { [string]$metadata.sha } else { "LOCAL_REVISION_UNRESOLVED" }
                    $sourceStatus = "LOCAL_METADATA_OBSERVED"
                } catch {
                    $sourceIdentity = "UNRESOLVED_LOCAL_SOURCE"
                    $revision = "UNRESOLVED_LOCAL_REVISION"
                    $sourceStatus = "UNRESOLVED_LOCAL_PROVENANCE"
                }
            } else {
                $sourceIdentity = "UNRESOLVED_LOCAL_SOURCE"
                $revision = "UNRESOLVED_LOCAL_REVISION"
                $sourceStatus = "UNRESOLVED_LOCAL_PROVENANCE"
            }
        }
        $candidateEntries += [ordered]@{
            kind = $kind
            name = $directory.Name
            local_path = "`${SPEECHRL_DATA_DIR}/$relative"
            files = [int64]$measure.Count
            bytes = [int64]$(if ($null -eq $measure.Sum) { 0 } else { $measure.Sum })
            source_identity = $sourceIdentity
            revision_or_fingerprint = $revision
            source_status = $sourceStatus
            layer_status = "LOCAL_CANDIDATE_UNFROZEN"
        }
    }
}

$missingLockedPaths = @()
foreach ($relative in $lockedByPath.Keys | Sort-Object) {
    $path = Join-Path $resolvedDataRoot ($relative -replace "/", [IO.Path]::DirectorySeparatorChar)
    if (-not (Test-Path -LiteralPath $path -PathType Container)) { $missingLockedPaths += $relative }
}
$auxiliaryEntries = @()
foreach ($name in @("survey-fulltext", "repos", "logs", "mlruns", "outputs")) {
    $auxiliaryEntries += [ordered]@{
        local_path = "`${SPEECHRL_DATA_DIR}/$name"
        present = Test-Path -LiteralPath (Join-Path $resolvedDataRoot $name)
    }
}

$document = [ordered]@{
    schema = "speechrl-data-layered-inventory-v1"
    data_root = "`${SPEECHRL_DATA_DIR}"
    snapshot_date = $SnapshotDate
    claim_limit = "Directory presence, file counts and byte totals only. FROZEN_BASELINE semantics come from docs/datasets.lock.json; no whole-disk content hash was recomputed."
    layers = @(
        [ordered]@{
            layer_id = "FROZEN_BASELINE"
            manifest = "docs/datasets.lock.json"
            locked_entries = $lockedByPath.Count
            observed_entries = $baselineEntries.Count
            missing_locked_paths = $missingLockedPaths
            entries = $baselineEntries
        },
        [ordered]@{
            layer_id = "LOCAL_CANDIDATE_UNFROZEN"
            observed_entries = $candidateEntries.Count
            entries = $candidateEntries
        },
        [ordered]@{
            layer_id = "SURVEY_AND_REPRO_AUXILIARY"
            counting_rule = "Kept outside dataset/model totals; presence only in this inventory."
            entries = $auxiliaryEntries
        }
    )
}

$outputParent = Split-Path -Parent $OutputPath
if ($outputParent) { New-Item -ItemType Directory -Force -Path $outputParent | Out-Null }
$json = $document | ConvertTo-Json -Depth 12
[IO.File]::WriteAllText((Join-Path (Get-Location) $OutputPath), $json + [Environment]::NewLine, [Text.UTF8Encoding]::new($false))
Write-Output "FROZEN_BASELINE: $($baselineEntries.Count) entries"
Write-Output "LOCAL_CANDIDATE_UNFROZEN: $($candidateEntries.Count) entries"
Write-Output "SURVEY_AND_REPRO_AUXILIARY: $($auxiliaryEntries.Count) entries"
if ($missingLockedPaths.Count -gt 0) { exit 1 }
