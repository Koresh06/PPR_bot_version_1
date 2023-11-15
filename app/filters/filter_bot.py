from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class UpdateRecord(BaseFilter):
    
    def __init__(self, title='Добавить запись') -> None:
        self.title = title
        
    async def __call__(self, message: Message) -> bool:
        return message.text in self.title
    
class Output_addresses(BaseFilter):
    
    def __init__(self, title='Вывод адресов') -> None:
        self.title = title
        
    async def __call__(self, message: Message) -> bool:
        return message.text in self.title
  
class IsDigitCheckTg_id(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data.isdigit() and len(callback.data) == 10:
            return True   
        
class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()
    
