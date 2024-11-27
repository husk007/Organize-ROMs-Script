import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import xml.etree.ElementTree as ET

# Mappings of folder names based on the system
folder_mappings = {
    # Wklej tutaj pełny słownik folder_mappings z Twojego projektu
    # Przykład:
    'NES': {'Batocera': 'nes', 'Stock': 'NES'},
    'SNES': {'Batocera': 'snes', 'Stock': 'SNES'},
    # Dodaj pozostałe mapowania...
}

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do zarządzania ROMami - Wersja 1.1.0")
        self.geometry("800x750")
        self.seven_zip_path = None

        # Pobranie ścieżki bazowej
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        # Ścieżka do pliku ikony
        icon_path = os.path.join(base_path, 'icon.ico')
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # Menu górne
        self.create_menu()

        self.system_var = tk.StringVar(value="Batocera")

        # Radio buttons do wyboru systemu
        self.create_radio_buttons()

        # Pola do wyboru ścieżek
        self.create_path_entries()

        # Przyciski akcji
        self.create_action_buttons()

        # Pole tekstowe do logowania
        self.create_log_text()

    def create_menu(self):
        menubar = tk.Menu(self)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Pomoc", command=self.show_help)
        helpmenu.add_command(label="GitHub", command=self.open_github)
        menubar.add_cascade(label="Pomoc", menu=helpmenu)
        self.config(menu=menubar)

    def show_help(self):
        help_text = (
            "Aplikacja do zarządzania ROMami - Wersja 1.1.0\n\n"
            "Funkcje:\n"
            "- Zmiana nazw folderów w zależności od wybranego systemu.\n"
            "- Segregowanie plików ROM do odpowiednich folderów na podstawie rozszerzeń plików i zawartości.\n"
            "- Generowanie pliku gamelist.xml dla gier.\n"
            "- Cofanie zmian na podstawie pliku log.\n\n"
            "Instrukcja obsługi:\n"
            "1. Wybierz system za pomocą odpowiednich przycisków radiowych.\n"
            "2. Wskaż ścieżkę źródłową i docelową.\n"
            "3. Użyj przycisków akcji do wykonania odpowiednich operacji.\n"
            "4. W przypadku korzystania z funkcji segregowania ROMów lub generowania gamelist.xml, upewnij się, że masz zainstalowany 7-Zip oraz odpowiednie pluginy.\n\n"
            "Więcej informacji znajdziesz w pliku README.md lub na stronie GitHub."
        )
        messagebox.showinfo("Pomoc", help_text)

    def open_github(self):
        webbrowser.open("https://github.com/husk007/Organize-ROMs-Script/")

    def create_radio_buttons(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Wybierz system:").pack(anchor='w')

        systems = [
            ("Batocera, KNULI, ROCKNIX (JELOS), EmuELEC", "Batocera"),
            ("Stock RG.., GarlicOS, Onion, MinUI", "Stock")
        ]

        for text, value in systems:
            tk.Radiobutton(frame, text=text, variable=self.system_var, value=value).pack(anchor='w')

    def create_path_entries(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Ścieżka źródłowa:").pack(anchor='w')
        self.source_entry = tk.Entry(frame, width=80)
        self.source_entry.pack(side='left')
        tk.Button(frame, text="Przeglądaj", command=self.browse_source).pack(side='left')

        frame2 = tk.Frame(self)
        frame2.pack(pady=10)

        tk.Label(frame2, text="Ścieżka docelowa:").pack(anchor='w')
        self.dest_entry = tk.Entry(frame2, width=80)
        self.dest_entry.pack(side='left')
        tk.Button(frame2, text="Przeglądaj", command=self.browse_dest).pack(side='left')

    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, path)

    def browse_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, path)

    def create_action_buttons(self):
        frame = tk.Frame(self)
        frame.pack(pady=20)

        tk.Button(frame, text="Zmień nazwy folderów", command=self.change_folder_names).pack(side='left', padx=10)
        tk.Button(frame, text="Segreguj ROMy", command=self.organize_roms).pack(side='left', padx=10)
        tk.Button(frame, text="Generuj gamelist.xml", command=self.generate_gamelist).pack(side='left', padx=10)
        tk.Button(frame, text="Cofnij zmiany w oparciu o LOG", command=self.undo_changes).pack(side='left', padx=10)

    def create_log_text(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Log operacji:").pack(anchor='w')
        self.log_text = tk.Text(frame, width=100, height=10)
        self.log_text.pack()

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def check_seven_zip(self):
        default_path = r"C:\Program Files\7-Zip\7z.exe"
        if os.path.isfile(default_path):
            self.seven_zip_path = default_path
        else:
            messagebox.showwarning("7-Zip", "Nie znaleziono 7-Zip w domyślnej lokalizacji.")
            path = filedialog.askopenfilename(title="Wskaż plik 7z.exe", filetypes=[("7z.exe", "7z.exe")])
            if path and os.path.isfile(path):
                self.seven_zip_path = path
            else:
                proceed = messagebox.askyesno("Kontynuować bez 7-Zip?", "Nie znaleziono 7-Zip. Czy chcesz kontynuować bez 7-Zip?\nPliki obrazów mogą zostać przeniesione do folderu 'Inne'.")
                if not proceed:
                    return False
        # Sprawdzenie obecności pluginu Iso7z
        formats_folder = os.path.join(os.path.dirname(self.seven_zip_path), "Formats")
        if not os.path.isdir(formats_folder):
            messagebox.showwarning("Plugin Iso7z", f"Nie znaleziono folderu 'Formats' w {formats_folder}.\nZainstaluj plugin Iso7z z https://www.tc4shell.com/en/7zip/iso7z/")
            proceed = messagebox.askyesno("Kontynuować bez pluginu?", "Czy chcesz kontynuować bez pluginu Iso7z?\nPliki obrazów mogą zostać przeniesione do folderu 'Inne'.")
            if not proceed:
                return False
        else:
            dll_found = any(fname in os.listdir(formats_folder) for fname in ["Iso7z.64.dll", "Iso7z.32.dll"])
            if not dll_found:
                messagebox.showwarning("Plugin Iso7z", f"Nie znaleziono pliku 'Iso7z.64.dll' lub 'Iso7z.32.dll' w {formats_folder}.\nZainstaluj plugin Iso7z z https://www.tc4shell.com/en/7zip/iso7z/")
                proceed = messagebox.askyesno("Kontynuować bez pluginu?", "Czy chcesz kontynuować bez pluginu Iso7z?\nPliki obrazów mogą zostać przeniesione do folderu 'Inne'.")
                if not proceed:
                    return False
        return True

    def change_folder_names(self):
        source = self.source_entry.get()
        dest = self.dest_entry.get()
        system = self.system_var.get()

        if not source or not dest:
            messagebox.showerror("Błąd", "Proszę podać ścieżki źródłową i docelową.")
            return

        if not os.path.isdir(source) or not os.path.isdir(dest):
            messagebox.showerror("Błąd", "Podane ścieżki nie są prawidłowymi folderami.")
            return

        for folder_name in os.listdir(source):
            source_folder = os.path.join(source, folder_name)
            if os.path.isdir(source_folder):
                mapping = folder_mappings.get(folder_name)
                if mapping:
                    new_name = mapping.get(system, folder_name)
                else:
                    new_name = folder_name  # Jeśli brak w mappingu, pozostaje bez zmian

                dest_folder = os.path.join(dest, new_name)
                shutil.move(source_folder, dest_folder)
                self.log(f"Przeniesiono {source_folder} do {dest_folder}")

        messagebox.showinfo("Sukces", "Nazwy folderów zostały zmienione.")

    def organize_roms(self):
        source = self.source_entry.get()
        dest = self.dest_entry.get()
        system = self.system_var.get()

        if not source or not dest:
            messagebox.showerror("Błąd", "Proszę podać ścieżki źródłową i docelową.")
            return

        if not os.path.isdir(source) or not os.path.isdir(dest):
            messagebox.showerror("Błąd", "Podane ścieżki nie są prawidłowymi folderami.")
            return

        # Sprawdzenie 7-Zip
        seven_zip_available = self.check_seven_zip()

        # Listy rozszerzeń
        image_extensions = [".iso", ".img", ".bin", ".mdf", ".chd", ".nrg", ".cdi", ".gdi", ".ecm", ".cso", ".gcz", ".rvz", ".wbfs", ".nsp", ".xci", ".dsk", ".pbp", ".elf", ".dol", ".isz", ".rar", ".7z", ".zip", ".gzip", ".tar", ".tar.gz", ".tar.bz2", ".001", ".part1", ".r01"]
        rom_extensions = [".nes", ".nez", ".unf", ".unif", ".smc", ".sfc", ".md", ".smd", ".gen", ".gg", ".z64", ".v64", ".n64", ".gb", ".gbc", ".gba", ".srl", ".gcm", ".gcz", ".xiso", ".nds", ".dsi", ".ids", ".cia", ".3ds", ".ngp", ".ngc", ".pce", ".vb", ".ws", ".wsc", ".adf", ".adz", ".dms", ".ipf", ".rp9", ".cdc", ".tzx", ".cas", ".fds", ".ecm", ".wav", ".tap", ".ndd", ".xbe", ".xex"]
        related_extensions = [".cue", ".ccd", ".mds", ".sbi", ".sub", ".m3u"]

        # Mapping rozszerzeń do systemów
        extension_mapping = {
            ".nes": "NES",
            ".smc": "SNES",
            ".sfc": "SNES",
            ".gb": "GB",
            ".gbc": "GBC",
            ".gba": "GBA",
            ".nds": "NDS",
            ".dsi": "NDS",
            ".n64": "N64",
            ".z64": "N64",
            ".v64": "N64",
            ".ngp": "NEOGEOPOCKET",
            ".ngc": "GAMECUBE",
            ".pce": "PCENGINE",
            ".vb": "VIRTUALBOY",
            ".ws": "WONDERSWAN",
            ".wsc": "WONDERSWAN_COLOR",
            ".adf": "AMIGA",
            ".adz": "AMIGA",
            ".dms": "AMIGA",
            ".ipf": "AMIGA",
            ".rp9": "AMIGA",
            ".cdc": "CPC",
            ".tzx": "ZXSPECTRUM",
            ".cas": "NEC PC-6000",
            ".fds": "FDS",
            ".ecm": "PS1",
            ".wav": "TAPE",
            ".tap": "TAPE",
            ".ndd": "64DD",
            ".xbe": "XBOX",
            ".xex": "XBOX360",
            # Dodaj pozostałe mapowania...
        }

        moved_files_log = []

        for file_name in os.listdir(source):
            source_file = os.path.join(source, file_name)
            if os.path.isfile(source_file):
                file_extension = os.path.splitext(file_name)[1].lower()
                file_name_lower = file_name.lower()
                file_size = os.path.getsize(source_file)

                # Określanie systemu na podstawie rozszerzenia
                if file_extension in rom_extensions:
                    rom_system = extension_mapping.get(file_extension, "Inne")
                elif file_extension in image_extensions:
                    rom_system = None
                    if seven_zip_available:
                        try:
                            command = [self.seven_zip_path, 'l', source_file]
                            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            if "unsupported" in result.stderr.lower():
                                self.log(f"Format pliku '{file_name}' nie jest obsługiwany przez 7-Zip.")
                                rom_system = "Inne"
                            else:
                                content = result.stdout
                                if any(keyword in content for keyword in ["SLUS_", "SLES_", "SCUS_", "SCEE_", "SCPS_"]):
                                    rom_system = "PS1"
                                elif "PSP_GAME" in content:
                                    rom_system = "PSP"
                                elif "SYSTEM.CNF" in content:
                                    rom_system = "PS2"
                                elif "PS3_GAME" in content:
                                    rom_system = "PS3"
                                elif "1ST_READ.BIN" in content:
                                    rom_system = "DREAMCAST"
                                elif "GAME.DOL" in content:
                                    rom_system = "GAMECUBE"
                                elif "SYSCONF" in content:
                                    rom_system = "WII"
                                elif "WIIU" in content:
                                    rom_system = "WIIU"
                                elif "Switch" in content:
                                    rom_system = "SWITCH"
                                elif "Xbox360" in content:
                                    rom_system = "XBOX360"
                                elif "icon.sys" in content:
                                    rom_system = "PSVITA"
                                else:
                                    rom_system = "Inne"
                        except Exception as e:
                            self.log(f"Błąd podczas przetwarzania pliku '{file_name}' za pomocą 7-Zip: {e}")
                            rom_system = "Inne"
                    else:
                        rom_system = "Inne"
                elif file_extension in related_extensions:
                    # Pliki powiązane, zostaną przeniesione wraz z głównym plikiem
                    continue
                else:
                    # Próba określenia systemu na podstawie nazwy pliku
                    rom_system = None
                    for key in folder_mappings.keys():
                        if key.lower() in file_name_lower:
                            rom_system = folder_mappings[key].get(system, key)
                            break
                    if not rom_system:
                        rom_system = "Inne"

                # Pobranie nazwy folderu docelowego na podstawie systemu
                mapping = folder_mappings.get(rom_system)
                if mapping:
                    folder_name = mapping.get(system, rom_system)
                else:
                    folder_name = rom_system

                dest_folder = os.path.join(dest, folder_name)

                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)

                dest_file = os.path.join(dest_folder, file_name)
                shutil.move(source_file, dest_file)
                self.log(f"Przeniesiono {source_file} do {dest_file}")
                moved_files_log.append(f"{source_file} -> {dest_file}")

                # Przenoszenie plików powiązanych
                file_base_name = os.path.splitext(file_name)[0]
                for ext in related_extensions:
                    related_file = os.path.join(source, file_base_name + ext)
                    if os.path.isfile(related_file):
                        dest_related_file = os.path.join(dest_folder, os.path.basename(related_file))
                        shutil.move(related_file, dest_related_file)
                        self.log(f"Przeniesiono powiązany plik {related_file} do {dest_related_file}")
                        moved_files_log.append(f"{related_file} -> {dest_related_file}")

        # Zapisywanie logów do pliku
        log_file_path = os.path.join(dest, "file_movements.log")
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            for log_entry in moved_files_log:
                log_file.write(log_entry + "\n")

        messagebox.showinfo("Sukces", f"ROMy zostały posegregowane.\nLog zapisano w {log_file_path}")

    def undo_changes(self):
        # Funkcja cofająca zmiany na podstawie pliku log
        log_file_path = filedialog.askopenfilename(title="Wybierz plik log", filetypes=[("Log files", "*.log"), ("All files", "*.*")])
        if not log_file_path:
            return

        if not os.path.isfile(log_file_path):
            messagebox.showerror("Błąd", "Wybrany plik log nie istnieje.")
            return

        with open(log_file_path, "r", encoding="utf-8") as log_file:
            lines = log_file.readlines()

        for line in lines:
            line = line.strip()
            if "->" in line:
                source, dest = line.split("->")
                source = source.strip()
                dest = dest.strip()
                # Zamiana źródła z celem
                original_source = dest
                original_dest = source

                # Sprawdzenie, czy plik istnieje
                if os.path.isfile(original_source):
                    dest_dir = os.path.dirname(original_dest)
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)

                    shutil.move(original_source, original_dest)
                    self.log(f"Cofnięto {original_source} do {original_dest}")
                else:
                    self.log(f"Plik {original_source} nie istnieje, pomijam.")

        messagebox.showinfo("Sukces", "Zmiany zostały cofnięte na podstawie pliku log.")

    def generate_gamelist(self):
        # Funkcja do generowania pliku gamelist.xml
        roms_path = filedialog.askdirectory(title="Wybierz folder z ROMami")
        if not roms_path:
            return

        if not os.path.isdir(roms_path):
            messagebox.showerror("Błąd", "Wybrana ścieżka nie jest prawidłowym folderem.")
            return

        gamelist_path = os.path.join(roms_path, "gamelist.xml")

        root = ET.Element("gameList")

        for root_dir, dirs, files in os.walk(roms_path):
            for file_name in files:
                file_extension = os.path.splitext(file_name)[1].lower()
                if file_extension in ['.zip', '.7z', '.rar', '.nes', '.smc', '.sfc', '.gba', '.gb', '.gbc', '.n64', '.v64', '.z64', '.nds', '.cia', '.3ds', '.iso', '.bin', '.cue', '.img', '.mdf', '.cdi', '.chd', '.ecm', '.gdi', '.nrg', '.iso']:
                    game = ET.SubElement(root, "game")
                    # Ścieżka do pliku ROM
                    relative_path = os.path.relpath(os.path.join(root_dir, file_name), roms_path)
                    ET.SubElement(game, "path").text = "./" + relative_path.replace("\\", "/")

                    # Nazwa gry (nazwa pliku bez rozszerzenia)
                    game_name = os.path.splitext(file_name)[0]
                    ET.SubElement(game, "name").text = game_name

                    # Wyszukiwanie obrazów
                    image_path = self.find_image(roms_path, game_name, '-image')
                    if image_path:
                        ET.SubElement(game, "image").text = image_path

                    # Wyszukiwanie miniatur
                    thumbnail_path = self.find_image(roms_path, game_name, '-thumb')
                    if thumbnail_path:
                        ET.SubElement(game, "thumbnail").text = thumbnail_path

                    # Dodatkowe pola mogą być dodane tutaj

                    self.log(f"Dodano grę: {game_name}")

        tree = ET.ElementTree(root)
        tree.write(gamelist_path, encoding='utf-8', xml_declaration=True)
        messagebox.showinfo("Sukces", f"Plik gamelist.xml został wygenerowany w {gamelist_path}")

    def find_image(self, roms_path, game_name, suffix):
        # Funkcja do wyszukiwania obrazów dla gry
        for images_folder_name in ['imgs', 'images']:
            images_folder = os.path.join(roms_path, images_folder_name)
            if os.path.isdir(images_folder):
                for img_extension in ['.png', '.jpg', '.jpeg']:
                    image_file_name = f"{game_name}{suffix}{img_extension}"
                    image_file_path = os.path.join(images_folder, image_file_name)
                    if os.path.isfile(image_file_path):
                        relative_image_path = os.path.relpath(image_file_path, roms_path)
                        return "./" + relative_image_path.replace("\\", "/")
        return None

if __name__ == "__main__":
    app = Application()
    app.mainloop()
