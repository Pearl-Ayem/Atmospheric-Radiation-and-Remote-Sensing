import sys
from pathlib import Path
import site

path=Path(__file__).resolve()
sys.path.insert(0,path.parent.parent)
sep='*'*30
print(f'{sep}\ncontext imported. Front of path:\n{sys.path[0]}\n{sys.path[1]}\n{sep}\n')
site.removeduppaths()
