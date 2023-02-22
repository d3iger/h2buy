import config
import logging
from aiogram import Bot, Dispatcher, executor

import parse_mm
import parse_varus
import parse_cm
import parse_eko
import parse_metro
import parse_auchan
import parse_novus
import parse_tv
import parse_um
import parse_vostorg
import parse_pchelka
import parse_kosmos
import parse_stol


import fnc

from sqlite import sqlight
import Levenshtein as lev
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import copy
import math
import asyncio
from contextlib import suppress
from aiogram import types
import aiogram.utils.exceptions
import aioschedule


# DATABASE SETUP
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
dba = sqlight(r'./db/parse_auchan.db')  # Auchan
dbn = sqlight(r'./db/parse_novus.db')  # Novus
dbv = sqlight(r'./db/parse_varus.db')  # Varus
dbm = sqlight(r'./db/parse_mm.db')  # MegaMarket
db_vs = sqlight(r'./db/parse_vostorg.db')  # Vostorg
db_um = sqlight(r'./db/parse_um.db')  # UltraMarket
db_eko = sqlight(r'./db/parse_eko.db')  # EkoMarket
db_cm = sqlight(r'./db/parse_cm.db')  # CityMarket
db_tv = sqlight(r'./db/parse_tv.db')  # EkoMarket
db_metro = sqlight(r'./db/parse_metro.db')  # CityMarket
db_pch = sqlight(r'./db/parse_pchelka.db')  # Pchelka
db_ksms = sqlight(r'./db/parse_kosmos.db')  # Kosmos
db_stol = sqlight(r'./db/parse_stolichniy.db')  # Sctolichniy
# DATABASE SETUP

# NAME LIST PRICE
name_list_price_novus_dict = {}
name_list_price_auchan_dict = {}
name_list_price_varus_dict = {}
name_list_price_mm_dict = {}
name_list_price_vs_dict = {}
name_list_price_eko_dict = {}
name_list_price_metro_dict = {}
name_list_price_um_dict = {}
name_list_price_tv_dict = {}
name_list_price_cm_dict = {}
name_list_price_pch_dict = {}
name_list_price_ksms_dict = {}
name_list_price_stol_dict = {}
# NAME LIST PRICE

# PRICE
price_auchan_dict = {}
price_novus_dict = {}
price_varus_dict = {}
price_mm_dict = {}
price_eko_dict = {}
price_vs_dict = {}
price_metro_dict = {}
price_tv_dict = {}
price_cm_dict = {}
price_um_dict = {}
price_pch_dict = {}
price_ksms_dict = {}
price_stol_dict = {}
# PRICE

# PRICE NAME
price_auchan_name_dict = {}
price_novus_name_dict = {}
price_varus_name_dict = {}
price_mm_name_dict = {}
price_vs_name_dict = {}
price_tv_name_dict = {}
price_cm_name_dict = {}
price_um_name_dict = {}
price_eko_name_dict = {}
price_metro_name_dict = {}
price_pch_name_dict = {}
price_ksms_name_dict = {}
price_stol_name_dict = {}
# PRICE NAME

# PRICE STR
price_names = ''
# PRICE STR

# NAME PRICE
name_price_auchan_dict = {}
name_price_novus_dict = {}
name_price_varus_dict = {}
name_price_mm_dict = {}
name_price_vs_dict = {}
name_price_metro_dict = {}
name_price_eko_dict = {}
name_price_tv_dict = {}
name_price_cm_dict = {}
name_price_um_dict = {}
name_price_pch_dict = {}
name_price_ksms_dict = {}
name_price_stol_dict = {}
# NAME PRICE

# PODBOR NAME
podbor_name_novus_dict = {}
podbor_name_auchan_dict = {}
podbor_name_varus_dict = {}
podbor_name_mm_dict = {}
podbor_name_vs_dict = {}
podbor_name_tv_dict = {}
podbor_name_eko_dict = {}
podbor_name_cm_dict = {}
podbor_name_metro_dict = {}
podbor_name_um_dict = {}
podbor_name_pch_dict = {}
podbor_name_ksms_dict = {}
podbor_name_stol_dict = {}
# PODBOR NAME

dba_int_dict = {}
dbn_int_dict = {}
dbv_int_dict = {}
dbm_int_dict = {}
db_metro_int_dict = {}
db_vs_int_dict = {}
db_eko_int_dict = {}
db_cm_int_dict = {}
db_um_int_dict = {}
db_tv_int_dict = {}
db_pch_int_dict = {}
db_ksms_int_dict = {}
db_stol_int_dict = {}

names_u_list_dict = {}

podbor_name_auchan_novus_dict = {}

podbor_str_index_podbor_dict = {}




def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper


def change(lst, sz):
    lst_r = [lst[i:i + sz] for i in range(0, len(lst), sz)]
    return lst_r


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(aiogram.utils.exceptions.MessageCantBeDeleted, aiogram.utils.exceptions.MessageToDeleteNotFound):
        await message.delete()


def find_name(name_str, db):
    names = []
    all_names_lower = db.get_names_lower()
    all_names = list(db.get_names())
    name_lower = name_str.lower()
    name_p = name_str.replace(' ', '')
    for n in range(len(all_names)):
        if (((lev.distance(str(name_lower), str(all_names_lower[n]))) * 100) / len(name_lower)) <= 30 and (
                ((lev.distance(str(name_lower), str(all_names_lower[n]))) * 100) / len(name_lower)) != 0:
            names.append(str(all_names[n][0]))
    return names


def find_name_x(name_str, db, x):
    names = []
    all_names_lower = db.get_names_lower()
    all_names = db.get_names()
    name_lower = name_str.lower()
    name_p = name_str.replace(' ', '')
    for n in range(0, len(all_names) - 1):
        if (((lev.distance(str(name_lower), str(all_names_lower[n]))) * 100) / len(name_lower)) <= x and (
                ((lev.distance(str(name_lower), str(all_names_lower[n]))) * 100) / len(name_lower)) != 0:
            names.append(str(all_names[n][0]))
    return names


def check_levels(lst):
    for item in lst:
        if isinstance(item, list):
            return False
    else:
        return True


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("FLOOD DETECTED")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer('Введи название продукта.')


