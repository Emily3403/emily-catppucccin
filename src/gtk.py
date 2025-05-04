import asyncio
import os
import subprocess
from pathlib import Path
from zipfile import ZipFile

import aiofiles
import aiofiles.os as os
import aiohttp

from src.settings import base_save_path, download_chunk_size, base_theme, theme_output_dir, base_persistent_config_dir
from src.utils import force_link

gtk_save_path = base_save_path / "gtk"
gtk_theme_file = gtk_save_path / "theme.zip"
gtk_extracted_dir = gtk_save_path / "extracted"
gtk_config_file = base_persistent_config_dir / "gtk/gtk-settings.ini"


async def download_gtk(release="v1.0.3", ) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://github.com/catppuccin/gtk/releases/download/{release}/{base_theme}.zip') as response:
            if not response.ok:
                print(f"Failed to download: HTTP {response.status}")
                return False

            await os.makedirs(f"{gtk_save_path}", exist_ok=True)
            async with aiofiles.open(gtk_theme_file, "wb") as f:
                chunked_response = response.content.iter_chunked(download_chunk_size)

                while True:
                    try:
                        chunk = await anext(chunked_response)
                        await f.write(chunk)
                    except StopAsyncIteration:
                        break
                    except TimeoutError:
                        await asyncio.sleep(0.5)
                        continue

            with ZipFile(gtk_theme_file) as f:
                f.extractall(gtk_extracted_dir)

        print(f"Successfully downloaded: {gtk_save_path}")
        return True


async def install_gtk():
    save_dir = gtk_extracted_dir / base_theme
    dest_dir = Path.home() / ".local/share/themes/emily-catppuccin"

    if not save_dir.exists():
        print("Theme not downloaded. Please download it first.")
        return

    await os.makedirs(dest_dir.parent, exist_ok=True)
    assert await force_link(save_dir, dest_dir)
    await install_gtk_settings()

async def install_gtk_settings():
    await regenerate_gtk3_config_file()

    assert await force_link(gtk_config_file, Path.home() / ".config/gtk-3.0/settings.ini")
    assert await force_link(gtk_config_file, Path.home() / ".config/gtk-4.0/settings.ini")



async def regenerate_gtk3_config_file():
    if gtk_config_file.exists():
        return

    await os.makedirs(gtk_config_file.parent, exist_ok=True)
    with open(gtk_config_file, "w") as f:
        # TODO: Clean this up
        f.write("""[Settings]
gtk-application-prefer-dark-theme=true
gtk-theme-name=emily-catppuccin

gtk-icon-theme-name=candy-icons
gtk-sound-theme-name=Smooth
gtk-font-name=Noto Sans 10
gtk-menu-images=0
gtk-button-images=0
gtk-toolbar-style=GTK_TOOLBAR_BOTH_HORIZ
gtk-cursor-theme-name=Qogir-Light
gtk-cursor-theme-size=24
gtk-toolbar-icon-size=GTK_ICON_SIZE_LARGE_TOOLBAR
gtk-enable-event-sounds=0
gtk-enable-input-feedback-sounds=0
gtk-xft-antialias=1
gtk-xft-hinting=1
gtk-xft-hintstyle=hintmedium
gtk-xft-rgba=none
gtk-modules=canberra-gtk-module:gail:atk-bridge
""")

    # TODO: Idle inibition via dconf load /
    # [org/gnome/desktop/lockdown]
    # disable-lock-screen=true
    # [org/gnome/desktop/screensaver]
    # idle-activation-enabled=false
    # [org/gnome/desktop/session]
    # idle-delay=uint32 0