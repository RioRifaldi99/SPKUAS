from sqlalchemy import String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Handphone(Base):
    __tablename__ = "handphone"
    id = Column(Integer, primary_key=True)
    nama_handphone = Column(String(255))
    ram_Gb = Column(Integer)
    rom_Gb = Column(Integer)
    chipset = Column(String(255))
    layar = Column(String(255))
    harga_Rp = Column(Integer)
    baterai_mAh = Column(Integer)

    def __repr__(self):
        return f"Handphone(nama_handphone={self.nama_handphone!r}, ram_Gb={self.ram_Gb!r}, rom_Gb={self.rom_Gb!r}, chipset={self.chipset!r}, layar={self.layar!r}, harga_Rp={self.harga_Rp!r}, baterai_mAh={self.baterai_mAh!r})"