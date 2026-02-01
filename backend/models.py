from pydantic import BaseModel

class Auto(BaseModel):
    gyarto: str
    modell: str
    ajtok_szama: int
    uzemanyag: str
    hengerurtartalom: int
