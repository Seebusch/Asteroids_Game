import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from game import AsteroidsGame

if __name__ == "__main__":
    space_rocks = AsteroidsGame()
    space_rocks.main_loop()