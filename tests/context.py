import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Smart/Hacky fix til at kunne tilgå passenger.passenger fra tests dir
# Bemærk at 'passenger' IKKE er unused, trods Pycharm siger det.
import andelsbolig
