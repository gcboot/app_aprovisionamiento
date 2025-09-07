from dataclasses import dataclass
from datetime import datetime

@dataclass
class Sesion:
    id: int
    usuario_id: str
    inicio: datetime
    fin: datetime
    ip: str
    dispositivo: str
    activo: bool