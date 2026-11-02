# Changelog

## [1.2.1] - 2026-11-02

Wersja 1.2.0 nie została wcześniej opublikowana jako wydanie – ta wersja zawiera zmiany z 1.2.0 oraz poprawki poniżej. / Version 1.2.0 was never published as a release; this one includes it plus the fixes below.

### Poprawki / Fixed
- **Segregowanie ROMów:** nazwa folderu docelowego zależy teraz od wybranego zestawu (Batocera / Stock). Wcześniej powstawały foldery `NES`, `SNES`, `PS1` niezależnie od wyboru. / The destination folder now follows the selected set (Batocera / Stock); previously folders like `NES`, `PS1` were always used.
- **Brak nadpisywania plików:** przy kolizji nazw dodawany jest sufiks ` (1)`, ` (2)`… zamiast po cichu nadpisywać istniejący plik. / Existing files are no longer silently overwritten.
- **7-Zip:** wybór „Nie" przy pytaniu o kontynuację faktycznie anuluje operację (wcześniej pliki i tak były przenoszone); wybór „kontynuuj bez 7-Zip" nie powoduje już błędu `TypeError`. 7-Zip jest też wykrywany w `PATH`. / Answering "No" now cancels the operation; "continue without 7-Zip" no longer crashes.
- **Metadane TheGamesDB:** naprawiono `NameError` (nieistniejąca zmienna `game`), przez który metadane nigdy nie trafiały do `gamelist.xml`; dodano timeout, obsługę pustych odpowiedzi i formatowanie daty wydania dla EmulationStation. Klucz API podaje się w zmiennej środowiskowej `THEGAMESDB_API_KEY` (bez klucza metadane są pomijane z jednym komunikatem w logu). / Fixed the `NameError` that prevented any metadata from being written; added a timeout and empty-response handling. The API key is read from `THEGAMESDB_API_KEY`.
- **Zmiana nazw folderów:** istniejący folder docelowy jest scalany zamiast zagnieżdżany; operacja zapisuje `folder_renames.log`, więc „Cofnij zmiany" działa także dla folderów. Cofanie przebiega w odwrotnej kolejności. / Existing target folders are merged instead of nested; renames are logged so "Undo" works for folders too.
- **Mapowanie rozszerzeń:** `.ngc` jest teraz Neo Geo Pocket Color (wcześniej GameCube); dodano `.md`, `.smd`, `.gen`, `.gg`, `.nez`, `.unf`, `.unif`, `.srl`, `.gcm`, `.gcz`, `.xiso`, `.cia`, `.3ds`, które wcześniej trafiały do „Inne". Usunięto rozszerzenia wieloczłonowe, których `os.path.splitext` nie rozpoznaje. / Fixed `.ngc`, added missing extensions.

### Zmiany techniczne / Maintenance
- Wersja 1.2.1 w tytule okna, pomocy i README; README opisuje klucz API i wymaganie Windows. / Version bump, README updates.
- Dodano `.gitignore`; usunięto z repozytorium katalog `build/` (artefakty PyInstaller). / Added `.gitignore`; removed tracked `build/`.

> Plik `dist/aplikacja_romy.exe` w repozytorium pochodzi z wersji 1.2.0 i nie zawiera tych poprawek. Aby go odświeżyć, zbuduj aplikację na Windows (`pyinstaller aplikacja_romy.spec`) i dołącz do wydania. / The committed `dist/aplikacja_romy.exe` is from 1.2.0; rebuild it on Windows.

### Znane ograniczenia / Known limitations
- Rozpoznawanie PS1/PS2 po liście plików w obrazie jest heurystyczne (obrazy PS2 zawierają także pliki `SLUS_`/`SLES_`). / PS1/PS2 detection from image contents is heuristic.
- Pliki niebędące ROM-ami (np. `.txt`, `.jpg`) trafiają do folderu „Inne". / Non-ROM files in the source folder go to "Inne".
