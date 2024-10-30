*ENGLISH*

# Organize ROMs Script

A PowerShell script to organize ROM files into system-specific folders based on their file extensions, content, and file names. The script also logs all file movements to allow undoing the operation if needed.

## Features

- Supports a wide range of ROM and image file extensions.
- Determines the system by analyzing file extensions, content using 7-Zip, and file names.
- Moves related files (e.g., `.cue`, `.ccd`, `.mds`, `.sbi`, `.sub`, `.m3u`) along with the main file.
- Logs all file movements to `file_movements.log` for easy reversal.

## Requirements

- **PowerShell**: This script is written in PowerShell and requires it to run.
- **7-Zip**: Used to inspect file contents. Download from [7-zip.org](https://www.7-zip.org/).
- **7-Zip Plugins**: Some file formats require additional plugins. Download from [tc4shell.com](https://www.tc4shell.com/en/7zip/).

## Usage

1. **Download the Script**: Save the script as `organize_roms.ps1`.

2. **Edit the Script**:
   - Set the `$romsPath` variable to the path of your ROMs directory.
   - Set the `$zipPath` variable to the path of your `7z.exe` executable.

3. **Install 7-Zip and Plugins**:
   - Install [7-Zip](https://www.7-zip.org/).
   - Install necessary plugins from [tc4shell.com](https://www.tc4shell.com/en/7zip/).

4. **Run the Script**:
   - Open PowerShell.
   - Navigate to the directory containing the script.
   - Execute the script:
     ```powershell
     .\organize_roms.ps1
     ```
     - If you encounter an execution policy error, you can bypass it:
       ```powershell
       powershell -ExecutionPolicy Bypass -File .\organize_roms.ps1
       ```

5. **Check the Log File**:
   - After execution, a log file named `file_movements.log` will be created in the ROMs directory.
   - This file records all file movements and can be used to undo the changes.

## Undoing the Operation

To reverse the file movements:

1. **Create a Reversal Script**:
   - You can write a script that reads `file_movements.log` and moves each file back to its original location.
   - Example reversal script:
     ```powershell
     $logFilePath = "E:\ROMS2\file_movements.log"
     Get-Content $logFilePath | ForEach-Object {
         $paths = $_ -split ' -> '
         if ($paths.Length -eq 2) {
             $source = $paths[1]
             $destination = $paths[0]
             Move-Item -Path $source -Destination $destination -Force
             Write-Host "Moved '$source' back to '$destination'."
         }
     }
     ```
2. **Run the Reversal Script**:
   - Save the reversal script as `undo_organize_roms.ps1`.
   - Run it in PowerShell to move the files back.

## Notes

- **Backup**: It's recommended to backup your ROMs directory before running the script.
- **Testing**: Test the script on a small set of files to ensure it works as expected.
- **Unsupported Formats**: Some file formats may not be supported by 7-Zip even with plugins. Such files will be moved to the `Others` folder.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

*POLSKI*

# Skrypt do Organizacji ROMów

Skrypt PowerShell do organizacji plików ROM w folderach specyficznych dla systemów na podstawie ich rozszerzeń, zawartości i nazw plików. Skrypt również loguje wszystkie przeniesienia plików, co pozwala na cofnięcie operacji w razie potrzeby.

## Funkcje

- Obsługuje szeroką gamę rozszerzeń plików ROM i obrazów.
- Określa system poprzez analizę rozszerzeń plików, zawartości za pomocą 7-Zip oraz nazw plików.
- Przenosi powiązane pliki (np. `.cue`, `.ccd`, `.mds`, `.sbi`, `.sub`, `.m3u`) wraz z głównym plikiem.
- Loguje wszystkie przeniesienia plików do `file_movements.log`, co umożliwia łatwe cofnięcie zmian.

## Wymagania

- **PowerShell**: Skrypt jest napisany w PowerShell i wymaga go do uruchomienia.
- **7-Zip**: Używany do analizy zawartości plików. Pobierz z [7-zip.org](https://www.7-zip.org/).
- **Wtyczki do 7-Zip**: Niektóre formaty plików wymagają dodatkowych wtyczek. Pobierz z [tc4shell.com](https://www.tc4shell.com/en/7zip/).

## Użycie

1. **Pobierz Skrypt**: Zapisz skrypt jako `organize_roms.ps1`.

2. **Edytuj Skrypt**:
   - Ustaw zmienną `$romsPath` na ścieżkę do Twojego katalogu z ROMami.
   - Ustaw zmienną `$zipPath` na ścieżkę do pliku wykonywalnego `7z.exe`.

3. **Zainstaluj 7-Zip i Wtyczki**:
   - Zainstaluj [7-Zip](https://www.7-zip.org/).
   - Zainstaluj potrzebne wtyczki z [tc4shell.com](https://www.tc4shell.com/en/7zip/).

4. **Uruchom Skrypt**:
   - Otwórz PowerShell.
   - Przejdź do katalogu zawierającego skrypt.
   - Wykonaj skrypt:
     ```powershell
     .\organize_roms.ps1
     ```
     - Jeśli napotkasz błąd związany z polityką wykonywania, możesz go ominąć:
       ```powershell
       powershell -ExecutionPolicy Bypass -File .\organize_roms.ps1
       ```

5. **Sprawdź Plik Logu**:
   - Po wykonaniu, w katalogu z ROMami zostanie utworzony plik logu o nazwie `file_movements.log`.
   - Plik ten rejestruje wszystkie przeniesienia plików i może być użyty do cofnięcia zmian.

## Cofnięcie Operacji

Aby cofnąć przeniesienia plików:

1. **Utwórz Skrypt Odwracający**:
   - Możesz napisać skrypt, który odczyta `file_movements.log` i przeniesie każdy plik z powrotem do pierwotnej lokalizacji.
   - Przykładowy skrypt odwracający:
     ```powershell
     $logFilePath = "E:\ROMS2\file_movements.log"
     Get-Content $logFilePath | ForEach-Object {
         $paths = $_ -split ' -> '
         if ($paths.Length -eq 2) {
             $source = $paths[1]
             $destination = $paths[0]
             Move-Item -Path $source -Destination $destination -Force
             Write-Host "Przeniesiono '$source' z powrotem do '$destination'."
         }
     }
     ```

2. **Uruchom Skrypt Odwracający**:
   - Zapisz skrypt odwracający jako `undo_organize_roms.ps1`.
   - Uruchom go w PowerShell, aby przenieść pliki z powrotem.

## Uwagi

- **Kopia Zapasowa**: Zaleca się wykonanie kopii zapasowej katalogu z ROMami przed uruchomieniem skryptu.
- **Testowanie**: Przetestuj skrypt na niewielkim zestawie plików, aby upewnić się, że działa zgodnie z oczekiwaniami.
- **Nieobsługiwane Format**: Niektóre formaty plików mogą nie być obsługiwane przez 7-Zip nawet z wtyczkami. Takie pliki zostaną przeniesione do folderu `Others`.

## Licencja

Ten projekt jest licencjonowany na podstawie licencji MIT - zobacz plik [LICENSE](LICENSE) w celu uzyskania szczegółów.
