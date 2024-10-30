# Path to the ROMs directory
$romsPath = "E:\ROMS2"

# Path to 7-Zip
$zipPath = "C:\Program Files\7-Zip\7z.exe"

# Log file path
$logFilePath = Join-Path $romsPath "file_movements.log"

# Change to the ROMs directory
Set-Location $romsPath

# Get all files in the directory
$files = Get-ChildItem -File

# Mapping of systems to folder names
$systemMapping = @{
    "Amiga" = "AMIGA"
    "Amstrad CPC" = "CPC"
    "Arcade" = "ARCADE"
    "Atari 2600" = "ATARI"
    "Atari 5200" = "ATARI5200"
    "Atari 7800" = "ATARI7800"
    "Atari Lynx" = "LYNX"
    "Bandai Sufami Turbo" = "SUFAMI"
    "Bandai WonderSwan & Color" = "WS"
    "Commodore 64" = "COMMODORE64"
    "Capcom Play System 1" = "CPS1"
    "Capcom Play System 2" = "CPS2"
    "Capcom Play System 3" = "CPS3"
    "ColecoVision" = "COLECO"
    "Fairchild Channel F" = "FAIRCHILD"
    "Famicom Disk System" = "FDS"
    "Game & Watch" = "G&W"
    "GCE Vectrex" = "VECTREX"
    "Magnavox Odyssey 2" = "ODYSSEY2"
    "Mattel Intellivision" = "INTELLIVISION"
    "Mega Duck" = "MEGADUCK"
    "MS-DOS" = "DOS"
    "MSX - MSX2" = "MSX"
    "NEC SuperGrafx" = "SGFX"
    "NEC TurboGrafx CD" = "PCECD"
    "NEC TurboGrafx-16" = "PCE"
    "Nintendo 64" = "N64"
    "Nintendo 64DD" = "64DD"
    "Nintendo DS" = "NDS"
    "Nintendo DSi" = "DSi"
    "Nintendo Entertainment System" = "NES"
    "Nintendo Game Boy" = "GB"
    "Nintendo Game Boy Advance" = "GBA"
    "Nintendo Game Boy Color" = "GBC"
    "Nintendo Pokemini" = "Pokemini"
    "Nintendo Satellaview" = "SATELLAVIEW"
    "Nintendo Super Game Boy" = "SGB"
    "Nintendo Super Nintendo" = "SNES"
    "Nintendo Virtual Boy" = "VB"
    "Nintendo GameCube" = "GAMECUBE"
    "Nintendo Wii" = "WII"
    "Nintendo Wii U" = "WIIU"
    "Nintendo Switch" = "SWITCH"
    "Nintendo 3DS" = "3DS"
    "PICO-8" = "PICO8"
    "Ports collection" = "PORTS"
    "ScummVM" = "SCUMMVM"
    "Sega 32X" = "SEGA32X"
    "Sega CD" = "SEGACD"
    "Sega Dreamcast" = "DREAMCAST"
    "Sega Game Gear" = "GAMEGEAR"
    "Sega Genesis" = "GENESIS"
    "Sega Master System" = "MASTERSYSTEM"
    "Sega SG-1000" = "SG1000"
    "Sinclair ZX Spectrum" = "ZXSPECTRUM"
    "SNK NeoGeo" = "NEOGEO"
    "SNK NeoGeo CD" = "NEOGEOCD"
    "SNK NeoGeo Pocket & Color" = "NGP"
    "Sony PlayStation" = "PS1"
    "Sony PlayStation 2" = "PS2"
    "Sony PlayStation 3" = "PS3"
    "Sony PlayStation 4" = "PS4"
    "Sony PlayStation Portable" = "PSP"
    "Sony PS Vita" = "PSVITA"
    "Microsoft Xbox" = "XBOX"
    "Microsoft Xbox 360" = "XBOX360"
    "Microsoft Xbox One" = "XBOXONE"
    "TIC-80" = "TIC80"
    "Commodore VIC-20" = "VIC20"
    "Watara Supervision" = "SUPERVISION"
}

# List of files moved, for logging purposes
$movedFiles = @()

