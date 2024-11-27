
# Organize-ROMs-Script

**Wersja:** 1.0.0

## Spis treści

- [Opis](#opis)
- [Funkcjonalności](#funkcjonalności)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Użycie](#użycie)
- [Licencja](#licencja)
- [English Version](#english-version)

## Opis

Aplikacja służy do zarządzania plikami ROM oraz folderami dla emulatorów. Pozwala na:

- Zmianę nazw folderów w zależności od wybranego systemu emulacji.
- Segregowanie plików ROM do odpowiednich folderów na podstawie rozszerzeń i zawartości plików.
- Cofanie wprowadzonych zmian na podstawie pliku log.

## Funkcjonalności

- **Zmiana nazw folderów**: Automatyczne dostosowanie nazw folderów do wymagań wybranego systemu emulacji.
- **Segregowanie ROMów**: Przenoszenie plików ROM do odpowiednich folderów na podstawie ich typu.
- **Cofanie zmian**: Możliwość cofnięcia wprowadzonych zmian za pomocą pliku log.
- **Interfejs graficzny**: Przyjazny dla użytkownika interfejs oparty na bibliotece `tkinter`.
- **Integracja z 7-Zip**: Wykorzystanie 7-Zip do analizowania zawartości skompresowanych plików.

## Wymagania

- Python 3.x
- Biblioteka `tkinter` (standardowo dostępna w instalacji Pythona)
- Zainstalowany 7-Zip (opcjonalnie, do pełnej funkcjonalności)

## Instalacja

1. **Sklonuj repozytorium**:

   ```bash
   git clone https://github.com/husk007/Organize-ROMs-Script.git
   ```

2. **Przejdź do katalogu projektu**:

   ```bash
   cd Organize-ROMs-Script
   ```

3. **Zainstaluj wymagane biblioteki**:

   Jeśli używasz `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   Jeśli używasz `pip3`:

   ```bash
   pip3 install -r requirements.txt
   ```

## Użycie

1. **Uruchom aplikację**:

   ```bash
   python aplikacja_romy.py
   ```

   Lub jeśli używasz `python3`:

   ```bash
   python3 aplikacja_romy.py
   ```

2. **Wybierz system emulacji**.

3. **Wskaż ścieżki źródłową i docelową**.

4. **Użyj przycisków akcji** do wykonania odpowiednich operacji.

5. **Aby cofnąć zmiany**, użyj przycisku **"Cofnij zmiany w oparciu o LOG"** i wybierz odpowiedni plik log.

## Licencja

Projekt jest licencjonowany na warunkach licencji MIT. Zobacz plik [LICENSE](LICENSE) po więcej informacji.

---

## English Version

### Table of Contents

- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

### Description

The application is designed to manage ROM files and folders for emulators. It allows you to:

- Change folder names based on the selected emulation system.
- Organize ROM files into appropriate folders based on file extensions and content.
- Undo changes made, based on a log file.

### Features

- **Folder Name Changing**: Automatically adjust folder names to meet the requirements of the selected emulation system.
- **ROM Organization**: Move ROM files to appropriate folders based on their type.
- **Undo Changes**: Ability to revert changes using a log file.
- **Graphical User Interface**: User-friendly interface based on the `tkinter` library.
- **7-Zip Integration**: Use 7-Zip to analyze the content of compressed files.

### Requirements

- Python 3.x
- `tkinter` library (usually included with Python installation)
- 7-Zip installed (optional, for full functionality)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/husk007/Organize-ROMs-Script.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd Organize-ROMs-Script
   ```

3. **Install the required libraries**:

   Using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   Using `pip3`:

   ```bash
   pip3 install -r requirements.txt
   ```

### Usage

1. **Run the application**:

   ```bash
   python aplikacja_romy.py
   ```

   Or if you are using `python3`:

   ```bash
   python3 aplikacja_romy.py
   ```

2. **Select the emulation system**.

3. **Specify the source and destination paths**.

4. **Use the action buttons** to perform the desired operations.

5. **To undo changes**, use the **"Undo changes based on LOG"** button and select the appropriate log file.

### License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for more information.
```
