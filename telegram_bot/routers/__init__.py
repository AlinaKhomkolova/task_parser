from aiogram import Dispatcher

from .start import router as start_router
from .search import router as search_router
from .help import router as help_router

def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(search_router)
    dp.include_router(help_router)