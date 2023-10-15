from database.models import async_session
from database.models import Users, Address_FSm, Violations, JESregion
from sqlalchemy import select, update, delete


async def add_new_user(tg_id):
    async with async_session() as session:
        user_query = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        if not user_query:
            session.add(Users(tg_id = tg_id))
            await session.commit()
            return False
        
        return True
    

async def set_region_db(data):
    async with async_session() as session:
        try:
            session.add(JESregion(name=data['region']))
            await session.commit()
            return True
        except:
            return False
        
        
async def set_address_db(data):
    async with async_session() as session:
        try:
            user_d = await session.scalar(select(Users).where(Users.tg_id == data['user']))
            region_d = await session.scalar(select(JESregion).where(JESregion.name == data['region']))
            print(user_d.id, region_d.id)
            address_check = await session.scalar(select(Address_FSm).where(Address_FSm.street==data['street'], Address_FSm.house==data['house'], Address_FSm.flat==data['flat'], Address_FSm.full_name==data['full_name'], Address_FSm.telephone==data['telephone']))
            if not address_check:
                session.add(Address_FSm(street=data['street'], house=data['house'], flat=data['flat'], full_name=data['full_name'], telephone=data['telephone'], user_fk=user_d.id, region_fk=region_d.name))
                await session.commit()
                return True
            else:
                return False
        except Exception as error:
            print(error)
            return False


async def set_violations_db(data):
    async with async_session() as session:
        try:
            address_d = await session.scalar(select(Address_FSm).where(Address_FSm.street==data['street'], Address_FSm.house==data['house'], Address_FSm.flat==data['flat']))
            session.add(Violations(description=data['violations'], address=address_d.id))
            await session.commit()
            return True
        except Exception as exxit:
            print(exxit)
            return False


#Выборка из БД

async def output_addresses_db(data, tg_id):
    async with async_session() as session:
        try:
            user_d = await session.scalar(select(Users).where(Users.tg_id == tg_id))
            addresses = await session.scalars(select(Address_FSm.street, Address_FSm.house, Address_FSm.flat, Address_FSm.id).where(Address_FSm.user_fk == user_d.id, Address_FSm.region_fk == data))
            return addresses
        except Exception as exxit:
            print(exxit)
            return False
        
async def full_information_output_db(id_address, tg_id):
    async with async_session() as session:
        try:
            user_d = await session.scalar(select(Users).where(Users.tg_id == tg_id))
            full_inform = await session.scalars(select(Address_FSm.street, Address_FSm.house, Address_FSm.flat, Address_FSm.full_name, Address_FSm.telephone).where(Address_FSm.id == int(id_address), Address_FSm.user_fk == user_d.id))
            violations_d = await session.scalar(select(Violations.description).where(Violations.address == int(id_address)))
            full = full_inform._fetchall_impl()
            full.append(violations_d)
            return full
        except Exception as exxit:
            print(exxit)
            return False
        