foreach ($file in $files) {
    # Initialize variables
    $system = $null
    $fileNameLower = $file.Name.ToLower()
    $extension = $file.Extension.ToLower()
    $fileSize = $file.Length

    # Lists of image and ROM extensions
    $imageExtensions = @(".iso", ".img", ".bin", ".mdf", ".chd", ".nrg", ".cdi", ".gdi", ".ecm", ".cso", ".gcz", ".rvz", ".wbfs", ".nsp", ".xci", ".dsk", ".pbp", ".elf", ".dol", ".isz", ".rar", ".7z", ".zip", ".gzip", ".tar", ".tar.gz", ".tar.bz2", ".001", ".part1", ".r01")
    $romExtensions = @(".nes", ".nez", ".unf", ".unif", ".smc", ".sfc", ".md", ".smd", ".gen", ".gg", ".z64", ".v64", ".n64", ".gb", ".gbc", ".gba", ".srl", ".gcm", ".gcz", ".xiso", ".nds", ".dsi", ".ids", ".cia", ".3ds", ".ngp", ".ngc", ".pce", ".vb", ".ws", ".wsc", ".adf", ".adz", ".dms", ".ipf", ".rp9", ".cdc", ".tzx", ".cas", ".fds", ".ecm", ".wav", ".tap", ".ndd", ".xbe", ".xex")

    # Determine system based on extension
    if ($extension -in $romExtensions) {
        # Map extension to system
        switch ($extension) {
            ".nes" { $system = "NES" }
            ".smc" { $system = "SNES" }
            ".sfc" { $system = "SNES" }
            ".gb"  { $system = "GB" }
            ".gbc" { $system = "GBC" }
            ".gba" { $system = "GBA" }
            ".nds" { $system = "NDS" }
            ".dsi" { $system = "DSi" }
            ".n64" { $system = "N64" }
            ".z64" { $system = "N64" }
            ".v64" { $system = "N64" }
            ".ngp" { $system = "NGP" }
            ".ngc" { $system = "NGP" }
            ".pce" { $system = "PCE" }
            ".vb"  { $system = "VB" }
            ".ws"  { $system = "WS" }
            ".wsc" { $system = "WS" }
            ".adf" { $system = "AMIGA" }
            ".adz" { $system = "AMIGA" }
            ".dms" { $system = "AMIGA" }
            ".ipf" { $system = "AMIGA" }
            ".rp9" { $system = "AMIGA" }
            ".cdc" { $system = "CPC" }
            ".tzx" { $system = "ZXSPECTRUM" }
            ".cas" { $system = "NEC PC-6000" }
            ".fds" { $system = "FDS" }
            ".ecm" { $system = "PS1" }
            ".wav" { $system = "TAPE" }
            ".tap" { $system = "TAPE" }
            ".ndd" { $system = "64DD" }
            ".xbe" { $system = "XBOX" }
            ".xex" { $system = "XBOX360" }
            default { $system = "Others" }
        }
    } elseif ($extension -in $imageExtensions) {
        # Image files for further analysis
        $system = $null
    } elseif ($extension -in @(".cue", ".ccd", ".mds", ".sbi", ".sub", ".m3u")) {
        # Related files will be moved with the main files
        continue
    } else {
        $system = "Others"
    }

    # If system is not determined, try further analysis
    if (-not $system) {
        # Analyze file content using 7-Zip for image files
        if ($extension -in $imageExtensions) {
            try {
                # Check if 7-Zip supports the format
                $formatSupported = & "$zipPath" l "$($file.FullName)" 2>&1
                if ($formatSupported -match "unsupported") {
                    Write-Host "File format '$($file.Name)' is not supported by 7-Zip. You may need to install plugins."
                    $system = "Others"
                } else {
                    $content = & "$zipPath" l "$($file.FullName)"
                    if ($content -match "SLUS_|SLES_|SCUS_|SCEE_|SCPS_") {
                        $system = "PS1"
                    } elseif ($content -match "PSP_GAME") {
                        $system = "PSP"
                    } elseif ($content -match "SYSTEM.CNF") {
                        $system = "PS2"
                    } elseif ($content -match "PS3_GAME") {
                        $system = "PS3"
                    } elseif ($content -match "1ST_READ.BIN") {
                        $system = "DREAMCAST"
                    } elseif ($content -match "GAME.DOL") {
                        $system = "GAMECUBE"
                    } elseif ($content -match "SYSCONF") {
                        $system = "WII"
                    } elseif ($content -match "WIIU") {
                        $system = "WIIU"
                    } elseif ($content -match "Switch") {
                        $system = "SWITCH"
                    } elseif ($content -match "Xbox360") {
                        $system = "XBOX360"
                    } elseif ($content -match "icon.sys") {
                        $system = "PSVITA"
                    } else {
                        # If not found, try based on file name
                        $system = "Others"
                    }
                }
            } catch {
                Write-Host "Failed to process file '$($file.Name)' with 7-Zip."
                $system = "Others"
            }
        } else {
            # Attempt to determine system based on file name
            foreach ($key in $systemMapping.Keys) {
                if ($fileNameLower -match $key.ToLower()) {
                    $system = $systemMapping[$key]
                    break
                }
            }

            if (-not $system) {
                $system = "Others"
            }
        }
    }

    # Create system directory if it doesn't exist
    $targetDirectory = Join-Path $romsPath $system
    if (!(Test-Path $targetDirectory)) {
        New-Item -ItemType Directory -Path $targetDirectory | Out-Null
    }

    # Find related files (e.g., .cue, .ccd, .mds, .sbi, .sub, .m3u)
    $fileNameWithoutExtension = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $relatedExtensions = @(".cue", ".ccd", ".mds", ".sbi", ".sub", ".m3u")
    $relatedFiles = Get-ChildItem -Path $file.DirectoryName -Filter "$fileNameWithoutExtension.*" | Where-Object { $_.Extension -in $relatedExtensions }

    # Move main file
    $originalPath = $file.FullName
    $destinationPath = Join-Path $targetDirectory $file.Name
    Move-Item -Path $originalPath -Destination $destinationPath -Force

    # Log the movement
    $movedFiles += @{ OriginalPath = $originalPath; DestinationPath = $destinationPath }

    # Move related files
    foreach ($relatedFile in $relatedFiles) {
        $originalRelatedPath = $relatedFile.FullName
        $destinationRelatedPath = Join-Path $targetDirectory $relatedFile.Name
        Move-Item -Path $originalRelatedPath -Destination $destinationRelatedPath -Force

        # Log the movement
        $movedFiles += @{ OriginalPath = $originalRelatedPath; DestinationPath = $destinationRelatedPath }
    }

    Write-Host "Moved '$($file.Name)' and related files to folder '$system'."

    # Add file name to moved files list
    $movedFiles += $fileNameWithoutExtension
}

# Write movements to log file
$movedFiles | ForEach-Object {
    "$($_.OriginalPath) -> $($_.DestinationPath)" | Out-File -FilePath $logFilePath -Append
}

Write-Host "All files have been organized."
Write-Host "A log of file movements has been saved to '$logFilePath'."

# Information about 7-Zip plugins
Write-Host "`nNOTE: Some file formats may require additional 7-Zip plugins."
Write-Host "You can download them from: https://www.tc4shell.com/en/7zip/"