@dp.message_handler(content_types=['text'])
@dp.throttled(anti_flood, rate=1)
async def name(message: types.Message):
    i = 0

    names_u_list = []
    global names_u_list_dict

    global podbor_str_index_podbor_dict

    # db_int
    global dba_int_dict
    dba_int = 0
    global dbn_int_dict
    dbn_int = 0
    global dbv_int_dict
    dbv_int = 0
    global dbm_int_dict
    dbm_int = 0
    global db_tv_int_dict
    db_tv_int = 0
    global db_cm_int_dict
    db_cm_int = 0
    global db_eko_int_dict
    db_eko_int = 0
    global db_metro_int_dict
    db_metro_int = 0
    global db_vs_int_dict
    db_vs_int = 0
    global db_um_int_dict
    db_um_int = 0

    global db_pch_int_dict
    db_pch_int = 0
    global db_ksms_int_dict
    db_ksms_int = 0
    global db_stol_int_dict
    db_stol_int = 0

    # PRICE
    global price_auchan_dict
    price_auchan = []
    global price_novus_dict
    price_novus = []
    global price_mm_dict
    price_mm = []
    global price_varus_dict
    price_varus = []
    global price_metro_dict
    price_metro = []
    global price_tv_dict
    price_tv = []
    global price_vs_dict
    price_vs = []
    global price_cm_dict
    price_cm = []
    global price_um_dict
    price_um = []
    global price_eko_dict
    price_eko = []

    global price_ksms_dict
    price_ksms = []
    global price_stol_dict
    price_stol = []
    global price_pch_dict
    price_pch = []

    # PRICE NAME
    global price_novus_name_dict
    price_novus_name = []
    global price_auchan_name_dict
    price_auchan_name = []
    global price_varus_name_dict
    price_varus_name = []
    global price_mm_name_dict
    price_mm_name = []
    global price_metro_name_dict
    price_metro_name = []
    global price_tv_name_dict
    price_tv_name = []
    global price_um_name_dict
    price_um_name = []
    global price_eko_name_dict
    price_eko_name = []
    global price_cm_name_dict
    price_cm_name = []
    global price_vs_name_dict
    price_vs_name = []

    global price_pch_name_dict
    price_pch_name = []
    global price_ksms_name_dict
    price_ksms_name = []
    global price_stol_name_dict
    price_stol_name = []
    # PRICE NAME

    # NAME PRICE
    global name_price_auchan_dict
    name_price_auchan = 0
    global name_price_novus_dict
    name_price_novus = 0
    global name_price_varus_dict
    name_price_varus = 0
    global name_price_mm_dict
    name_price_mm = 0
    global name_price_vs_dict
    name_price_vs = 0
    global name_price_metro_dict
    name_price_metro = 0
    global name_price_um_dict
    name_price_um = 0
    global name_price_eko_dict
    name_price_eko = 0
    global name_price_cm_dict
    name_price_cm = 0
    global name_price_tv_dict
    name_price_tv = 0

    global name_price_pch_dict
    name_price_pch = 0
    global name_price_ksms_dict
    name_price_ksms = 0
    global name_price_stol_dict
    name_price_stol = 0
    # NAME PRICE

    # PODBOR NAME
    global podbor_name_auchan_dict
    podbor_name_auchan = []
    global podbor_name_novus_dict
    podbor_name_novus = []
    global podbor_name_varus_dict
    podbor_name_varus = []
    global podbor_name_mm_dict
    podbor_name_mm = []
    global podbor_name_eko_dict
    podbor_name_eko = []
    global podbor_name_cm_dict
    podbor_name_cm = []
    global podbor_name_tv_dict
    podbor_name_tv = []
    global podbor_name_um_dict
    podbor_name_um = []
    global podbor_name_metro_dict
    podbor_name_metro = []
    global podbor_name_vs_dict
    podbor_name_vs = []

    global podbor_name_ksms_dict
    podbor_name_ksms = []
    global podbor_name_pch_dict
    podbor_name_pch = []
    global podbor_name_stol_dict
    podbor_name_stol = []

    global podbor_name_auchan_novus_dict

    # PRICE STR
    global price_names
    price_names = ''

    name_list = message.text
    names_u_list_spl = name_list.split(';')
    names_u_list = []
    for nam_list in names_u_list_spl:
        if len(nam_list) > 0:
            names_u_list.append(nam_list.strip())
    names_u_list_set = set(names_u_list)
    contains_duplicates = len(names_u_list) != len(names_u_list_set)
    for num in range(len(names_u_list)):
        names_u_list[num] = names_u_list[num].replace('\n', '')
    if contains_duplicates:
        i += 1
        await message.answer('Дубликаты удалены')
        names_u_list = list(dict.fromkeys(names_u_list))
    for name_list in names_u_list:
        podbor_str_index_podbor = 0
        podbor_name_auchan_novus = []
        indx_of_name_list = names_u_list.index(name_list)

        podbor_name_novus = []
        podbor_name_auchan = []
        podbor_name_varus = []
        podbor_name_mm = []
        podbor_name_metro = []
        podbor_name_um = []
        podbor_name_cm = []
        podbor_name_eko = []
        podbor_name_tv = []
        podbor_name_vs = []

        podbor_name_ksms = []
        podbor_name_stol = []
        podbor_name_pch = []

        dba_int = 0
        dbn_int = 0
        dbv_int = 0
        dbm_int = 0
        db_cm_int = 0
        db_tv_int = 0
        db_vs_int = 0
        db_um_int = 0
        db_metro_int = 0
        db_eko_int = 0

        db_ksms_int = 0
        db_stol_int = 0
        db_pch_int = 0

        podbor_name_novus.clear()
        podbor_name_auchan.clear()
        podbor_name_varus.clear()
        podbor_name_mm.clear()
        podbor_name_vs.clear()
        podbor_name_um.clear()
        podbor_name_cm.clear()
        podbor_name_tv.clear()
        podbor_name_eko.clear()
        podbor_name_metro.clear()

        podbor_name_ksms.clear()
        podbor_name_pch.clear()
        podbor_name_stol.clear()

        print('Hello WRLD')

        # IS NOT NONE
        if dba.get_price(name_list) is not None:
            price_auchan.append(list(dba.get_price(name_list))[0])
            price_auchan_name.append(name_list)

        if dbn.get_price(name_list) is not None:
            price_novus.append(list(dbn.get_price(name_list))[0])
            price_novus_name.append(name_list)

        if dbv.get_price(name_list) is not None:
            price_varus.append(list(dbv.get_price(name_list))[0])
            price_varus_name.append(name_list)

        if dbm.get_price(name_list) is not None:
            price_mm.append(list(dbm.get_price(name_list))[0])
            price_mm_name.append(name_list)

        if db_eko.get_price(name_list) is not None:
            price_eko.append(list(db_eko.get_price(name_list))[0])
            price_eko_name.append(name_list)

        if db_tv.get_price(name_list) is not None:
            price_tv.append(list(db_tv.get_price(name_list))[0])
            price_tv_name.append(name_list)

        if db_metro.get_price(name_list) is not None:
            price_metro.append(list(db_metro.get_price(name_list))[0])
            price_metro_name.append(name_list)

        if db_cm.get_price(name_list) is not None:
            price_cm.append(list(db_cm.get_price(name_list))[0])
            price_cm_name.append(name_list)

        if db_um.get_price(name_list) is not None:
            price_um.append(list(db_um.get_price(name_list))[0])
            price_um_name.append(name_list)

        if db_vs.get_price(name_list) is not None:
            price_vs.append(list(db_vs.get_price(name_list))[0])
            price_vs_name.append(name_list)



        if db_pch.get_price(name_list) is not None:
            price_pch.append(list(db_pch.get_price(name_list))[0])
            price_pch_name.append(name_list)

        if db_ksms.get_price(name_list) is not None:
            price_ksms.append(list(db_ksms.get_price(name_list))[0])
            price_ksms_name.append(name_list)

        if db_stol.get_price(name_list) is not None:
            price_stol.append(list(db_stol.get_price(name_list))[0])
            price_stol_name.append(name_list)

        # IS NOT NONE



        # IS NONE
        if dba.get_price(name_list) is None:
            names = find_name(name_list, dba)
            dba_int = 1
            if names:
                for name in names:
                    podbor_name_auchan.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_auchan.append(podbor_name_auchan)
                price_auchan_name.append(podbor_name_auchan)
            else:
                all_names_auchan = dba.get_names()
                all_names_auchan_list = list(x for t in all_names_auchan for x in t)
                names = [sub_list for sub_list in all_names_auchan_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_auchan.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_auchan.append(podbor_name_auchan)
                    price_auchan_name.append(podbor_name_auchan)
                else:
                    price_auchan.append(0)
                    price_auchan_name.append(name_list)
                    dba_int = 0

        if dbn.get_price(name_list) is None:
            names = find_name(name_list, dbn)
            dbn_int = 1
            if names:
                for name in names:
                    podbor_name_novus.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_novus.append(podbor_name_novus)
                price_novus_name.append(podbor_name_novus)
            else:
                all_names_metro = dbn.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_novus.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_novus.append(podbor_name_novus)
                    price_novus_name.append(podbor_name_novus)
                else:
                    price_novus.append(0)
                    price_novus_name.append(name_list)
                    dbn_int = 0

        if dbm.get_price(name_list) is None:
            names = find_name(name_list, dbm)
            dbm_int = 1
            if names:
                for name in names:
                    podbor_name_mm.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_mm.append(podbor_name_mm)
                price_mm_name.append(podbor_name_mm)
            else:
                all_names_metro = dbm.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_mm.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_mm.append(podbor_name_mm)
                    price_mm_name.append(podbor_name_mm)
                else:
                    price_mm.append(0)
                    price_mm_name.append(name_list)
                    dbm_int = 0

        if dbv.get_price(name_list) is None:
            names = find_name(name_list, dbv)
            dbv_int = 1
            if names:
                for name in names:
                    podbor_name_varus.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_varus.append(podbor_name_varus)
                price_varus_name.append(podbor_name_varus)
            else:
                all_names_metro = dbv.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_varus.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_varus.append(podbor_name_varus)
                    price_varus_name.append(podbor_name_varus)
                else:
                    price_varus.append(0)
                    price_varus_name.append(name_list)
                    dbv_int = 0

        if db_eko.get_price(name_list) is None:
            names = find_name(name_list, db_eko)
            db_eko_int = 1
            if names:
                for name in names:
                    podbor_name_eko.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_eko.append(podbor_name_eko)
                price_eko_name.append(podbor_name_eko)
            else:
                all_names_metro = db_eko.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_eko.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_eko.append(podbor_name_eko)
                    price_eko_name.append(podbor_name_eko)
                else:
                    price_eko.append(0)
                    price_eko_name.append(name_list)
                    db_eko_int = 0
        if db_tv.get_price(name_list) is None:
            names = find_name(name_list, db_tv)
            db_tv_int = 1
            if names:
                for name in names:
                    podbor_name_tv.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_tv.append(podbor_name_tv)
                price_tv_name.append(podbor_name_tv)
            else:
                all_names_metro = db_tv.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_tv.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_tv.append(podbor_name_tv)
                    price_tv_name.append(podbor_name_tv)
                else:
                    price_tv.append(0)
                    price_tv_name.append(name_list)
                    db_tv_int = 0
        if db_um.get_price(name_list) is None:
            names = find_name(name_list, db_um)
            db_um_int = 1
            if names:
                for name in names:
                    podbor_name_um.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_um.append(podbor_name_um)
                price_um_name.append(podbor_name_um)
            else:
                all_names_metro = db_um.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_um.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_um.append(podbor_name_um)
                    price_um_name.append(podbor_name_um)
                else:
                    price_um.append(0)
                    price_um_name.append(name_list)
                    db_um_int = 0
        if db_cm.get_price(name_list) is None:
            names = find_name(name_list, db_cm)
            db_cm_int = 1
            if names:
                for name in names:
                    podbor_name_cm.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_cm.append(podbor_name_cm)
                price_cm_name.append(podbor_name_cm)
            else:
                all_names_metro = db_cm.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_cm.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_cm.append(podbor_name_cm)
                    price_cm_name.append(podbor_name_cm)
                else:
                    price_cm.append(0)
                    price_cm_name.append(name_list)
                    db_cm_int = 0
        if db_vs.get_price(name_list) is None:
            names = find_name(name_list, db_vs)
            db_vs_int = 1
            if names:
                for name in names:
                    podbor_name_vs.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_vs.append(podbor_name_vs)
                price_vs_name.append(podbor_name_vs)
            else:
                all_names_metro = db_vs.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_vs.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_vs.append(podbor_name_vs)
                    price_vs_name.append(podbor_name_vs)
                else:
                    price_vs.append(0)
                    price_vs_name.append(name_list)
                    db_vs_int = 0
        if db_metro.get_price(name_list) is None:
            names = find_name(name_list, db_metro)
            db_metro_int = 1
            if names:
                for name in names:
                    podbor_name_metro.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_metro.append(podbor_name_metro)
                price_metro_name.append(podbor_name_metro)
            else:
                all_names_metro = db_metro.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_metro.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_metro.append(podbor_name_metro)
                    price_metro_name.append(podbor_name_metro)
                else:
                    price_metro.append(0)
                    price_metro_name.append(name_list)
                    db_metro_int = 0



        if db_ksms.get_price(name_list) is None:
            names = find_name(name_list, db_ksms)
            db_ksms_int = 1
            if names:
                for name in names:
                    podbor_name_ksms.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_ksms.append(podbor_name_ksms)
                price_ksms_name.append(podbor_name_ksms)
            else:
                all_names_metro = db_ksms.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_ksms.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_ksms.append(podbor_name_ksms)
                    price_ksms_name.append(podbor_name_ksms)
                else:
                    price_ksms.append(0)
                    price_ksms_name.append(name_list)
                    db_ksms_int = 0
        if db_pch.get_price(name_list) is None:
            names = find_name(name_list, db_pch)
            db_pch_int = 1
            if names:
                for name in names:
                    podbor_name_pch.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_pch.append(podbor_name_pch)
                price_pch_name.append(podbor_name_pch)
            else:
                all_names_metro = db_vs.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_pch.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_pch.append(podbor_name_pch)
                    price_pch_name.append(podbor_name_pch)
                else:
                    price_pch.append(0)
                    price_pch_name.append(name_list)
                    db_pch_int = 0
        if db_stol.get_price(name_list) is None:
            names = find_name(name_list, db_stol)
            db_stol_int = 1
            if names:
                for name in names:
                    podbor_name_stol.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_stol.append(podbor_name_stol)
                price_stol_name.append(podbor_name_stol)
            else:
                all_names_metro = db_stol.get_names()
                all_names_metro_list = list(x for t in all_names_metro for x in t)
                names = [sub_list for sub_list in all_names_metro_list if
                         all(s in sub_list.lower() for s in name_list.lower().split())]
                if names:
                    for name in names:
                        podbor_name_stol.append(name)
                        podbor_name_auchan_novus.append(name)
                    podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                    price_stol.append(podbor_name_stol)
                    price_stol_name.append(podbor_name_stol)
                else:
                    price_stol.append(0)
                    price_stol_name.append(name_list)
                    db_stol_int = 0

        print(dba_int)
        print(dbn_int)
        print(db_metro_int)
        print(db_vs_int)
        print(db_tv_int)
        print(db_um_int)
        print(db_cm_int)

        # IS NONE
        inline_kb_full = InlineKeyboardMarkup(row_width=1)
        podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
        podbor_name_auchan_novus = [x for y in (
        podbor_name_auchan_novus[i:i + 9] + ['Дальше>>'] * (i < len(podbor_name_auchan_novus) - 8) for i in
        range(0, len(podbor_name_auchan_novus), 9)) for x in y]
        podbor_name_auchan_novus = [x for y in (
            podbor_name_auchan_novus[i:i + 10] + ['<<Назад'] * (i < len(podbor_name_auchan_novus) - 9) for i in
            range(0, len(podbor_name_auchan_novus), 10)) for x in y]
        podbor_name_auchan_novus = [podbor_name_auchan_novus[i:i + 11] for i in
                                    range(0, len(podbor_name_auchan_novus), 11)]
        if len(podbor_name_auchan_novus) > 0 and podbor_name_auchan_novus[0][len(podbor_name_auchan_novus[0]) - 1] == '<<Назад':
            del podbor_name_auchan_novus[0][len(podbor_name_auchan_novus[0]) - 1]
        if  len(podbor_name_auchan_novus) > 0 and  podbor_name_auchan_novus[len(podbor_name_auchan_novus) - 1][
            len(podbor_name_auchan_novus[len(podbor_name_auchan_novus) - 1]) - 1] != '<<Назад':
            podbor_name_auchan_novus[len(podbor_name_auchan_novus) - 1].append('<<Назад')
        if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1 or db_eko_int == 1 or db_vs_int == 1 or\
                db_cm_int == 1 or db_um_int == 1 or db_tv_int == 1 or db_metro_int == 1 or db_ksms_int == 1 or\
                db_pch_int == 1 or db_stol_int == 1:
            i += 1
        id_message = int(message.message_id) + i
        for name in podbor_name_auchan_novus[0]:
            product_id = ''
            podbor_str = ''
            if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1 or db_eko_int == 1 or db_vs_int == 1 or \
                    db_cm_int == 1 or db_um_int == 1 or db_tv_int == 1 or db_metro_int == 1 or db_ksms_int == 1 or \
                    db_pch_int == 1 or db_stol_int == 1:
                if dba.get_price(name) and dba_int == 1:
                    podbor_str = str(podbor_str) + 'a/' + str(price_auchan.index(podbor_name_auchan)) + ';'
                    product_id = 'a/' + str(dba.get_id(name)[0])
                if dbn.get_price(name) and dbn_int == 1:
                    podbor_str = str(podbor_str) + 'n/' + str(price_novus.index(podbor_name_novus)) + ';'
                    product_id = 'n/' + str(dbn.get_id(name)[0])
                if dbv.get_price(name) and dbv_int == 1:
                    podbor_str = str(podbor_str) + 'v/' + str(price_varus.index(podbor_name_varus)) + ';'
                    product_id = 'v/' + str(dbv.get_id(name)[0])
                if dbm.get_price(name) and dbm_int == 1:
                    podbor_str = str(podbor_str) + 'm/' + str(price_mm.index(podbor_name_mm)) + ';'
                    product_id = 'm/' + str(dbm.get_id(name)[0])

                if db_eko.get_price(name) and db_eko_int == 1:
                    podbor_str = str(podbor_str) + 'ek/' + str(price_eko.index(podbor_name_eko)) + ';'
                    product_id = 'ek/' + str(db_eko.get_id(name)[0])

                if db_metro.get_price(name) and db_metro_int == 1:
                    podbor_str = str(podbor_str) + 'mtr/' + str(price_metro.index(podbor_name_metro)) + ';'
                    product_id = 'mtr/' + str(db_metro.get_id(name)[0])
                if db_um.get_price(name) and db_um_int == 1:
                    podbor_str = str(podbor_str) + 'um/' + str(price_um.index(podbor_name_um)) + ';'
                    product_id = 'um/' + str(db_um.get_id(name)[0])

                if db_cm.get_price(name) and db_cm_int == 1:
                    podbor_str = str(podbor_str) + 'cm/' + str(price_cm.index(podbor_name_cm)) + ';'
                    product_id = 'cm/' + str(db_cm.get_id(name)[0])

                if db_tv.get_price(name) and db_tv_int == 1:
                    podbor_str = str(podbor_str) + 'tv/' + str(price_tv.index(podbor_name_tv)) + ';'
                    product_id = 'tv/' + str(db_tv.get_id(name)[0])

                if db_vs.get_price(name) and db_vs_int == 1:
                    podbor_str = str(podbor_str) + 'vs/' + str(price_vs.index(podbor_name_vs)) + ';'
                    product_id = 'vs/' + str(db_vs.get_id(name)[0])

                if db_ksms.get_price(name) and db_ksms_int == 1:
                    podbor_str = str(podbor_str) + 'ks/' + str(price_ksms.index(podbor_name_ksms)) + ';'
                    product_id = 'ks/' + str(db_ksms.get_id(name)[0])

                if db_pch.get_price(name) and db_pch_int == 1:
                    podbor_str = str(podbor_str) + 'pch/' + str(price_pch.index(podbor_name_pch)) + ';'
                    product_id = 'pch/' + str(db_pch.get_id(name)[0])

                if db_stol.get_price(name) and db_stol_int == 1:
                    podbor_str = str(podbor_str) + 'stl/' + str(price_stol.index(podbor_name_stol)) + ';'
                    product_id = 'stl/' + str(db_stol.get_id(name)[0])

                if name == 'Дальше>>':
                    podbor_str = str(podbor_str) + 'nx/' + '0' + ';'
                    product_id = 'nxt/' + str(indx_of_name_list)
                if name == '<<Назад':
                    podbor_str = str(podbor_str) + 'bf/' + '0' + ';'
                    product_id = 'bfr/' + str(indx_of_name_list)
                data = 'dbk,' + str(product_id) + ',' + str(podbor_str) + ',' + str(id_message) + ',' + str(
                    names_u_list.index(name_list))
                inline_btn = InlineKeyboardButton(name, callback_data=data)
                print('str and data:')
                print(name)

                print(data)
                inline_kb_full.add(inline_btn)
        if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1 or db_eko_int == 1 or db_vs_int == 1 or \
                db_cm_int == 1 or db_um_int == 1 or db_tv_int == 1 or db_metro_int == 1 or db_ksms_int == 1 or \
                db_pch_int == 1 or db_stol_int == 1:
            print('GJ')
            msg = await message.answer('Возможно вы имели ввиду:', reply_markup=inline_kb_full)
            asyncio.create_task(delete_message(msg, 50))
        podbor_name_auchan_novus_dict.update({'podbor_name_auchan_novus_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_auchan_novus})
        podbor_str_index_podbor_dict.update({'podbor_str_index_podbor_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_str_index_podbor})
        podbor_name_mm_dict.update({'podbor_name_mm_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_mm})
        podbor_name_varus_dict.update({'podbor_name_varus_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_varus})
        podbor_name_novus_dict.update({'podbor_name_novus_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_novus})
        podbor_name_auchan_dict.update({'podbor_name_auchan_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_auchan})
        podbor_name_eko_dict.update({'podbor_name_eko_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_eko})
        podbor_name_vs_dict.update({'podbor_name_vs_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_vs})
        podbor_name_metro_dict.update({'podbor_name_metro_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_metro})
        podbor_name_um_dict.update({'podbor_name_um_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_um})
        podbor_name_cm_dict.update({'podbor_name_cm_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_cm})
        podbor_name_tv_dict.update({'podbor_name_tv_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_tv})

        podbor_name_ksms_dict.update({'podbor_name_ksms_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_ksms})
        podbor_name_pch_dict.update({'podbor_name_pch_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_pch})
        podbor_name_stol_dict.update({'podbor_name_stol_' + str(message.from_user.id) + '_' + str(
            names_u_list.index(name_list)): podbor_name_stol})
    name_price_auchan = 0
    name_price_novus = 0
    name_price_varus = 0
    name_price_mm = 0
    name_price_vs = 0
    name_price_tv = 0
    name_price_um = 0
    name_price_cm = 0
    name_price_eko = 0
    name_price_metro = 0

    name_price_ksms = 0
    name_price_pch = 0
    name_price_stol = 0
    names_u_list_dict.update({'names_u_list_' + str(message.from_user.id): names_u_list})
    dba_int_dict.update({'dba_int_' + str(message.from_user.id): dba_int})
    dbn_int_dict.update({'dbn_int_' + str(message.from_user.id): dbn_int})
    dbv_int_dict.update({'dbv_int_' + str(message.from_user.id): dbv_int})
    dbm_int_dict.update({'dbm_int_' + str(message.from_user.id): dbm_int})
    db_tv_int_dict.update({'db_tv_int_' + str(message.from_user.id): db_tv_int})
    db_um_int_dict.update({'db_um_int_' + str(message.from_user.id): db_um_int})
    db_cm_int_dict.update({'db_cm_int_' + str(message.from_user.id): db_cm_int})
    db_vs_int_dict.update({'db_vs_int_' + str(message.from_user.id): db_vs_int})
    db_metro_int_dict.update({'db_metro_int_' + str(message.from_user.id): db_metro_int})
    db_eko_int_dict.update({'db_eko_int_' + str(message.from_user.id): db_eko_int})

    db_pch_int_dict.update({'db_pch_int_' + str(message.from_user.id): db_pch_int})
    db_stol_int_dict.update({'db_stol_int_' + str(message.from_user.id): db_stol_int})
    db_ksms_int_dict.update({'db_ksms_int_' + str(message.from_user.id): db_ksms_int})

    price_auchan_dict.update({'price_auchan_' + str(message.from_user.id): price_auchan})
    price_novus_dict.update({'price_novus_' + str(message.from_user.id): price_novus})
    price_mm_dict.update({'price_mm_' + str(message.from_user.id): price_mm})
    price_varus_dict.update({'price_varus_' + str(message.from_user.id): price_varus})
    price_tv_dict.update({'price_tv_' + str(message.from_user.id): price_tv})
    price_um_dict.update({'price_um_' + str(message.from_user.id): price_um})
    price_cm_dict.update({'price_cm_' + str(message.from_user.id): price_cm})
    price_vs_dict.update({'price_vs_' + str(message.from_user.id): price_vs})
    price_metro_dict.update({'price_metro_' + str(message.from_user.id): price_metro})
    price_eko_dict.update({'price_eko_' + str(message.from_user.id): price_eko})

    price_ksms_dict.update({'price_ksms_' + str(message.from_user.id): price_ksms})
    price_stol_dict.update({'price_stol_' + str(message.from_user.id): price_stol})
    price_pch_dict.update({'price_pch_' + str(message.from_user.id): price_pch})

    price_novus_name_dict.update({'price_novus_name_' + str(message.from_user.id): price_novus_name})
    print('NAUAUUAUAUUU')
    print(message.from_user.id)
    print()
    price_auchan_name_dict.update({'price_auchan_name_' + str(message.from_user.id): price_auchan_name})
    price_varus_name_dict.update({'price_varus_name_' + str(message.from_user.id): price_varus_name})
    price_mm_name_dict.update({'price_mm_name_' + str(message.from_user.id): price_mm_name})
    price_vs_name_dict.update({'price_vs_name_' + str(message.from_user.id): price_vs_name})
    price_tv_name_dict.update({'price_tv_name_' + str(message.from_user.id): price_tv_name})
    price_um_name_dict.update({'price_um_name_' + str(message.from_user.id): price_um_name})
    price_cm_name_dict.update({'price_cm_name_' + str(message.from_user.id): price_cm_name})
    price_metro_name_dict.update({'price_metro_name_' + str(message.from_user.id): price_metro_name})
    price_eko_name_dict.update({'price_eko_name_' + str(message.from_user.id): price_eko_name})

    price_ksms_name_dict.update({'price_ksms_name_' + str(message.from_user.id): price_ksms_name})
    price_pch_name_dict.update({'price_pch_name_' + str(message.from_user.id): price_pch_name})
    price_stol_name_dict.update({'price_stol_name_' + str(message.from_user.id): price_stol_name})

    name_price_auchan_dict.update({'name_price_auchan_' + str(message.from_user.id): name_price_auchan})
    name_price_novus_dict.update({'name_price_novus_' + str(message.from_user.id): name_price_novus})
    name_price_varus_dict.update({'name_price_varus_' + str(message.from_user.id): name_price_varus})
    name_price_mm_dict.update({'name_price_mm_' + str(message.from_user.id): name_price_mm})
    name_price_um_dict.update({'name_price_um_' + str(message.from_user.id): name_price_um})
    name_price_vs_dict.update({'name_price_vs_' + str(message.from_user.id): name_price_vs})
    name_price_tv_dict.update({'name_price_tv_' + str(message.from_user.id): name_price_tv})
    name_price_cm_dict.update({'name_price_cm_' + str(message.from_user.id): name_price_cm})
    name_price_metro_dict.update({'name_price_metro_' + str(message.from_user.id): name_price_metro})
    name_price_eko_dict.update({'name_price_eko_' + str(message.from_user.id): name_price_eko})

    name_price_pch_dict.update({'name_price_pch_' + str(message.from_user.id): name_price_pch})
    name_price_stol_dict.update({'name_price_stol_' + str(message.from_user.id): name_price_stol})
    name_price_ksms_dict.update({'name_price_ksms_' + str(message.from_user.id): name_price_ksms})

    if check_levels(price_novus) and check_levels(price_auchan) and check_levels(price_varus) and check_levels(
            price_mm) and check_levels(price_eko) and check_levels(price_metro) and check_levels(price_vs) and check_levels(
            price_cm) and check_levels(price_um) and check_levels(price_tv) and check_levels(price_stol) and\
            check_levels(price_ksms) and check_levels(price_pch):
        if price_auchan and price_novus and price_varus and price_mm and price_tv and price_eko and\
                price_metro and price_cm and price_um and price_vs and price_ksms and price_stol and price_pch:
            all_prices = []
            r = 0
            repeat = 0
            for num in range(len(price_auchan)):
                res = num - r
                all_prices_name = [int(price_auchan[res]), int(price_novus[res]), int(price_varus[res]),
                                   int(price_mm[res]), int(price_eko[res]), int(price_metro[res]),
                                   int(price_cm[res]), int(price_vs[res]), int(price_tv[res]),
                                   int(price_um[res]), int(price_ksms[res]), int(price_pch[res]), int(price_stol[res])]
                count_elements = all_prices_name.count(0)
                if int(count_elements) >= 12:
                    price_names = str(price_names) + (
                            str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                            str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                            str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                            str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
                            str(price_cm_name[res]) + " = " + str(price_cm[res]) + " [CityMarket]\r\n" +
                            str(price_tv_name[res]) + " = " + str(price_tv[res]) + " [Tavria V]\r\n" +
                            str(price_vs_name[res]) + " = " + str(price_vs[res]) + " [Vostorg]\r\n" +
                            str(price_um_name[res]) + " = " + str(price_um[res]) + " [UltraMarket]\r\n" +
                            str(price_metro_name[res]) + " = " + str(price_metro[res]) + " [Metro]\r\n" +
                            str(price_eko_name[res]) + " = " + str(price_eko[res]) + " [EkoMarket]\r\n" +
                            str(price_stol_name[res]) + " = " + str(price_stol[res]) + " [Stol]\r\n" +
                            str(price_pch_name[res]) + " = " + str(price_pch[res]) + " [Pchelka]\r\n" +
                            str(price_ksms_name[res]) + " = " + str(price_ksms[res]) + " [Kosmos]\r\n" +
                            "--------------------\r\n")
                    del price_auchan[res]
                    del price_novus[res]
                    del price_varus[res]
                    del price_mm[res]
                    del price_cm[res]
                    del price_tv[res]
                    del price_vs[res]
                    del price_um[res]
                    del price_metro[res]
                    del price_eko[res]

                    del price_ksms[res]
                    del price_stol[res]
                    del price_pch[res]

                    del price_auchan_name[res]
                    del price_novus_name[res]
                    del price_varus_name[res]
                    del price_mm_name[res]
                    del price_cm_name[res]
                    del price_tv_name[res]
                    del price_vs_name[res]
                    del price_um_name[res]
                    del price_metro_name[res]
                    del price_eko_name[res]

                    del price_ksms_name[res]
                    del price_pch_name[res]
                    del price_stol_name[res]

                    r += 1
                else:
                    price_names = str(price_names) + (
                            str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                            str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                            str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                            str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
                            str(price_cm_name[res]) + " = " + str(price_cm[res]) + " [CityMarket]\r\n" +
                            str(price_tv_name[res]) + " = " + str(price_tv[res]) + " [Tavria V]\r\n" +
                            str(price_vs_name[res]) + " = " + str(price_vs[res]) + " [Vostorg]\r\n" +
                            str(price_um_name[res]) + " = " + str(price_um[res]) + " [UltraMarket]\r\n" +
                            str(price_metro_name[res]) + " = " + str(price_metro[res]) + " [Metro]\r\n" +
                            str(price_eko_name[res]) + " = " + str(price_eko[res]) + " [EkoMarket]\r\n" +
                            str(price_stol_name[res]) + " = " + str(price_stol[res]) + " [Stol]\r\n" +
                            str(price_pch_name[res]) + " = " + str(price_pch[res]) + " [Pchelka]\r\n" +
                            str(price_ksms_name[res]) + " = " + str(price_ksms[res]) + " [Kosmos]\r\n" +
                            "--------------------\r\n")

            if 0 not in price_auchan:
                for x in range(len(price_auchan)):
                    name_price_auchan = name_price_auchan + price_auchan[x]
                all_prices.append(name_price_auchan)

            if 0 not in price_novus:
                for y in range(len(price_novus)):
                    name_price_novus = name_price_novus + price_novus[y]
                all_prices.append(name_price_novus)

            if 0 not in price_varus:
                for y in range(len(price_varus)):
                    name_price_varus = name_price_varus + price_varus[y]
                all_prices.append(name_price_varus)

            if 0 not in price_mm:
                for y in range(len(price_mm)):
                    name_price_mm = name_price_mm + price_mm[y]
                all_prices.append(name_price_mm)

            if 0 not in price_vs:
                for x in range(len(price_vs)):
                    name_price_vs = name_price_vs + price_vs[x]
                all_prices.append(name_price_vs)

            if 0 not in price_eko:
                for y in range(len(price_eko)):
                    name_price_eko = name_price_eko + price_eko[y]
                all_prices.append(name_price_eko)

            if 0 not in price_metro:
                for y in range(len(price_metro)):
                    name_price_metro = name_price_metro + price_metro[y]
                all_prices.append(name_price_metro)

            if 0 not in price_um:
                for y in range(len(price_um)):
                    name_price_um = name_price_um + price_um[y]
                all_prices.append(name_price_um)

            if 0 not in price_cm:
                for x in range(len(price_cm)):
                    name_price_cm = name_price_cm + price_cm[x]
                all_prices.append(name_price_cm)

            if 0 not in price_tv:
                for y in range(len(price_tv)):
                    name_price_tv = name_price_tv + price_tv[y]
                all_prices.append(name_price_tv)



            if 0 not in price_pch:
                for y in range(len(price_pch)):
                    name_price_pch = name_price_pch + price_pch[y]
                all_prices.append(name_price_pch)

            if 0 not in price_stol:
                for x in range(len(price_stol)):
                    name_price_stol = name_price_stol + price_stol[x]
                all_prices.append(name_price_stol)

            if 0 not in price_ksms:
                for y in range(len(price_ksms)):
                    name_price_ksms = name_price_ksms + price_ksms[y]
                all_prices.append(name_price_ksms)


            counter = dict((item, all_prices.count(item)) for item in all_prices)
            price_prices = '--------------------\r\n' + 'В сравнении участвовали такие магазины:\r\n'
            for a in all_prices:
                if a == name_price_auchan:
                    price_prices = price_prices + 'Auchan: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_novus:
                    price_prices = price_prices + 'Novus: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_varus:
                    price_prices = price_prices + 'Varus: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_mm:
                    price_prices = price_prices + 'MegaMarket: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_tv:
                    price_prices = price_prices + 'Tavria V: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_metro:
                    price_prices = price_prices + 'Metro: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_eko:
                    price_prices = price_prices + 'EkoMarket: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_cm:
                    price_prices = price_prices + 'CityMarket: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_vs:
                    price_prices = price_prices + 'Vostorg: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_um:
                    price_prices = price_prices + 'UltraMarket: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_ksms:
                    price_prices = price_prices + 'Kosmos: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_stol:
                    price_prices = price_prices + 'Stol: ' + str(truncate(a, 2)) + '\r\n'
                if a == name_price_pch:
                    price_prices = price_prices + 'Pchelka: ' + str(truncate(a, 2)) + '\r\n'
            price_prices = price_prices + '--------------------\r\n'
            for n in counter:
                if counter[n] > 1:
                    repeat = 1
                else:
                    repeat = 0
            if repeat == 0:
                min_item = min(all_prices)
                if int(name_price_auchan) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в Auchan\r\n' + str(price_prices) + str(
                            price_names))
                elif int(name_price_novus) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в Novus\r\n' + str(price_prices) + str(price_names))
                elif int(name_price_mm) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в MegaMarket\r\n' + str(price_prices) + str(
                            price_names))
                elif int(name_price_varus) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в Varus\r\n' + str(price_prices) + str(price_names))
                elif int(name_price_vs) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в Vostorg\r\n' + str(price_prices) + str(price_names))
                elif int(name_price_cm) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в CityMarket\r\n' + str(price_prices) + str(
                            price_names))
                elif int(name_price_tv) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в Tavria V\r\n' + str(price_prices) + str(price_names))
                elif int(name_price_metro) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в Metro\r\n' + str(price_prices) + str(price_names))
                elif int(name_price_um) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в UltraMarket\r\n' + str(price_prices) + str(
                            price_names))
                elif int(name_price_eko) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в EkoMarket\r\n' + str(price_prices) + str(price_names))

                elif int(name_price_ksms) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в Kosmos\r\n' + str(price_prices) + str(price_names))
                elif int(name_price_pch) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в Pchelka\r\n' + str(price_prices) + str(
                            price_names))
                elif int(name_price_stol) == int(min_item):
                    await message.answer(
                        'Выгоднее купить в Stol\r\n' + str(price_prices) + str(price_names))
            elif repeat == 1:
                repeat_list = []
                repeat_string = ''
                min_item = min(all_prices)
                if int(name_price_auchan) == int(min_item):
                    repeat_list.append('dba')
                    repeat_string = repeat_string + 'Auchan, '
                if int(name_price_novus) == int(min_item):
                    repeat_list.append('dbn')
                    repeat_string = repeat_string + 'Novus, '
                if int(name_price_mm) == int(min_item):
                    repeat_list.append('dbm')
                    repeat_string = repeat_string + 'MegaMarket, '
                if int(name_price_varus) == int(min_item):
                    repeat_list.append('dbv')
                    repeat_string = repeat_string + 'Varus, '
                if int(name_price_tv) == int(min_item):
                    repeat_list.append('db_tv')
                    repeat_string = repeat_string + 'Tavria V, '
                if int(name_price_um) == int(min_item):
                    repeat_list.append('db_um')
                    repeat_string = repeat_string + 'UltraMarket, '
                if int(name_price_vs) == int(min_item):
                    repeat_list.append('db_vs')
                    repeat_string = repeat_string + 'Vostorg, '
                if int(name_price_metro) == int(min_item):
                    repeat_list.append('db_metro')
                    repeat_string = repeat_string + 'Metro, '
                if int(name_price_cm) == int(min_item):
                    repeat_list.append('db_cm')
                    repeat_string = repeat_string + 'CityMarket, '
                if int(name_price_eko) == int(min_item):
                    repeat_list.append('db_eko')
                    repeat_string = repeat_string + 'EkoMarket, '

                if int(name_price_ksms) == int(min_item):
                    repeat_list.append('db_ksms')
                    repeat_string = repeat_string + 'Kosmos, '
                if int(name_price_stol) == int(min_item):
                    repeat_list.append('db_stol')
                    repeat_string = repeat_string + 'Stol, '
                if int(name_price_pch) == int(min_item):
                    repeat_list.append('db_pch')
                    repeat_string = repeat_string + 'Pchelka, '
                if len(repeat_list) == 4:
                    await message.answer(
                        'Цена одинаковая\r\n' + str(price_prices) + str(price_names))
                else:
                    await message.answer(
                        'Цена одинаковая в магазинах ' + str(repeat_string) + '\r\n' + str(
                            price_prices) + str(
                            price_names))


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global price_auchan_name_dict
    print(price_auchan_name_dict)
    price_auchan_name = copy.deepcopy(price_auchan_name_dict['price_auchan_name_' + str(callback_query.from_user.id)])
    global price_novus_name_dict
    price_novus_name = copy.deepcopy(price_novus_name_dict['price_novus_name_' + str(callback_query.from_user.id)])
    global price_varus_name_dict
    price_varus_name = copy.deepcopy(price_varus_name_dict['price_varus_name_' + str(callback_query.from_user.id)])
    global price_mm_name_dict
    price_mm_name = copy.deepcopy(price_mm_name_dict['price_mm_name_' + str(callback_query.from_user.id)])
    global price_eko_name_dict
    price_eko_name = copy.deepcopy(price_eko_name_dict['price_eko_name_' + str(callback_query.from_user.id)])
    global price_metro_name_dict
    price_metro_name = copy.deepcopy(price_metro_name_dict['price_metro_name_' + str(callback_query.from_user.id)])
    global price_um_name_dict
    price_um_name = copy.deepcopy(price_um_name_dict['price_um_name_' + str(callback_query.from_user.id)])
    global price_tv_name_dict
    price_tv_name = copy.deepcopy(price_tv_name_dict['price_tv_name_' + str(callback_query.from_user.id)])
    global price_vs_name_dict
    price_vs_name = copy.deepcopy(price_vs_name_dict['price_vs_name_' + str(callback_query.from_user.id)])
    global price_cm_name_dict
    price_cm_name = copy.deepcopy(price_cm_name_dict['price_cm_name_' + str(callback_query.from_user.id)])

    global price_ksms_name_dict
    price_ksms_name = copy.deepcopy(price_ksms_name_dict['price_ksms_name_' + str(callback_query.from_user.id)])
    global price_stol_name_dict
    price_stol_name = copy.deepcopy(price_stol_name_dict['price_stol_name_' + str(callback_query.from_user.id)])
    global price_pch_name_dict
    price_pch_name = copy.deepcopy(price_pch_name_dict['price_pch_name_' + str(callback_query.from_user.id)])

    global price_auchan_dict
    price_auchan = copy.deepcopy(price_auchan_dict['price_auchan_' + str(callback_query.from_user.id)])
    global price_novus_dict
    price_novus = copy.deepcopy(price_novus_dict['price_novus_' + str(callback_query.from_user.id)])
    global price_varus_dict
    price_varus = copy.deepcopy(price_varus_dict['price_varus_' + str(callback_query.from_user.id)])
    global price_mm_dict
    price_mm = copy.deepcopy(price_mm_dict['price_mm_' + str(callback_query.from_user.id)][:])
    global price_metro_dict
    price_metro = copy.deepcopy(price_metro_dict['price_metro_' + str(callback_query.from_user.id)])
    global price_eko_dict
    price_eko = copy.deepcopy(price_eko_dict['price_eko_' + str(callback_query.from_user.id)])
    global price_um_dict
    price_um = copy.deepcopy(price_um_dict['price_um_' + str(callback_query.from_user.id)][:])
    global price_tv_dict
    price_tv = copy.deepcopy(price_tv_dict['price_tv_' + str(callback_query.from_user.id)])
    global price_vs_dict
    price_vs = copy.deepcopy(price_vs_dict['price_vs_' + str(callback_query.from_user.id)])
    global price_cm_dict
    price_cm = copy.deepcopy(price_cm_dict['price_cm_' + str(callback_query.from_user.id)][:])

    global price_ksms_dict
    price_ksms = copy.deepcopy(price_ksms_dict['price_ksms_' + str(callback_query.from_user.id)])
    global price_stol_dict
    price_stol = copy.deepcopy(price_stol_dict['price_stol_' + str(callback_query.from_user.id)])
    global price_pch_dict
    price_pch = copy.deepcopy(price_pch_dict['price_pch_' + str(callback_query.from_user.id)][:])

    global name_price_auchan_dict
    name_price_auchan = copy.deepcopy(name_price_auchan_dict['name_price_auchan_' + str(callback_query.from_user.id)])
    global name_price_novus_dict
    name_price_novus = copy.deepcopy(name_price_novus_dict['name_price_novus_' + str(callback_query.from_user.id)])
    global name_price_varus_dict
    name_price_varus = copy.deepcopy(name_price_varus_dict['name_price_varus_' + str(callback_query.from_user.id)])
    global name_price_mm_dict
    name_price_mm = copy.deepcopy(name_price_mm_dict['name_price_mm_' + str(callback_query.from_user.id)])
    global name_price_eko_dict
    name_price_eko = copy.deepcopy(name_price_eko_dict['name_price_eko_' + str(callback_query.from_user.id)])
    global name_price_metro_dict
    name_price_metro = copy.deepcopy(name_price_metro_dict['name_price_metro_' + str(callback_query.from_user.id)])
    global name_price_um_dict
    name_price_um = copy.deepcopy(name_price_um_dict['name_price_um_' + str(callback_query.from_user.id)])
    global name_price_tv_dict
    name_price_tv = copy.deepcopy(name_price_tv_dict['name_price_tv_' + str(callback_query.from_user.id)])
    global name_price_vs_dict
    name_price_vs = copy.deepcopy(name_price_vs_dict['name_price_vs_' + str(callback_query.from_user.id)])
    global name_price_cm_dict
    name_price_cm = copy.deepcopy(name_price_cm_dict['name_price_cm_' + str(callback_query.from_user.id)])

    global name_price_ksms_dict
    name_price_ksms = copy.deepcopy(name_price_ksms_dict['name_price_ksms_' + str(callback_query.from_user.id)])
    global name_price_stol_dict
    name_price_stol = copy.deepcopy(name_price_stol_dict['name_price_stol_' + str(callback_query.from_user.id)])
    global name_price_pch_dict
    name_price_pch = copy.deepcopy(name_price_pch_dict['name_price_pch_' + str(callback_query.from_user.id)])

    global dba_int_dict
    dba_int = copy.deepcopy(dba_int_dict['dba_int_' + str(callback_query.from_user.id)])
    global dbn_int_dict
    dbn_int = copy.deepcopy(dbn_int_dict['dbn_int_' + str(callback_query.from_user.id)])
    global dbv_int_dict
    dbv_int = copy.deepcopy(dbv_int_dict['dbv_int_' + str(callback_query.from_user.id)])
    global dbm_int_dict
    dbm_int = copy.deepcopy(dbm_int_dict['dbm_int_' + str(callback_query.from_user.id)])
    global db_um_int_dict
    db_um_int = copy.deepcopy(db_um_int_dict['db_um_int_' + str(callback_query.from_user.id)])
    global db_cm_int_dict
    db_cm_int = copy.deepcopy(db_cm_int_dict['db_cm_int_' + str(callback_query.from_user.id)])
    global db_tv_int_dict
    db_tv_int = copy.deepcopy(db_tv_int_dict['db_tv_int_' + str(callback_query.from_user.id)])
    global db_vs_int_dict
    db_vs_int = copy.deepcopy(db_vs_int_dict['db_vs_int_' + str(callback_query.from_user.id)])
    global db_metro_int_dict
    db_metro_int = copy.deepcopy(db_metro_int_dict['db_metro_int_' + str(callback_query.from_user.id)])
    global db_eko_int_dict
    db_eko_int = copy.deepcopy(db_eko_int_dict['db_eko_int_' + str(callback_query.from_user.id)])

    global db_ksms_int_dict
    db_ksms_int = copy.deepcopy(db_ksms_int_dict['db_ksms_int_' + str(callback_query.from_user.id)])
    global db_stol_int_dict
    db_stol_int = copy.deepcopy(db_stol_int_dict['db_stol_int_' + str(callback_query.from_user.id)])
    global db_pch_int_dict
    db_pch_int = copy.deepcopy(db_pch_int_dict['db_pch_int_' + str(callback_query.from_user.id)])

    global podbor_name_auchan_dict
    global podbor_name_novus_dict
    global podbor_name_varus_dict
    global podbor_name_mm_dict
    global podbor_name_metro_dict
    global podbor_name_eko_dict
    global podbor_name_cm_dict
    global podbor_name_tv_dict
    global podbor_name_vs_dict
    global podbor_name_um_dict

    global podbor_name_ksms_dict
    global podbor_name_stol_dict
    global podbor_name_pch_dict

    global podbor_name_auchan_novus_dict

    global podbor_str_index_podbor_dict

    global price_names

    price_names = ''
    code = callback_query.data
    podbor_str_index = ''
    product_name_podbor = ''
    spl = code.split(',')
    db = spl[0]
    inline_kb = InlineKeyboardMarkup(row_width=1)
    if str(db) == 'dbk':
        product_id_before_split = spl[1]
        podbor_str_before_spl = spl[2]
        id_message = spl[3]
        product_in_list = spl[4]
        product_id_spl = product_id_before_split.split('/')
        db_podbor = product_id_spl[0]
        product_id = product_id_spl[1]
        podbor_name_auchan_novus = copy.deepcopy(podbor_name_auchan_novus_dict['podbor_name_auchan_novus_' + str(
            callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_str_index_podbor = int(copy.deepcopy(podbor_str_index_podbor_dict['podbor_str_index_podbor_' + str(
            callback_query.from_user.id) + '_' + str(product_in_list)]))
        print('just copied ')
        print(podbor_str_index_podbor)
        print(podbor_str_index_podbor_dict)

        podbor_name_mm = copy.deepcopy(
            podbor_name_mm_dict['podbor_name_mm_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_varus = copy.deepcopy(
            podbor_name_varus_dict[
                'podbor_name_varus_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_novus = copy.deepcopy(
            podbor_name_novus_dict[
                'podbor_name_novus_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_auchan = copy.deepcopy(
            podbor_name_auchan_dict[
                'podbor_name_auchan_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_cm = copy.deepcopy(
            podbor_name_cm_dict['podbor_name_cm_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_vs = copy.deepcopy(
            podbor_name_vs_dict[
                'podbor_name_vs_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_tv = copy.deepcopy(
            podbor_name_tv_dict[
                'podbor_name_tv_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_eko = copy.deepcopy(
            podbor_name_eko_dict[
                'podbor_name_eko_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_um = copy.deepcopy(
            podbor_name_um_dict['podbor_name_um_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_metro = copy.deepcopy(
            podbor_name_metro_dict[
                'podbor_name_metro_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])

        podbor_name_ksms = copy.deepcopy(
            podbor_name_ksms_dict[
                'podbor_name_ksms_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_stol = copy.deepcopy(
            podbor_name_stol_dict['podbor_name_stol_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_pch = copy.deepcopy(
            podbor_name_pch_dict[
                'podbor_name_pch_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])

        if db_podbor == 'a':
            product_name_podbor = str(dba.get_name_id(int(product_id))[0])
        elif db_podbor == 'n':
            product_name_podbor = str(dbn.get_name_id(int(product_id))[0])
        elif db_podbor == 'v':
            product_name_podbor = str(dbv.get_name_id(int(product_id))[0])
        elif db_podbor == 'm':
            product_name_podbor = str(dbm.get_name_id(int(product_id))[0])
        elif db_podbor == 'ek':
            product_name_podbor = str(db_eko.get_name_id(int(product_id))[0])
        elif db_podbor == 'vs':
            product_name_podbor = str(db_vs.get_name_id(int(product_id))[0])
        elif db_podbor == 'cm':
            product_name_podbor = str(db_cm.get_name_id(int(product_id))[0])
        elif db_podbor == 'um':
            product_name_podbor = str(db_um.get_name_id(int(product_id))[0])
        elif db_podbor == 'tv':
            product_name_podbor = str(db_tv.get_name_id(int(product_id))[0])
        elif db_podbor == 'mtr':
            product_name_podbor = str(db_metro.get_name_id(int(product_id))[0])

        elif db_podbor == 'ks':
            product_name_podbor = str(db_ksms.get_name_id(int(product_id))[0])
        elif db_podbor == 'pch':
            product_name_podbor = str(db_pch.get_name_id(int(product_id))[0])
        elif db_podbor == 'stl':
            product_name_podbor = str(db_stol.get_name_id(int(product_id))[0])

        elif db_podbor == 'nxt':
            product_name_podbor = 'NEXT BTN'
        elif db_podbor == 'bfr':
            product_name_podbor = 'PAST BTN'
        podbor_str = podbor_str_before_spl.split(';')
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=int(id_message),
                                    reply_markup=None)
        for podbor in podbor_str:
            if len(podbor) >= 1:
                print('mmmmmmmmm')
                print(podbor_name_auchan_novus)
                each_podbor_str = podbor.split('/')
                podbor_str_db = str(each_podbor_str[0])
                podbor_str_index = int(each_podbor_str[1])
                print(podbor_str_index)
                if podbor_str_db == 'a':
                    price_auchan[int(podbor_str_index)] = dba.get_price(product_name_podbor)[0]
                    price_auchan_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'n':
                    price_novus[int(podbor_str_index)] = dbn.get_price(product_name_podbor)[0]
                    price_novus_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'v':
                    price_varus[int(podbor_str_index)] = dbv.get_price(product_name_podbor)[0]
                    price_varus_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'm':
                    price_mm[int(podbor_str_index)] = dbm.get_price(product_name_podbor)[0]
                    price_mm_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'mtr':
                    price_metro[int(podbor_str_index)] = db_metro.get_price(product_name_podbor)[0]
                    price_metro_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'ek':
                    price_eko[int(podbor_str_index)] = db_eko.get_price(product_name_podbor)[0]
                    price_eko_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'um':
                    price_um[int(podbor_str_index)] = db_um.get_price(product_name_podbor)[0]
                    price_um_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'cm':
                    price_cm[int(podbor_str_index)] = db_cm.get_price(product_name_podbor)[0]
                    price_cm_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'tv':
                    price_tv[int(podbor_str_index)] = db_tv.get_price(product_name_podbor)[0]
                    price_tv_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'vs':
                    price_vs[int(podbor_str_index)] = db_vs.get_price(product_name_podbor)[0]
                    price_vs_name[int(podbor_str_index)] = str(product_name_podbor)

                elif podbor_str_db == 'ks':
                    price_ksms[int(podbor_str_index)] = db_ksms.get_price(product_name_podbor)[0]
                    price_ksms_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'pch':
                    price_pch[int(podbor_str_index)] = db_pch.get_price(product_name_podbor)[0]
                    price_pch_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'stl':
                    price_stol[int(podbor_str_index)] = db_stol.get_price(product_name_podbor)[0]
                    price_stol_name[int(podbor_str_index)] = str(product_name_podbor)
                elif podbor_str_db == 'nx':
                    podbor_str_index_podbor = podbor_str_index_podbor + 1
                    for name in podbor_name_auchan_novus[podbor_str_index_podbor]:
                        podbor_str = ''
                        if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1 or db_eko_int == 1 or db_vs_int == 1 or \
                                db_cm_int == 1 or db_um_int == 1 or db_tv_int == 1 or db_metro_int == 1 or db_ksms_int == 1 or \
                                db_pch_int == 1 or db_stol_int == 1:
                            if dba.get_price(name) and dba_int == 1:
                                podbor_str = str(podbor_str) + 'a/' + str(price_auchan.index(podbor_name_auchan)) + ';'
                                product_id = 'a/' + str(dba.get_id(name)[0])
                            if dbn.get_price(name) and dbn_int == 1:
                                podbor_str = str(podbor_str) + 'n/' + str(price_novus.index(podbor_name_novus)) + ';'
                                product_id = 'n/' + str(dbn.get_id(name)[0])
                            if dbv.get_price(name) and dbv_int == 1:
                                podbor_str = str(podbor_str) + 'v/' + str(price_varus.index(podbor_name_varus)) + ';'
                                product_id = 'v/' + str(dbv.get_id(name)[0])
                            if dbm.get_price(name) and dbm_int == 1:
                                podbor_str = str(podbor_str) + 'm/' + str(price_mm.index(podbor_name_mm)) + ';'
                                product_id = 'm/' + str(dbm.get_id(name)[0])

                            if db_eko.get_price(name) and db_eko_int == 1:
                                podbor_str = str(podbor_str) + 'ek/' + str(price_eko.index(podbor_name_eko)) + ';'
                                product_id = 'ek/' + str(db_eko.get_id(name)[0])

                            if db_metro.get_price(name) and db_metro_int == 1:
                                podbor_str = str(podbor_str) + 'mtr/' + str(price_metro.index(podbor_name_metro)) + ';'
                                product_id = 'mtr/' + str(db_metro.get_id(name)[0])
                            if db_um.get_price(name) and db_um_int == 1:
                                podbor_str = str(podbor_str) + 'um/' + str(price_um.index(podbor_name_um)) + ';'
                                product_id = 'um/' + str(db_um.get_id(name)[0])

                            if db_cm.get_price(name) and db_cm_int == 1:
                                podbor_str = str(podbor_str) + 'cm/' + str(price_cm.index(podbor_name_cm)) + ';'
                                product_id = 'cm/' + str(db_cm.get_id(name)[0])

                            if db_tv.get_price(name) and db_tv_int == 1:
                                podbor_str = str(podbor_str) + 'tv/' + str(price_tv.index(podbor_name_tv)) + ';'
                                product_id = 'tv/' + str(db_tv.get_id(name)[0])

                            if db_ksms.get_price(name) and db_ksms_int == 1:
                                podbor_str = str(podbor_str) + 'ks/' + str(price_ksms.index(podbor_name_ksms)) + ';'
                                product_id = 'ks/' + str(db_ksms.get_id(name)[0])

                            if db_pch.get_price(name) and db_pch_int == 1:
                                podbor_str = str(podbor_str) + 'pch/' + str(price_pch.index(podbor_name_pch)) + ';'
                                product_id = 'pch/' + str(db_pch.get_id(name)[0])

                            if db_stol.get_price(name) and db_stol_int == 1:
                                podbor_str = str(podbor_str) + 'stl/' + str(price_stol.index(podbor_name_stol)) + ';'
                                product_id = 'stl/' + str(db_stol.get_id(name)[0])

                            if db_vs.get_price(name) and db_vs_int == 1:
                                podbor_str = str(podbor_str) + 'vs/' + str(price_vs.index(podbor_name_vs)) + ';'
                                product_id = 'vs/' + str(db_vs.get_id(name)[0])
                            if name == 'Дальше>>':
                                podbor_str = str(podbor_str) + 'nx/' + str(podbor_str_index_podbor) + ';'
                                product_id = 'nxt/' + str(product_id)
                            if name == '<<Назад':
                                podbor_str = str(podbor_str) + 'bf/' + str(podbor_str_index_podbor) + ';'
                                product_id = 'bfr/' + str(product_id)
                            data = 'dbk,' + str(product_id) + ',' + str(podbor_str) + ',' + str(id_message) + ',' + str(
                                product_in_list)
                            inline_btn = InlineKeyboardButton(name, callback_data=data)
                            print('str and data:')
                            print(name)

                            print(data)
                            inline_kb.add(inline_btn)
                    if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1 or db_eko_int == 1 or db_vs_int == 1 or \
                            db_cm_int == 1 or db_um_int == 1 or db_tv_int == 1 or db_metro_int == 1 or db_ksms_int == 1 or \
                            db_pch_int == 1 or db_stol_int == 1:
                        msg = await bot.edit_message_text(text='Возможно вы имели ввиду:',
                                                          chat_id=callback_query.from_user.id,
                                                          message_id=int(id_message),
                                                          reply_markup=inline_kb)
                        asyncio.create_task(delete_message(msg, 50))
                elif podbor_str_db == 'bf':
                    podbor_str_index_podbor = podbor_str_index_podbor - 1
                    for name in podbor_name_auchan_novus[podbor_str_index_podbor]:
                        print('LLLLL')
                        print(podbor_name_auchan_novus[podbor_str_index_podbor])
                        podbor_str = ''
                        if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1 or db_eko_int == 1 or db_vs_int == 1 or \
                                db_cm_int == 1 or db_um_int == 1 or db_tv_int == 1 or db_metro_int == 1 or db_ksms_int == 1 or \
                                db_pch_int == 1 or db_stol_int == 1:
                            if dba.get_price(name) and dba_int == 1:
                                podbor_str = str(podbor_str) + 'a/' + str(price_auchan.index(podbor_name_auchan)) + ';'
                                product_id = 'a/' + str(dba.get_id(name)[0])
                            if dbn.get_price(name) and dbn_int == 1:
                                podbor_str = str(podbor_str) + 'n/' + str(price_novus.index(podbor_name_novus)) + ';'
                                product_id = 'n/' + str(dbn.get_id(name)[0])
                            if dbv.get_price(name) and dbv_int == 1:
                                podbor_str = str(podbor_str) + 'v/' + str(price_varus.index(podbor_name_varus)) + ';'
                                product_id = 'v/' + str(dbv.get_id(name)[0])
                            if dbm.get_price(name) and dbm_int == 1:
                                podbor_str = str(podbor_str) + 'm/' + str(price_mm.index(podbor_name_mm)) + ';'
                                product_id = 'm/' + str(dbm.get_id(name)[0])

                            if db_eko.get_price(name) and db_eko_int == 1:
                                podbor_str = str(podbor_str) + 'ek/' + str(price_eko.index(podbor_name_eko)) + ';'
                                product_id = 'ek/' + str(db_eko.get_id(name)[0])

                            if db_metro.get_price(name) and db_metro_int == 1:
                                podbor_str = str(podbor_str) + 'mtr/' + str(price_metro.index(podbor_name_metro)) + ';'
                                product_id = 'mtr/' + str(db_metro.get_id(name)[0])

                            if db_um.get_price(name) and db_um_int == 1:
                                podbor_str = str(podbor_str) + 'um/' + str(price_um.index(podbor_name_um)) + ';'
                                product_id = 'um/' + str(db_um.get_id(name)[0])

                            if db_cm.get_price(name) and db_cm_int == 1:
                                podbor_str = str(podbor_str) + 'cm/' + str(price_cm.index(podbor_name_cm)) + ';'
                                product_id = 'cm/' + str(db_cm.get_id(name)[0])

                            if db_tv.get_price(name) and db_tv_int == 1:
                                podbor_str = str(podbor_str) + 'tv/' + str(price_tv.index(podbor_name_tv)) + ';'
                                product_id = 'tv/' + str(db_tv.get_id(name)[0])

                            if db_vs.get_price(name) and db_vs_int == 1:
                                podbor_str = str(podbor_str) + 'vs/' + str(price_vs.index(podbor_name_vs)) + ';'
                                product_id = 'vs/' + str(db_vs.get_id(name)[0])

                            if db_ksms.get_price(name) and db_ksms_int == 1:
                                podbor_str = str(podbor_str) + 'ks/' + str(price_ksms.index(podbor_name_ksms)) + ';'
                                product_id = 'ks/' + str(db_ksms.get_id(name)[0])

                            if db_pch.get_price(name) and db_pch_int == 1:
                                podbor_str = str(podbor_str) + 'pch/' + str(price_pch.index(podbor_name_pch)) + ';'
                                product_id = 'pch/' + str(db_pch.get_id(name)[0])

                            if db_stol.get_price(name) and db_stol_int == 1:
                                podbor_str = str(podbor_str) + 'stl/' + str(price_stol.index(podbor_name_stol)) + ';'
                                product_id = 'stl/' + str(db_stol.get_id(name)[0])

                            if name == 'Дальше>>':
                                podbor_str = str(podbor_str) + 'nx/' + str(podbor_str_index_podbor) + ';'
                                product_id = 'nxt/' + str(product_id)
                            if name == '<<Назад':
                                podbor_str = str(podbor_str) + 'bf/' + str(podbor_str_index_podbor) + ';'
                                product_id = 'bfr/' + str(product_id)
                            data = 'dbk,' + str(product_id) + ',' + str(podbor_str) + ',' + str(id_message) + ',' + str(
                                product_in_list)
                            inline_btn = InlineKeyboardButton(name, callback_data=data)
                            print('str and data:')
                            print(name)

                            print(data)
                            inline_kb.add(inline_btn)
                    if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1 or db_eko_int == 1 or db_vs_int == 1 or \
                            db_cm_int == 1 or db_um_int == 1 or db_tv_int == 1 or db_metro_int == 1 or db_ksms_int == 1 or \
                            db_pch_int == 1 or db_stol_int == 1:
                        msg = await bot.edit_message_text(text='Возможно вы имели ввиду:',
                                                          chat_id=callback_query.from_user.id,
                                                          message_id=int(id_message),
                                                          reply_markup=inline_kb)
                        asyncio.create_task(delete_message(msg, 50))

        print(price_auchan)
        print("gjopa1")
        await fnc.check_db_dbk(dba, product_name_podbor, price_auchan, price_auchan_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'Auchan')
        await fnc.check_db_dbk(dbv, product_name_podbor, price_varus, price_varus_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'Varus')

        await fnc.check_db_dbk(dbm, product_name_podbor, price_mm, price_mm_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'MegaMarket')

        await fnc.check_db_dbk(dbn, product_name_podbor, price_novus, price_novus_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'Novus')

        await fnc.check_db_dbk(db_eko, product_name_podbor, price_eko, price_eko_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'EkoMarket')

        await fnc.check_db_dbk(db_metro, product_name_podbor, price_metro, price_metro_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'Metro')

        await fnc.check_db_dbk(db_vs, product_name_podbor, price_vs, price_vs_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'Vostorg')

        await fnc.check_db_dbk(db_tv, product_name_podbor, price_tv, price_tv_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'Tavria V')

        await fnc.check_db_dbk(db_cm, product_name_podbor, price_cm, price_cm_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'CityMarket')

        await fnc.check_db_dbk(db_um, product_name_podbor, price_um, price_um_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'UltraMarket')

        await fnc.check_db_dbk(db_ksms, product_name_podbor, price_ksms, price_ksms_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'Kosmos')

        await fnc.check_db_dbk(db_stol, product_name_podbor, price_stol, price_stol_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'Stol')

        await fnc.check_db_dbk(db_pch, product_name_podbor, price_pch, price_pch_name, podbor_str_index,
                               InlineKeyboardButton, id_message, inline_kb, bot, callback_query, 'Pchelka')

        # BILL
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)
        podbor_name_auchan_novus_dict.update(
            {'podbor_name_auchan_novus_' + str(callback_query.from_user.id) + '_' + str(
                product_in_list): podbor_name_auchan_novus})
        print('Index_podbor:')
        print(podbor_str_index_podbor)
        podbor_str_index_podbor_dict.update({'podbor_str_index_podbor_' + str(callback_query.from_user.id) + '_' + str(
            product_in_list): podbor_str_index_podbor})

        podbor_name_mm_dict.update({'podbor_name_mm_' + str(callback_query.from_user.id): podbor_name_mm})
        podbor_name_varus_dict.update({'podbor_name_varus_' + str(callback_query.from_user.id): podbor_name_varus})
        podbor_name_novus_dict.update({'podbor_name_novus_' + str(callback_query.from_user.id): podbor_name_novus})
        podbor_name_auchan_dict.update({'podbor_name_auchan_' + str(callback_query.from_user.id): podbor_name_auchan})
        podbor_name_um_dict.update({'podbor_name_um_' + str(callback_query.from_user.id): podbor_name_um})
        podbor_name_cm_dict.update({'podbor_name_cm_' + str(callback_query.from_user.id): podbor_name_cm})
        podbor_name_tv_dict.update({'podbor_name_tv_' + str(callback_query.from_user.id): podbor_name_tv})
        podbor_name_vs_dict.update({'podbor_name_vs_' + str(callback_query.from_user.id): podbor_name_vs})
        podbor_name_eko_dict.update({'podbor_name_eko_' + str(callback_query.from_user.id): podbor_name_eko})
        podbor_name_metro_dict.update({'podbor_name_metro_' + str(callback_query.from_user.id): podbor_name_metro})

        podbor_name_ksms_dict.update({'podbor_name_ksms_' + str(callback_query.from_user.id): podbor_name_ksms})
        podbor_name_stol_dict.update({'podbor_name_stol_' + str(callback_query.from_user.id): podbor_name_stol})
        podbor_name_pch_dict.update({'podbor_name_pch_' + str(callback_query.from_user.id): podbor_name_pch})
    if str(db) == 'a_n':
        id_a = int(spl[1])
        id_message = int(spl[2])
        index_a = int(spl[3])
        product_name_podbor = str(dba.get_name_id(id_a)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_auchan[int(index_a)] = dba.get_price(product_name_podbor)[0]
        price_auchan_name[int(index_a)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'n_n':
        id_n = int(spl[1])
        id_message = int(spl[2])
        index_n = int(spl[3])
        product_name_podbor = str(dbn.get_name_id(id_n)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_novus[int(index_n)] = dbn.get_price(product_name_podbor)[0]
        price_novus_name[int(index_n)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'v_n':
        id_v = int(spl[1])
        id_message = int(spl[2])
        index_v = int(spl[3])
        product_name_podbor = str(dbv.get_name_id(id_v)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_varus[int(index_v)] = dbv.get_price(product_name_podbor)[0]
        price_varus_name[int(index_v)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'm_n':
        id_m = int(spl[1])
        id_message = int(spl[2])
        index_m = int(spl[3])
        product_name_podbor = str(dbm.get_name_id(id_m)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_mm[int(index_m)] = dbm.get_price(product_name_podbor)[0]
        price_mm_name[int(index_m)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'eko_n':
        id_eko = int(spl[1])
        id_message = int(spl[2])
        index_eko = int(spl[3])
        product_name_podbor = str(db_eko.get_name_id(id_eko)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_eko[int(index_eko)] = db_eko.get_price(product_name_podbor)[0]
        price_eko_name[int(index_eko)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'metro_n':
        id_metro = int(spl[1])
        id_message = int(spl[2])
        index_metro = int(spl[3])
        product_name_podbor = str(db_metro.get_name_id(id_metro)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_metro[int(index_metro)] = db_metro.get_price(product_name_podbor)[0]
        price_metro_name[int(index_metro)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'tv_n':
        id_tv = int(spl[1])
        id_message = int(spl[2])
        index_tv = int(spl[3])
        product_name_podbor = str(db_tv.get_name_id(id_tv)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_tv[int(index_tv)] = db_tv.get_price(product_name_podbor)[0]
        price_tv_name[int(index_tv)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'vs_n':
        id_vs = int(spl[1])
        id_message = int(spl[2])
        index_vs = int(spl[3])
        product_name_podbor = str(db_vs.get_name_id(id_vs)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_vs[int(index_vs)] = db_vs.get_price(product_name_podbor)[0]
        price_vs_name[int(index_vs)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'cm_n':
        id_cm = int(spl[1])
        id_message = int(spl[2])
        index_cm = int(spl[3])
        product_name_podbor = str(db_cm.get_name_id(id_cm)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_cm[int(index_cm)] = db_cm.get_price(product_name_podbor)[0]
        price_cm_name[int(index_cm)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'um_n':
        id_um = int(spl[1])
        id_message = int(spl[2])
        index_um = int(spl[3])
        product_name_podbor = str(db_um.get_name_id(id_um)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_um[int(index_um)] = db_um.get_price(product_name_podbor)[0]
        price_um_name[int(index_um)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'ks_n':
        id_ksms = int(spl[1])
        id_message = int(spl[2])
        index_ksms = int(spl[3])
        product_name_podbor = str(db_ksms.get_name_id(id_ksms)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_ksms[int(index_ksms)] = db_ksms.get_price(product_name_podbor)[0]
        price_ksms_name[int(index_ksms)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_ksms)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'stl_n':
        id_stol = int(spl[1])
        id_message = int(spl[2])
        index_stol = int(spl[3])
        product_name_podbor = str(db_stol.get_name_id(id_stol)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_stol[int(index_stol)] = db_stol.get_price(product_name_podbor)[0]
        price_stol_name[int(index_stol)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_stol)
        print(price_eko)
        print(price_metro)
        print(price_um)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus, name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    if str(db) == 'pch_n':
        id_pch = int(spl[1])
        id_message = int(spl[2])
        index_pch = int(spl[3])
        product_name_podbor = str(db_pch.get_name_id(id_pch)[0])
        await bot.edit_message_text(text='Вы уже выбрали ' + product_name_podbor, chat_id=callback_query.from_user.id,
                                    message_id=id_message,
                                    reply_markup=None)
        price_pch[int(index_pch)] = db_pch.get_price(product_name_podbor)[0]
        price_pch_name[int(index_pch)] = str(product_name_podbor)
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        print(price_tv)
        print(price_vs)
        print(price_cm)
        print(price_eko)
        print(price_metro)
        print(price_pch)
        await fnc.bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
                       price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
                       price_auchan_name, price_novus_name, price_varus_name,
                       price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
                       price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
                       bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
                       name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus,
                       name_price_auchan,
                       name_price_ksms, name_price_stol, name_price_pch)

    dba_int_dict.update({'dba_int_' + str(callback_query.from_user.id): dba_int})
    dbn_int_dict.update({'dbn_int_' + str(callback_query.from_user.id): dbn_int})
    dbv_int_dict.update({'dbv_int_' + str(callback_query.from_user.id): dbv_int})
    dbm_int_dict.update({'dbm_int_' + str(callback_query.from_user.id): dbm_int})
    db_tv_int_dict.update({'db_tv_int_' + str(callback_query.from_user.id): db_tv_int})
    db_um_int_dict.update({'db_um_int_' + str(callback_query.from_user.id): db_um_int})
    db_cm_int_dict.update({'db_cm_int_' + str(callback_query.from_user.id): db_cm_int})
    db_vs_int_dict.update({'db_vs_int_' + str(callback_query.from_user.id): db_vs_int})
    db_eko_int_dict.update({'db_eko_int_' + str(callback_query.from_user.id): db_eko_int})
    db_metro_int_dict.update({'db_metro_int_' + str(callback_query.from_user.id): db_metro_int})

    db_ksms_int_dict.update({'db_ksms_int_' + str(callback_query.from_user.id): db_ksms_int})
    db_stol_int_dict.update({'db_stol_int_' + str(callback_query.from_user.id): db_stol_int})
    db_pch_int_dict.update({'db_pch_int_' + str(callback_query.from_user.id): db_pch_int})

    price_auchan_dict.update({'price_auchan_' + str(callback_query.from_user.id): price_auchan})
    price_novus_dict.update({'price_novus_' + str(callback_query.from_user.id): price_novus})
    price_mm_dict.update({'price_mm_' + str(callback_query.from_user.id): price_mm})
    price_varus_dict.update({'price_varus_' + str(callback_query.from_user.id): price_varus})
    price_tv_dict.update({'price_tv_' + str(callback_query.from_user.id): price_tv})
    price_cm_dict.update({'price_cm_' + str(callback_query.from_user.id): price_cm})
    price_um_dict.update({'price_um_' + str(callback_query.from_user.id): price_um})
    price_vs_dict.update({'price_vs_' + str(callback_query.from_user.id): price_vs})
    price_eko_dict.update({'price_eko_' + str(callback_query.from_user.id): price_eko})
    price_metro_dict.update({'price_metro_' + str(callback_query.from_user.id): price_metro})

    price_ksms_dict.update({'price_ksms_' + str(callback_query.from_user.id): price_ksms})
    price_stol_dict.update({'price_stol_' + str(callback_query.from_user.id): price_stol})
    price_pch_dict.update({'price_pch_' + str(callback_query.from_user.id): price_pch})

    price_novus_name_dict.update({'price_novus_name_' + str(callback_query.from_user.id): price_novus_name})
    price_auchan_name_dict.update({'price_auchan_name_' + str(callback_query.from_user.id): price_auchan_name})
    price_varus_name_dict.update({'price_varus_name_' + str(callback_query.from_user.id): price_varus_name})
    price_mm_name_dict.update({'price_mm_name_' + str(callback_query.from_user.id): price_mm_name})
    price_tv_name_dict.update({'price_tv_name_' + str(callback_query.from_user.id): price_tv_name})
    price_vs_name_dict.update({'price_vs_name_' + str(callback_query.from_user.id): price_vs_name})
    price_cm_name_dict.update({'price_cm_name_' + str(callback_query.from_user.id): price_cm_name})
    price_metro_name_dict.update({'price_metro_name_' + str(callback_query.from_user.id): price_metro_name})
    price_eko_name_dict.update({'price_eko_name_' + str(callback_query.from_user.id): price_eko_name})
    price_um_name_dict.update({'price_um_name_' + str(callback_query.from_user.id): price_um_name})

    price_stol_name_dict.update({'price_stol_name_' + str(callback_query.from_user.id): price_stol_name})
    price_pch_name_dict.update({'price_pch_name_' + str(callback_query.from_user.id): price_pch_name})
    price_ksms_name_dict.update({'price_ksms_name_' + str(callback_query.from_user.id): price_ksms_name})

    name_price_auchan_dict.update({'name_price_auchan_' + str(callback_query.from_user.id): name_price_auchan})
    name_price_novus_dict.update({'name_price_novus_' + str(callback_query.from_user.id): name_price_novus})
    name_price_varus_dict.update({'name_price_varus_' + str(callback_query.from_user.id): name_price_varus})
    name_price_mm_dict.update({'name_price_mm_' + str(callback_query.from_user.id): name_price_mm})
    name_price_tv_dict.update({'name_price_tv_' + str(callback_query.from_user.id): name_price_tv})
    name_price_vs_dict.update({'name_price_vs_' + str(callback_query.from_user.id): name_price_vs})
    name_price_cm_dict.update({'name_price_cm_' + str(callback_query.from_user.id): name_price_cm})
    name_price_eko_dict.update({'name_price_eko_' + str(callback_query.from_user.id): name_price_eko})
    name_price_metro_dict.update({'name_price_metro_' + str(callback_query.from_user.id): name_price_metro})
    name_price_um_dict.update({'name_price_um_' + str(callback_query.from_user.id): name_price_um})

    name_price_stol_dict.update({'name_price_stol_' + str(callback_query.from_user.id): name_price_stol})
    name_price_pch_dict.update({'name_price_pch_' + str(callback_query.from_user.id): name_price_pch})
    name_price_ksms_dict.update({'name_price_ksms_' + str(callback_query.from_user.id): name_price_ksms})


async def parse_all():
    await parse_mm.parse()
    await parse_novus.parse()
    await parse_auchan.parse()
    await parse_metro.parse()
    await parse_vostorg.parse()
    await parse_varus.parse()
    await parse_um.parse()
    await parse_cm.parse()
    await parse_tv.parse()
    await parse_eko.parse()
    await parse_pchelka.parse()
    await parse_kosmos.parse()
    await parse_stol.parse()


async def scheduler():
    aioschedule.every().day.at("15:40").do(parse_all)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
