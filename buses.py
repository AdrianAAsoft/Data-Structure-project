from dataclasses import dataclass
from typing import List

@dataclass
class LineaBus:
    nombre: str
    paradas: List[str]

# Ejemplo (no usado aún por app.py):
DEMO_LINEAS = [
    LineaBus(nombre="L1", paradas=["Avenida", "Central", "Estación"]),
    LineaBus(nombre="L2", paradas=["Central", "Parque", "Universidad"]),
]
