import asyncio

from src.gtk import download_gtk, install_gtk
from src.replace import replace_colors


async def main():
    await download_gtk()
    await replace_colors()
    await install_gtk()


if __name__ == "__main__":
    asyncio.run(main())
