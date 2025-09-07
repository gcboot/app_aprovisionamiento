from dataclasses import dataclass
from datetime import datetime

@dataclass
class Usuario:
    id: str
    auth_id: str
    nombre: str
    rol: str
    creado_en: datetime