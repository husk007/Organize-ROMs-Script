import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
# Mappings of folder names based on the system
folder_mappings = {
    "Abuse SDL": {"Batocera": "abuse", "Stock": "abuse"},
    "Acorn Computers": {"Batocera": "atom", "Stock": "atom"},
    "Acorn Electron": {"Batocera": "electron", "Stock": "electron"},
    "Adventure Vision": {"Batocera": "advision", "Stock": "advision"},
    "Amiga 1200/AGA": {"Batocera": "amiga1200", "Stock": "amiga1200"},
    "Amiga 500/OCS/ECS": {"Batocera": "amiga500", "Stock": "amiga500"},
    "Amstrad CPC": {"Batocera": "amstradcpc", "Stock": "CPC"},
    "Amstrad GX4000": {"Batocera": "gx4000", "Stock": "gx4000"},
    "APF-MP1000/MP-1000/M-1000": {"Batocera": "apfm1000", "Stock": "apfm1000"},
    "Apple II": {"Batocera": "apple2", "Stock": "apple2"},
    "Apple IIGS": {"Batocera": "apple2gs", "Stock": "apple2gs"},
    "Arcade": {"Batocera": "arcade", "Stock": "ARCADE"},
    "Arcadia 2001/et al.": {"Batocera": "arcadia", "Stock": "arcadia"},
    "Archimedes": {"Batocera": "archimedes", "Stock": "archimedes"},
    "Arduboy": {"Batocera": "arduboy", "Stock": "arduboy"},
    "Atari 2600/VCS": {"Batocera": "atari2600", "Stock": "ATARI"},
    "Atari 5200": {"Batocera": "atari5200", "Stock": "FIFTYTWOHUNDRED"},
    "Atari 7800": {"Batocera": "atari7800", "Stock": "SEVENTYEIGHTHUNDRED"},
    "Atari 800": {"Batocera": "atari800", "Stock": "atari800"},
    "Atari Jaguar": {"Batocera": "jaguar", "Stock": "jaguar"},
    "Atari Lynx": {"Batocera": "lynx", "Stock": "LYNX"},
    "Atari ST": {"Batocera": "atarist", "Stock": "atarist"},
    "Atari XEGS": {"Batocera": "xegs", "Stock": "xegs"},
    "Atomiswave": {"Batocera": "atomiswave", "Stock": "atomiswave"},
    "Bally Astrocade/Arcade/ABA-1000": {"Batocera": "astrocde", "Stock": "astrocde"},
    "Bandai Wonderswan": {"Batocera": "wonderswan", "Stock": "wonderswan"},
    "Bandai Wonderswan Color": {"Batocera": "wonderswancolor", "Stock": "WS"},
    "BBC Micro/Master/Archimedes": {"Batocera": "bbc", "Stock": "bbc"},
    "Bermuda Syndrome": {"Batocera": "ports/bermuda", "Stock": "ports/bermuda"},
    "Blake Stone": {"Batocera": "ports/bstone/aog", "Stock": "ports/bstone/aog"},
    "Blake Stone Planet Strike": {"Batocera": "ports/bstone/ps", "Stock": "ports/bstone/ps"},
    "Camputers Lynx": {"Batocera": "camplynx", "Stock": "camplynx"},
    "Cannonball": {"Batocera": "cannonball", "Stock": "cannonball"},
    "Capcom PlaySystem 1": {"Batocera": "cps1", "Stock": "CPS1"},
    "Capcom PlaySystem 2": {"Batocera": "cps2", "Stock": "CPS2"},
    "Capcom PlaySystem 3": {"Batocera": "cps3", "Stock": "CPS3"},
    "Casio PV-1000/ぴーぶいせん/Pi Bui-Sen": {"Batocera": "pv1000", "Stock": "pv1000"},
    "Cave Story": {"Batocera": "ports/CaveStory", "Stock": "ports/CaveStory"},
    "C-Dogs (Cdogs-sdl)": {"Batocera": "ports/cdogs-sdl", "Stock": "ports/cdogs-sdl"},
    "Celeste": {"Batocera": "ports/celeste", "Stock": "ports/celeste"},
    "Coleco Adam": {"Batocera": "adam", "Stock": "adam"},
    "ColecoVision": {"Batocera": "colecovision", "Stock": "COLECO"},
    "Commander Keen": {"Batocera": "ports/cgenius", "Stock": "ports/cgenius"},
    "Commodore 128 (C128)": {"Batocera": "c128", "Stock": "c128"},
    "Commodore 64": {"Batocera": "c64", "Stock": "COMMODORE"},
    "Commodore Amiga": {"Batocera": "amiga", "Stock": "AMIGA"},
    "Commodore Amiga CD 32": {"Batocera": "amigacd32", "Stock": "amigacd32"},
    "Commodore CDTV": {"Batocera": "amigacdtv", "Stock": "amigacdtv"},
    "Commodore PET": {"Batocera": "pet", "Stock": "pet"},
    "Commodore Plus/4": {"Batocera": "cplus4", "Stock": "cplus4"},
    "Commodore Plus4": {"Batocera": "c16", "Stock": "c16"},
    "Commodore VIC-20/VC-20": {"Batocera": "c20", "Stock": "VIC20"},
    "CreatiVision/Educat 2002/Dick Smith Wizzard/FunVision": {"Batocera": "crvision", "Stock": "crvision"},
    "Daphne": {"Batocera": "daphne", "Stock": "daphne"},
    "DAPHNE (Laserdisc)": {"Batocera": "daphne", "Stock": "daphne"},
    "DevilutionX": {"Batocera": "devilutionx", "Stock": "devilutionx"},
    "Diablo": {"Batocera": "ports/diablo", "Stock": "ports/diablo"},
    "Diablo Hellfire": {"Batocera": "ports/diablo", "Stock": "ports/diablo"},
    "Dinothawr": {"Batocera": "ports/dinothawr", "Stock": "ports/dinothawr"},
    "Doom": {"Batocera": "ports/doom", "Stock": "ports/doom"},
    "Doom 2": {"Batocera": "ports/doom2", "Stock": "ports/doom2"},
    "DOS x86": {"Batocera": "pc", "Stock": "pc"},
    "DOSbox": {"Batocera": "dos", "Stock": "DOS"},
    "Duke Nukem 2 (RigelEngine)": {"Batocera": "ports/rigelengine", "Stock": "ports/rigelengine"},
    "Duke Nukem 3D": {"Batocera": "ports/eduke", "Stock": "ports/eduke"},
    "DXX-Rebirth": {"Batocera": "dxx-rebirth", "Stock": "dxx-rebirth"},
    "EasyRPG": {"Batocera": "easyrpg", "Stock": "easyrpg"},
    "ECWolf": {"Batocera": "ecwolf", "Stock": "ecwolf"},
    "EDuke32": {"Batocera": "eduke32", "Stock": "eduke32"},
    "Fairchild Channel F": {"Batocera": "channelf", "Stock": "FAIRCHILD"},
    "Fallout": {"Batocera": "ports/falloutce1", "Stock": "ports/falloutce1"},
    "Fallout 2": {"Batocera": "ports/falloutce2", "Stock": "ports/falloutce2"},
    "Final Burn Neo": {"Batocera": "fbneo", "Stock": "fbneo"},
    "Flashback": {"Batocera": "ports/reminiscence", "Stock": "ports/reminiscence"},
    "Flashpoint": {"Batocera": "flash", "Stock": "flash"},
    "Flatpak": {"Batocera": "flatpak", "Stock": "flatpak"},
    "FM Towns/Towns Marty": {"Batocera": "fmtowns", "Stock": "fmtowns"},
    "Fujitsu FM-Towns": {"Batocera": "fmtownsux", "Stock": "fmtownsux"},
    "Fujitsu Micro 7 (FM-7)": {"Batocera": "fm7", "Stock": "fm7"},
    "Future Pinball": {"Batocera": "fpinball", "Stock": "fpinball"},
    "Gamate/chāojí xiǎozi/Super Boy/chāojí shéntóng/Super Child Prodigy": {"Batocera": "gamate", "Stock": "gamate"},
    "Game Boy 2 Players": {"Batocera": "gb2players", "Stock": "gb2players"},
    "Game Boy Color 2 Players": {"Batocera": "gbc2players", "Stock": "gbc2players"},
    "Game Gear": {"Batocera": "gamegear", "Stock": "GG"},
    "Game Master/Systema 2000/Super Game/Game Tronic": {"Batocera": "gmaster", "Stock": "gmaster"},
    "Game Pocket Computer": {"Batocera": "gamepock", "Stock": "gamepock"},
    "Game.com": {"Batocera": "gamecom", "Stock": "gamecom"},
    "Gamemaker Loader": {"Batocera": "gmloader", "Stock": "gmloader"},
    "GP32": {"Batocera": "gp32", "Stock": "gp32"},
    "GZDoom": {"Batocera": "gzdoom", "Stock": "gzdoom"},
    "Half-Life": {"Batocera": "ports/half-life", "Stock": "ports/half-life"},
    "Handheld LCD Games": {"Batocera": "lcdgames", "Stock": "lcdgames"},
    "Heart of Darkness": {"Batocera": "ports/hode", "Stock": "ports/hode"},
    "Heroes of Might and Magic II": {"Batocera": "ports/fheroes2", "Stock": "ports/fheroes2"},
    "Hurrican": {"Batocera": "hurrican", "Stock": "hurrican"},
    "Hydra Castle Labyrinth": {"Batocera": "hcl", "Stock": "hcl"},
    "Ikemen Go": {"Batocera": "ikemen", "Stock": "ikemen"},
    "Intellivision": {"Batocera": "intellivision", "Stock": "INTELLIVISION"},
    "Ion Fury": {"Batocera": "fury", "Stock": "fury"},
    "Java Games": {"Batocera": "freej2me", "Stock": "freej2me"},
    "Jazz Jackrabbit (OpenJazz)": {"Batocera": "ports/openjazz", "Stock": "ports/openjazz"},
    "Karaoke": {"Batocera": "karaoke", "Stock": "karaoke"},
    "Laser 310": {"Batocera": "laser310", "Stock": "laser310"},
    "Lowres NX": {"Batocera": "lowresnx", "Stock": "lowresnx"},
    "Lutro": {"Batocera": "lutro", "Stock": "lutro"},
    "M.U.G.E.N": {"Batocera": "mugen", "Stock": "mugen"},
    "Macintosh 128K": {"Batocera": "macintosh", "Stock": "macintosh"},
    "Magnavox Odyssey 2": {"Batocera": "odyssey", "Stock": "ODYSSEY"},
    "Magnavox Odyssey²/Philips Videopac G7000/Philips Odyssey/Odyssey²": {"Batocera": "odyssey2", "Stock": "odyssey2"},
    "MAME Video Game Music Player": {"Batocera": "vgmplay", "Stock": "vgmplay"},
    "Mattel Intellivision": {"Batocera": "intellivision", "Stock": "INTELLIVISION"},
    "Media Player": {"Batocera": "mplayer", "Stock": "mplayer"},
    "Mega Duck/Cougar Boy": {"Batocera": "megaduck", "Stock": "MEGADUCK"},
    "Microsoft MSX turboR": {"Batocera": "msxturbor", "Stock": "msxturbor"},
    "Microsoft MSX1": {"Batocera": "msx1", "Stock": "msx1"},
    "Microsoft MSX2": {"Batocera": "msx2", "Stock": "MSX"},
    "Microsoft MSX2plus": {"Batocera": "msx2+", "Stock": "msx2+"},
    "Microsoft Xbox": {"Batocera": "xbox", "Stock": "xbox"},
    "Microsoft Xbox 360": {"Batocera": "xbox360", "Stock": "xbox360"},
    "Milton Bradley Vectrex": {"Batocera": "vectrex", "Stock": "VECTREX"},
    "Moonlight": {"Batocera": "moonlight", "Stock": "moonlight"},
    "Mr. Boom": {"Batocera": "mrboom", "Stock": "mrboom"},
    "MSX": {"Batocera": "msx", "Stock": "msx"},
    "Multiple Arcade Machine Emulator": {"Batocera": "mame", "Stock": "mame"},
    "Namco System 246": {"Batocera": "namco2x6", "Stock": "namco2x6"},
    "Near's Super Nintendo MSU1": {"Batocera": "snesmsu1", "Stock": "snesmsu1"},
    "NEC PC-8800": {"Batocera": "pc88", "Stock": "pc88"},
    "NEC PC-9800/PC-98": {"Batocera": "pc98", "Stock": "pc98"},
    "NEC PC-FX": {"Batocera": "pcfx", "Stock": "pcfx"},
    "NEC Super Grafx": {"Batocera": "sgfx", "Stock": "SGFX"},
    "NEC TurboGrafx 16": {"Batocera": "tg16", "Stock": "PCE"},
    "NEC TurboGrafx 16-CD": {"Batocera": "tg16cd", "Stock": "PCECD"},
    "Neo Geo CD": {"Batocera": "neogeocd", "Stock": "NEOCD"},
    "Nintendo 3DS": {"Batocera": "3ds", "Stock": "3ds"},
    "Nintendo 64": {"Batocera": "n64", "Stock": "n64"},
    "Nintendo 64DD": {"Batocera": "n64dd", "Stock": "n64dd"},
    "Nintendo DS": {"Batocera": "nds", "Stock": "NDS"},
    "Nintendo Entertainment System Hacks": {"Batocera": "nesh", "Stock": "nesh"},
    "Nintendo Entertainment System/Famicom": {"Batocera": "nes", "Stock": "FC"},
    "Nintendo Famicom": {"Batocera": "famicom", "Stock": "famicom"},
    "Nintendo Family Computer Disk System/Famicom": {"Batocera": "fds", "Stock": "FDS"},
    "Nintendo Game and Watch": {"Batocera": "gameandwatch", "Stock": "GW"},
    "Nintendo Game Boy": {"Batocera": "gb", "Stock": "GB"},
    "Nintendo Game Boy 2 Players": {"Batocera": "gb2players", "Stock": "gb2players"},
    "Nintendo Game Boy Advance": {"Batocera": "gba", "Stock": "GBA"},
    "Nintendo Game Boy Advance hacks": {"Batocera": "gbah", "Stock": "gbah"},
    "Nintendo Game Boy Color": {"Batocera": "gbc", "Stock": "GBC"},
    "Nintendo Game Boy Color 2 Players": {"Batocera": "gbc2players", "Stock": "gbc2players"},
    "Nintendo Game Boy Color Hacks": {"Batocera": "gbch", "Stock": "gbch"},
    "Nintendo Game Boy Hacks": {"Batocera": "gbh", "Stock": "gbh"},
    "Nintendo GameCube": {"Batocera": "gamecube", "Stock": "gamecube"},
    "Nintendo Super Famicom": {"Batocera": "sfc", "Stock": "sfc"},
    "Nintendo Super Nintendo Hacks": {"Batocera": "snesh", "Stock": "snesh"},
    "Nintendo Virtual Boy": {"Batocera": "virtualboy", "Stock": "VB"},
    "Nintendo Wii": {"Batocera": "wii", "Stock": "wii"},
    "Nintendo Wii U": {"Batocera": "wiiu", "Stock": "wiiu"},
    "Open Beats of Rage": {"Batocera": "openbor", "Stock": "openbor"},
    "Openjazz": {"Batocera": "openjazz", "Stock": "openjazz"},
    "Othello Multivision": {"Batocera": "multivision", "Stock": "multivision"},
    "Out Run (Cannonball)": {"Batocera": "ports/cannonball", "Stock": "ports/cannonball"},
    "Panasonic 3DO Interactive Multiplayer": {"Batocera": "3do", "Stock": "3do"},
    "PC Engine CD-ROM²/PC Engine Duo R/PC Engine Duo RX/TurboGrafx-CD/TurboDuo": {"Batocera": "pcenginecd", "Stock": "pcenginecd"},
    "PC Engine SuperGrafx/SuperGrafx/PCエンジンスーパーグラフィックス/Pī Shī Enjin SūpāGurafikkusu/PC Engine 2": {"Batocera": "supergrafx", "Stock": "supergrafx"},
    "PC Engine/TurboGrafx-16": {"Batocera": "pcengine", "Stock": "pcengine"},
    "Philips Compact Disc Interactive/CD-i": {"Batocera": "cdi", "Stock": "cdi"},
    "Philips VideoPac": {"Batocera": "videopac", "Stock": "VIDEOPAC"},
    "Philips Videopac+ G7400/G7420": {"Batocera": "videopacplus", "Stock": "videopacplus"},
    "PICO-8 fantasy console": {"Batocera": "pico8", "Stock": "PICO"},
    "PlayStation Vita": {"Batocera": "psvita", "Stock": "psvita"},
    "Plug 'n' Play/Handheld TV Games": {"Batocera": "plugnplay", "Stock": "plugnplay"},
    "Pokémon Mini": {"Batocera": "pokemini", "Stock": "POKE"},
    "PolyGame Master": {"Batocera": "pgm2", "Stock": "pgm2"},
    "Portmaster": {"Batocera": "ports/", "Stock": "ports/"},
    "PrBoom": {"Batocera": "prboom", "Stock": "prboom"},
    "pygame": {"Batocera": "pygame", "Stock": "pygame"},
    "Pyxel fantasy console": {"Batocera": "pyxel", "Stock": "pyxel"},
    "Quake": {"Batocera": "ports/quake/id1", "Stock": "ports/quake/id1"},
    "Raze": {"Batocera": "raze", "Stock": "raze"},
    "RetroArch": {"Batocera": "RetroArch", "Stock": "RetroArch"},
    "Rick Dangerous": {"Batocera": "ports/xrick", "Stock": "ports/xrick"},
    "SAM Coupé": {"Batocera": "samcoupe", "Stock": "samcoupe"},
    "Sammy Atomiswave": {"Batocera": "atomiswave", "Stock": "atomiswave"},
    "Satellaview": {"Batocera": "satellaview", "Stock": "SATELLAVIEW"},
    "ScummVM": {"Batocera": "scummvm", "Stock": "SCUMMVM"},
    "SDLPoP": {"Batocera": "sdlpop", "Stock": "sdlpop"},
    "Sega 32X": {"Batocera": "sega32x", "Stock": "THIRTYTWOX"},
    "Sega CD/Mega CD": {"Batocera": "segacd", "Stock": "SEGACD"},
    "Sega Dreamcast": {"Batocera": "dreamcast", "Stock": "dreamcast"},
    "Sega Game Gear Hacks": {"Batocera": "gamegearh", "Stock": "gamegearh"},
    "Sega Genesis": {"Batocera": "genesis", "Stock": "MD"},
    "Sega Genesis Hacks": {"Batocera": "genh", "Stock": "genh"},
    "Sega Genesis/Mega Drive": {"Batocera": "megadrive", "Stock": "megadrive"},
    "Sega Master System/Mark III": {"Batocera": "mastersystem", "Stock": "MS"},
    "Sega Mega Drive Japan": {"Batocera": "megadrive-japan", "Stock": "megadrive-japan"},
    "Sega Mega Drive MSU": {"Batocera": "megadrivemsu", "Stock": "megadrivemsu"},
    "Sega Model 1": {"Batocera": "mame/model1", "Stock": "mame/model1"},
    "Sega Model 2": {"Batocera": "mame/model2", "Stock": "mame/model2"},
    "Sega Model 3": {"Batocera": "mame/model3", "Stock": "mame/model3"},
    "Sega Naomi": {"Batocera": "naomi", "Stock": "naomi"},
    "Sega NAOMI 2": {"Batocera": "naomi2", "Stock": "naomi2"},
    "Sega Pico": {"Batocera": "pico", "Stock": "pico"},
    "Sega Saturn": {"Batocera": "saturn", "Stock": "saturn"},
    "Sega SC-3000": {"Batocera": "sc-3000", "Stock": "sc-3000"},
    "Sega SG-1000/SG-1000 II/SC-3000": {"Batocera": "sg1000", "Stock": "SEGASGONE"},
    "Sharp X1": {"Batocera": "x1", "Stock": "x1"},
    "Sharp X68000": {"Batocera": "x68000", "Stock": "x68000"},
    "Shovel Knight": {"Batocera": "ports/shovelknight", "Stock": "ports/shovelknight"},
    "Sinclair ZX Spectrum": {"Batocera": "zxspectrum", "Stock": "ZXS"},
    "Sinclair ZX81": {"Batocera": "zx81", "Stock": "zx81"},
    "SINGE": {"Batocera": "singe", "Stock": "singe"},
    "SNK Neo-Geo MVS": {"Batocera": "neogeo", "Stock": "NEOGEO"},
    "SNK Neo-Geo Pocket": {"Batocera": "ngp", "Stock": "ngp"},
    "SNK Neo-Geo Pocket Color": {"Batocera": "ngpc", "Stock": "NGP"},
    "Solarus": {"Batocera": "solarus", "Stock": "solarus"},
    "Sonic 1": {"Batocera": "ports/sonic1", "Stock": "ports/sonic1"},
    "Sonic 2": {"Batocera": "ports/sonic2", "Stock": "ports/sonic2"},
    "Sonic CD": {"Batocera": "ports/soniccd", "Stock": "ports/soniccd"},
    "Sonic Mania": {"Batocera": "ports/sonicmania", "Stock": "ports/sonicmania"},
    "Sony PlayStation": {"Batocera": "psx", "Stock": "PS"},
    "Sony PlayStation 2": {"Batocera": "ps2", "Stock": "ps2"},
    "Sony PlayStation 3": {"Batocera": "ps3", "Stock": "ps3"},
    "Sony PlayStation Portable": {"Batocera": "psp", "Stock": "psp"},
    "Sony PlayStation Portable Minis": {"Batocera": "pspminis", "Stock": "pspminis"},
    "Spectravideo": {"Batocera": "spectravideo", "Stock": "spectravideo"},
    "Star Engine/Sonic Retro Engine": {"Batocera": "sonicretro", "Stock": "sonicretro"},
    "Steam": {"Batocera": "steam", "Stock": "steam"},
    "Streets of Rage Remake (Sorr)": {"Batocera": "ports/sorr", "Stock": "ports/sorr"},
    "SuFami Turbo": {"Batocera": "sufami", "Stock": "SUFAMI"},
    "Super A'Can": {"Batocera": "supracan", "Stock": "supracan"},
    "Super Cassette Vision/スーパーカセットビジョン/Suupaa Kasetto Bijon": {"Batocera": "scv", "Stock": "scv"},
    "Super Game Boy": {"Batocera": "sgb", "Stock": "SGB"},
    "Super Mario War": {"Batocera": "superbroswar", "Stock": "superbroswar"},
    "Super NES CD-ROM/SNES MSU-1": {"Batocera": "snes_msu-1", "Stock": "snes_msu-1"},
    "Super Nintendo Entertainment System": {"Batocera": "snes", "Stock": "SFC"},
    "SuperTux": {"Batocera": "ports/supertux", "Stock": "ports/supertux"},
    "SuperTuxKart": {"Batocera": "ports/supertuxkart", "Stock": "ports/supertuxkart"},
    "Tandy Video Information System": {"Batocera": "vis", "Stock": "vis"},
    "Thomson MO/TO Series Computer": {"Batocera": "thomson", "Stock": "thomson"},
    "TI-99/4 (TI-99/4A)": {"Batocera": "ti99", "Stock": "ti99"},
    "TIC-80 fantasy console": {"Batocera": "tic80", "Stock": "TIC"},
    "TMNTSR": {"Batocera": "ports/tmntsr", "Stock": "ports/tmntsr"},
    "Tomy Tutor/Pyūta/Grandstand Tutor": {"Batocera": "tutor", "Stock": "tutor"},
    "Triforce": {"Batocera": "triforce", "Stock": "triforce"},
    "TRS-80/Tandy Color Computer": {"Batocera": "coco", "Stock": "coco"},
    "Turrican (Hurrican)": {"Batocera": "ports/hurrican/data", "Stock": "ports/hurrican/data"},
    "Tyrian (OpenTyrian)": {"Batocera": "ports/opentyrian", "Stock": "ports/opentyrian"},
    "TyrQuake": {"Batocera": "tyrquake", "Stock": "tyrquake"},
    "Uzebox Open-Source console": {"Batocera": "uzebox", "Stock": "uzebox"},
    "V.Smile (TV LEARNING SYSTEM)": {"Batocera": "vsmile", "Stock": "vsmile"},
    "Video Computer 4000": {"Batocera": "vc4000", "Stock": "vc4000"},
    "Visual Pinball": {"Batocera": "vpinball", "Stock": "vpinball"},
    "Voxatron fantasy console": {"Batocera": "voxatron", "Stock": "voxatron"},
    "VVVVVV": {"Batocera": "ports/VVVVVV", "Stock": "ports/VVVVVV"},
    "WASM4 fantasy console": {"Batocera": "wasm4", "Stock": "wasm4"},
    "Watara Supervision": {"Batocera": "supervision", "Stock": "SUPERVISION"},
    "WINE": {"Batocera": "windows", "Stock": "windows"},
    "Wolfenstein 3D": {"Batocera": "ports/ecwolf/games", "Stock": "ports/ecwolf/games"},
    "WonderSwan": {"Batocera": "wswan", "Stock": "wswan"},
    "WonderSwan Color": {"Batocera": "wswanc", "Stock": "wswanc"},
    "Xash3D FWGS": {"Batocera": "xash3d_fwgs", "Stock": "xash3d_fwgs"},
}

