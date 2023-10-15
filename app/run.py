import asyncio
import os

from dotenv import load_dotenv, find_dotenv

from aiogram import Bot, Dispatcher
from handlers.user_handler import router
load_dotenv(find_dotenv())

from database.models import async_main


async def main():
    await async_main() #Запуск БД
    bot: Bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    
    dp.include_router(router)
    
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as exx:
        print(exit())