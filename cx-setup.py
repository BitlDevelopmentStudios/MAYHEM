#sets up MAYHEM for cx_freeze.
import sys
from cx_Freeze import setup, Executable

# included classes
INCLUDE_FILES = ["actorEngine", "aiEngine", "playerEngine", "spriteEngine"]
# all the sprites/data files
DATA_FILES = ["p1.png", "p2.png", "platform.png", "playerbullet.png", "target.png", "alien.png", "robot.png", "zombie.png", "robotbullet.png", "alienbullet.png", "ufo.png", "ufobullet.png", "grass.png"]
#options
build_exe_options = {'includes': INCLUDE_FILES, 'include_files': DATA_FILES}

#game we should set as executable
target = Executable(
    script="MAYHEM.py",
    base=None,
    icon="icon.ico")

#the EXE details.
setup(
    name = "MAYHEM",
    version = "1.0",
    description = "A horde mode co-op top-down shooter game.",
    author = "Bitl",
    options = {"build_exe": build_exe_options},
    executables = [target])
