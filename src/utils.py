from pathlib import Path

import aiofiles.os as os


async def force_link(src: Path, dest: Path) -> bool:
    if dest.is_symlink():
        target = dest.readlink()
        if target == src:
            return True

        # Todo: This might fail with IsADirectoryError because the unlink follows
        target.unlink()
    elif dest.exists():
        print("File already exists here, not overwriting!")
        return False

    await os.symlink(src, dest)

    return True