from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from typing import List
import config


engine = create_async_engine(
    url=config.SQLALCHEMY_URL,
    echo=config.SQLALCHEMY_ECHO
)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    
    address_rel: Mapped[List['Address_FSm']] = relationship(back_populates='user_rel', cascade='all, delete')


class JESregion(Base):
    __tablename__ = 'JES_region'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))

    address_rel: Mapped[List['Address_FSm']] = relationship(back_populates='region_rel', cascade='all, delete')


class Address_FSm(Base):
    __tablename__ = 'address_FSm'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column(String(30))
    house: Mapped[str] = mapped_column(String(5))
    flat: Mapped[str] = mapped_column(String(5))
    full_name: Mapped[str] = mapped_column(String(50))
    telephone: Mapped[str] = mapped_column(String(15))
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    region_fk: Mapped[str] = mapped_column(ForeignKey('JES_region.name', ondelete='CASCADE'))
    
    user_rel: Mapped['Users'] = relationship(back_populates='address_rel')
    region_rel: Mapped['JESregion'] = relationship(back_populates='address_rel')
    
    violations_rel: Mapped[List['Violations']] = relationship(back_populates='address_rel', cascade='all, delete')
    

class Violations(Base):
    __tablename__ = 'violations'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(200))
    #photo: Mapped[str] = mapped_column()
    address: Mapped[int] = mapped_column(ForeignKey('address_FSm.id', ondelete='CASCADE'))
    
    address_rel: Mapped[List['Address_FSm']] = relationship(back_populates='violations_rel')
    
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)