# Jeśli nazwa nie występuje w mappingu, pozostaje bez zmian

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do zarządzania ROMami - Wersja 1.0.0")
        self.geometry("800x700")
        self.seven_zip_path = None

        # Pobranie ścieżki bazowej
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        # Ścieżka do pliku ikony
        icon_path = os.path.join(base_path, 'icon.ico')
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
            "Aplikacja do zarządzania ROMami - Wersja 1.0.0\n\n"
            "Funkcje:\n"
            "- Zmiana nazw folderów w zależności od wybranego systemu.\n"
            "- Segregowanie plików ROM do odpowiednich folderów na podstawie rozszerzeń plików i zawartości.\n"
            "- Cofanie zmian na podstawie pliku log.\n\n"
            "Instrukcja obsługi:\n"
            "1. Wybierz system za pomocą odpowiednich przycisków radiowych.\n"
            "2. Wskaż ścieżkę źródłową i docelową.\n"
            "3. Użyj przycisków akcji do wykonania odpowiednich operacji.\n"
            "4. W przypadku korzystania z funkcji segregowania ROMów, upewnij się, że masz zainstalowany 7-Zip oraz odpowiednie pluginy.\n\n"
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
            # ... (upewnij się, że tutaj znajduje się pełny mapping rozszerzeń z poprzedniej odpowiedzi)
            ".nes": "NES",
            ".smc": "SNES",
            ".sfc": "SNES",
            ".gb": "GB",
            ".gbc": "GBC",
            ".gba": "GBA",
            ".nds": "NDS",
            ".dsi": "DSi",
            ".n64": "N64",
            ".z64": "N64",
            ".v64": "N64",
            ".ngp": "NGP",
            ".ngc": "NGP",
            ".pce": "PCE",
            ".vb": "VB",
            ".ws": "WS",
            ".wsc": "WS",
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

if __name__ == "__main__":
    app = Application()
    app.mainloop()