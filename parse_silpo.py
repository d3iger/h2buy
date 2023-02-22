import config
import logging
from aiogram import Bot, Dispatcher, executor
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

# DATABASE SETUP
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
dba = sqlight(r'/Users/matviy/PycharmProjects/H2BUY/db/parse_auchan.db')
dbn = sqlight(r'/Users/matviy/PycharmProjects/H2BUY/db/parse_novus.db')
dbv = sqlight(r'/Users/matviy/PycharmProjects/H2BUY/db/parse_varus.db')
dbm = sqlight(r'/Users/matviy/PycharmProjects/H2BUY/db/parse_mm.db')
# DATABASE SETUP

# NAME LIST PRICE
name_list_price_novus_dict = {}
name_list_price_auchan_dict = {}
name_list_price_varus_dict = {}
name_list_price_mm_dict = {}
# NAME LIST PRICE

# PRICE
price_auchan_dict = {}
price_novus_dict = {}
price_varus_dict = {}
price_mm_dict = {}
# PRICE

# PRICE NAME
price_auchan_name_dict = {}
price_novus_name_dict = {}
price_varus_name_dict = {}
price_mm_name_dict = {}
# PRICE NAME

# PRICE STR
price_names = ''
# PRICE STR


name_price_auchan_dict = {}
name_price_novus_dict = {}
name_price_varus_dict = {}
name_price_mm_dict = {}

podbor_name_novus_dict = {}
podbor_name_auchan_dict = {}
podbor_name_varus_dict = {}
podbor_name_mm_dict = {}


dba_int_dict = {}
dbn_int_dict = {}
dbv_int_dict = {}
dbm_int_dict = {}

names_u_list_dict = {}

podbor_name_auchan_novus_dict = {}

podbor_str_index_podbor_dict = {}


def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper


def change(lst, sz):
    lst_r = [lst[i:i+sz] for i in range(0, len(lst), sz)]
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


# def slice_list(input, size):
#     input_size = len(input)
#     slice_size = int(input_size / size)
#     remain = int(input_size % size)
#     result = []
#     iterator = iter(input)
#     for i in range(size):
#         result.append([])
#         for j in range(slice_size):
#             result[i].append(iterator.next())
#         if remain:
#             result[i].append(iterator.next())
#             remain -= 1
#     return result


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
@dp.throttled(anti_flood, rate=10)
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

    # PRICE
    global price_auchan_dict
    price_auchan = []
    global price_novus_dict
    price_novus = []
    global price_mm_dict
    price_mm = []
    global price_varus_dict
    price_varus = []
    # PRICE NAME
    global price_novus_name_dict
    price_novus_name = []
    global price_auchan_name_dict
    price_auchan_name = []
    global price_varus_name_dict
    price_varus_name = []
    global price_mm_name_dict
    price_mm_name = []
    # NAME PRICE
    global name_price_auchan_dict
    name_price_auchan = 0
    global name_price_novus_dict
    name_price_novus = 0
    global name_price_varus_dict
    name_price_varus = 0
    global name_price_mm_dict
    name_price_mm = 0
    # PODBOR NAME
    global podbor_name_auchan_dict
    podbor_name_auchan = []
    global podbor_name_novus_dict
    podbor_name_novus = []
    global podbor_name_varus_dict
    podbor_name_varus = []
    global podbor_name_mm_dict
    podbor_name_mm = []
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

        dba_int = 0
        dbn_int = 0
        dbv_int = 0
        dbm_int = 0

        podbor_name_novus.clear()
        podbor_name_auchan.clear()
        podbor_name_varus.clear()
        podbor_name_mm.clear()

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
        # IS NOT NONE

        # IS NONE
        if dba.get_price(name_list) is None:
            dba_int = 1
            names = find_name(name_list, dba)
            if names:
                for name in names:
                    podbor_name_auchan.append(name)
                    podbor_name_auchan_novus.append(name)
                price_auchan.append(podbor_name_auchan)
                price_auchan_name.append(podbor_name_auchan)
            elif not names:
                all_names_a = dba.get_names()
                all_names_a_list = list(x for t in all_names_a for x in t)
                names = [sub_list for sub_list in all_names_a_list if
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
            dbn_int = 1
            names = find_name(name_list, dbn)
            if names:
                for name in names:
                    podbor_name_novus.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_novus.append(podbor_name_novus)
                price_novus_name.append(podbor_name_novus)
            else:
                all_names_n = dbn.get_names()
                all_names_n_list = list(x for t in all_names_n for x in t)
                names = [sub_list for sub_list in all_names_n_list if
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
            dbm_int = 1
            names = find_name(name_list, dbm)
            if names:
                for name in names:
                    podbor_name_mm.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_mm.append(podbor_name_mm)
                price_mm_name.append(podbor_name_mm)
            elif not names:
                all_names_mm = dbm.get_names()
                all_names_mm_list = list(x for t in all_names_mm for x in t)
                names = [sub_list for sub_list in all_names_mm_list if
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
            dbv_int = 1
            names = find_name(name_list, dbv)
            if names:
                for name in names:
                    podbor_name_varus.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price_varus.append(podbor_name_varus)
                price_varus_name.append(podbor_name_varus)
            else:
                all_names_v = dbv.get_names()
                all_names_v_list = list(x for t in all_names_v for x in t)
                names = [sub_list for sub_list in all_names_v_list if
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
        # IS NONE
        inline_kb_full = InlineKeyboardMarkup(row_width=1)
        podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
        podbor_name_auchan_novus = [x for y in (podbor_name_auchan_novus[i:i + 9] + ['Дальше>>'] * (i < len(podbor_name_auchan_novus) - 8) for i in range(0, len(podbor_name_auchan_novus), 9)) for x in y]
        podbor_name_auchan_novus = [x for y in (
            podbor_name_auchan_novus[i:i + 10] + ['<<Назад'] * (i < len(podbor_name_auchan_novus) - 9) for i in
            range(0, len(podbor_name_auchan_novus), 10)) for x in y]
        podbor_name_auchan_novus = [podbor_name_auchan_novus[i:i+11] for i in range(0, len(podbor_name_auchan_novus), 11)]
        if podbor_name_auchan_novus[0][len(podbor_name_auchan_novus[0]) - 1] == '<<Назад':
            del podbor_name_auchan_novus[0][len(podbor_name_auchan_novus[0]) - 1]
        if podbor_name_auchan_novus[len(podbor_name_auchan_novus) - 1][len(podbor_name_auchan_novus[len(podbor_name_auchan_novus) - 1]) - 1] != '<<Назад':
            podbor_name_auchan_novus[len(podbor_name_auchan_novus) - 1].append('<<Назад')
        if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1:
            i += 1
        id_message = int(message.message_id) + i
        for name in podbor_name_auchan_novus[0]:
            product_id = ''
            podbor_str = ''
            if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1:
                if dba.get_price(name) and dba_int == 1:
                    print('YORI')
                    print(price_auchan)
                    print(podbor_name_auchan)
                    print(str(price_auchan.index(podbor_name_auchan)))
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
                if name == 'Дальше>>':
                    podbor_str = str(podbor_str) + 'nx/' + '0' + ';'
                    product_id = 'nxt/' + str(indx_of_name_list)
                if name == '<<Назад':
                    podbor_str = str(podbor_str) + 'bf/' + '0' + ';'
                    product_id = 'bfr/' + str(indx_of_name_list)
                data = 'dbk,' + str(product_id) + ',' + str(podbor_str) + ',' + str(id_message) + ',' + str(names_u_list.index(name_list))
                inline_btn = InlineKeyboardButton(name, callback_data=data)
                print('str and data:')
                print(name)
                
                print(data)
                inline_kb_full.add(inline_btn)
        if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1:
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
    name_price_auchan = 0
    name_price_novus = 0
    name_price_varus = 0
    name_price_mm = 0
    names_u_list_dict.update({'names_u_list_' + str(message.from_user.id): names_u_list})
    dba_int_dict.update({'dba_int_' + str(message.from_user.id): dba_int})
    dbn_int_dict.update({'dbn_int_' + str(message.from_user.id): dbn_int})
    dbv_int_dict.update({'dbv_int_' + str(message.from_user.id): dbv_int})
    dbm_int_dict.update({'dbm_int_' + str(message.from_user.id): dbm_int})
    price_auchan_dict.update({'price_auchan_' + str(message.from_user.id): price_auchan})
    price_novus_dict.update({'price_novus_' + str(message.from_user.id): price_novus})
    price_mm_dict.update({'price_mm_' + str(message.from_user.id): price_mm})
    price_varus_dict.update({'price_varus_' + str(message.from_user.id): price_varus})
    price_novus_name_dict.update({'price_novus_name_' + str(message.from_user.id): price_novus_name})
    price_auchan_name_dict.update({'price_auchan_name_' + str(message.from_user.id): price_auchan_name})
    price_varus_name_dict.update({'price_varus_name_' + str(message.from_user.id): price_varus_name})
    price_mm_name_dict.update({'price_mm_name_' + str(message.from_user.id): price_mm_name})
    name_price_auchan_dict.update({'name_price_auchan_' + str(message.from_user.id): name_price_auchan})
    name_price_novus_dict.update({'name_price_novus_' + str(message.from_user.id): name_price_novus})
    name_price_varus_dict.update({'name_price_varus_' + str(message.from_user.id): name_price_varus})
    name_price_mm_dict.update({'name_price_mm_' + str(message.from_user.id): name_price_mm})

    print(price_auchan_dict)
    print('.......')
    print(price_auchan)
    if check_levels(price_novus) and check_levels(price_auchan) and check_levels(price_varus) and check_levels(
            price_mm):
        if price_auchan and price_novus and price_varus and price_mm:
            all_prices = []
            r = 0
            repeat = 0
            for num in range(len(price_auchan)):
                res = num - r
                all_prices_name = [int(price_auchan[res]), int(price_novus[res]), int(price_varus[res]),
                                   int(price_mm[res])]
                count_elements = all_prices_name.count(0)
                if int(count_elements) >= 3:
                    price_names = str(price_names) + (
                            str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                            str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                            str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                            str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
                            "--------------------\r\n")
                    del price_auchan[res]
                    del price_novus[res]
                    del price_varus[res]
                    del price_mm[res]
                    del price_auchan_name[res]
                    del price_novus_name[res]
                    del price_varus_name[res]
                    del price_mm_name[res]
                    r += 1
                else:
                    price_names = str(price_names) + (
                            str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                            str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                            str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                            str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
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
    price_auchan_name = copy.deepcopy(price_auchan_name_dict['price_auchan_name_' + str(callback_query.from_user.id)])
    global price_novus_name_dict
    price_novus_name = copy.deepcopy(price_novus_name_dict['price_novus_name_' + str(callback_query.from_user.id)])
    global price_varus_name_dict
    price_varus_name = copy.deepcopy(price_varus_name_dict['price_varus_name_' + str(callback_query.from_user.id)])
    global price_mm_name_dict
    price_mm_name = copy.deepcopy(price_mm_name_dict['price_mm_name_' + str(callback_query.from_user.id)])

    global price_auchan_dict
    print('PRICE_AUCHAN_DICT:')
    print(price_auchan_dict)
    price_auchan = copy.deepcopy(price_auchan_dict['price_auchan_' + str(callback_query.from_user.id)])
    print(price_auchan)
    global price_novus_dict
    price_novus = copy.deepcopy(price_novus_dict['price_novus_' + str(callback_query.from_user.id)])
    global price_varus_dict
    price_varus = copy.deepcopy(price_varus_dict['price_varus_' + str(callback_query.from_user.id)])
    global price_mm_dict
    price_mm = copy.deepcopy(price_mm_dict['price_mm_' + str(callback_query.from_user.id)][:])

    global name_price_auchan_dict
    name_price_auchan = copy.deepcopy(name_price_auchan_dict['name_price_auchan_' + str(callback_query.from_user.id)])
    global name_price_novus_dict
    name_price_novus = copy.deepcopy(name_price_novus_dict['name_price_novus_' + str(callback_query.from_user.id)])
    global name_price_varus_dict
    name_price_varus = copy.deepcopy(name_price_varus_dict['name_price_varus_' + str(callback_query.from_user.id)])
    global name_price_mm_dict
    name_price_mm = copy.deepcopy(name_price_mm_dict['name_price_mm_' + str(callback_query.from_user.id)])

    global dba_int_dict
    dba_int = copy.deepcopy(dba_int_dict['dba_int_' + str(callback_query.from_user.id)])
    global dbn_int_dict
    dbn_int = copy.deepcopy(dbn_int_dict['dbn_int_' + str(callback_query.from_user.id)])
    global dbv_int_dict
    dbv_int = copy.deepcopy(dbv_int_dict['dbv_int_' + str(callback_query.from_user.id)])
    global dbm_int_dict
    dbm_int = copy.deepcopy(dbm_int_dict['dbm_int_' + str(callback_query.from_user.id)])

    global podbor_name_auchan_dict

    global podbor_name_novus_dict

    global podbor_name_varus_dict

    global podbor_name_mm_dict


    global podbor_name_auchan_novus_dict

    global podbor_str_index_podbor_dict

    global price_names

    price_names = ''
    code = callback_query.data
    podbor_str_index = ''
    product_name_podbor = ''
    spl = code.split(',')
    db = spl[0]
    print('code:')
    print(code)
    inline_kb = InlineKeyboardMarkup(row_width=1)
    if str(db) == 'dbk':
        product_id_before_split = spl[1]
        podbor_str_before_spl = spl[2]
        id_message = spl[3]
        product_in_list = spl[4]
        product_id_spl = product_id_before_split.split('/')
        db_podbor = product_id_spl[0]
        product_id = product_id_spl[1]
        podbor_name_auchan_novus = copy.deepcopy(podbor_name_auchan_novus_dict['podbor_name_auchan_novus_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_str_index_podbor = int(copy.deepcopy(podbor_str_index_podbor_dict['podbor_str_index_podbor_' + str(callback_query.from_user.id) + '_' + str(product_in_list)]))
        podbor_name_mm = copy.deepcopy(podbor_name_mm_dict['podbor_name_mm_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_varus = copy.deepcopy(
            podbor_name_varus_dict['podbor_name_varus_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_novus = copy.deepcopy(
            podbor_name_novus_dict['podbor_name_novus_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        podbor_name_auchan = copy.deepcopy(
            podbor_name_auchan_dict['podbor_name_auchan_' + str(callback_query.from_user.id) + '_' + str(product_in_list)])
        if db_podbor == 'a':
            product_name_podbor = str(dba.get_name_id(int(product_id))[0])
        elif db_podbor == 'n':
            product_name_podbor = str(dbn.get_name_id(int(product_id))[0])
        elif db_podbor == 'v':
            product_name_podbor = str(dbv.get_name_id(int(product_id))[0])
        elif db_podbor == 'm':
            product_name_podbor = str(dbm.get_name_id(int(product_id))[0])
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

                elif podbor_str_db == 'nx':
                    podbor_str_index_podbor += 1
                    for name in podbor_name_auchan_novus[podbor_str_index_podbor]:
                        podbor_str = ''
                        if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1:
                            print(price_auchan)
                            if dba.get_price(name) and dba_int == 1:
                                podbor_str = str(podbor_str) + 'a/' + str(
                                    price_auchan.index(podbor_name_auchan)) + ';'
                                product_id_spl = 'a/' + str(dba.get_id(name)[0])
                            if dbn.get_price(name) and dbn_int == 1:
                                podbor_str = str(podbor_str) + 'n/' + str(
                                    price_novus.index(podbor_name_novus)) + ';'
                                product_id_spl = 'n/' + str(dbn.get_id(name)[0])
                            if dbv.get_price(name) and dbv_int == 1:
                                podbor_str = str(podbor_str) + 'v/' + str(
                                    price_varus.index(podbor_name_varus)) + ';'

                                product_id_spl = 'v/' + str(dbv.get_id(name)[0])
                            if dbm.get_price(name) and dbm_int == 1:
                                podbor_str = str(podbor_str) + 'm/' + str(price_mm.index(podbor_name_mm)) + ';'
                                product_id_spl = 'm/' + str(dbm.get_id(name)[0])
                            if name == 'Дальше>>':
                                podbor_str = str(podbor_str) + 'nx/' + str(podbor_str_index_podbor) + ';'
                                product_id_spl = 'nxt/' + str(product_id)
                            if name == '<<Назад':
                                podbor_str = str(podbor_str) + 'bf/' + str(podbor_str_index_podbor) + ';'
                                product_id_spl = 'bfr/' + str(product_id)
                            data = 'dbk,' + str(product_id_spl) + ',' + str(podbor_str) + ',' + str(id_message) + ',' + str(product_in_list)
                            inline_btn = InlineKeyboardButton(name, callback_data=data)
                            inline_kb.add(inline_btn)
                            print('data:')
                            print(data)
                    if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1:
                        msg = await bot.edit_message_text(text='Возможно вы имели ввиду:', chat_id=callback_query.from_user.id, message_id=int(id_message), reply_markup=inline_kb)
                        asyncio.create_task(delete_message(msg, 50))
                elif podbor_str_db == 'bf':
                    podbor_str_index_podbor -= 1
                    for name in podbor_name_auchan_novus[podbor_str_index_podbor]:
                        podbor_str = ''
                        if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1:
                            if dba.get_price(name) and dba_int == 1:
                                podbor_str = str(podbor_str) + 'a/' + str(
                                    price_auchan.index(podbor_name_auchan)) + ';'
                                product_id_spl = 'a/' + str(dba.get_id(name)[0])
                            if dbn.get_price(name) and dbn_int == 1:
                                podbor_str = str(podbor_str) + 'n/' + str(
                                    price_novus.index(podbor_name_novus)) + ';'
                                product_id_spl = 'n/' + str(dbn.get_id(name)[0])
                            if dbv.get_price(name) and dbv_int == 1:
                                podbor_str = str(podbor_str) + 'v/' + str(
                                    price_varus.index(podbor_name_varus)) + ';'
                                product_id_spl = 'v/' + str(dbv.get_id(name)[0])
                            if dbm.get_price(name) and dbm_int == 1:
                                podbor_str = str(podbor_str) + 'm/' + str(price_mm.index(podbor_name_mm)) + ';'
                                product_id_spl = 'm/' + str(dbm.get_id(name)[0])
                            if name == 'Дальше>>':
                                podbor_str = str(podbor_str) + 'nx/' + str(podbor_str_index_podbor) + ';'
                                product_id_spl = 'nxt/' + str(product_id)
                            if name == '<<Назад':
                                podbor_str = str(podbor_str) + 'bf/' + str(podbor_str_index_podbor) + ';'
                                product_id_spl = 'bfr/' + str(product_id)
                            data = 'dbk,' + str(product_id_spl) + ',' + str(podbor_str) + ',' + str(id_message) + ',' + str(product_in_list)
                            inline_btn = InlineKeyboardButton(name, callback_data=data)
                            inline_kb.add(inline_btn)

                    if dba_int == 1 or dbn_int == 1 or dbv_int == 1 or dbm_int == 1:
                        msg = await bot.edit_message_text(text='Возможно вы имели ввиду:',
                                                          chat_id=callback_query.from_user.id, message_id=int(id_message),
                                                          reply_markup=inline_kb)
                        asyncio.create_task(delete_message(msg, 50))

        print(price_auchan)
        print("gjopa1")
        if dba.get_price(product_name_podbor) and not check_levels(price_auchan) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
            price_auchan[int(podbor_str_index)] = dba.get_price(product_name_podbor)[0]
            price_auchan_name[int(podbor_str_index)] = str(product_name_podbor)
        elif dba.get_price(product_name_podbor) is None and not check_levels(price_auchan) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
            names = find_name_x(product_name_podbor, dba, 30)
            if len(names) == 1:
                product_name_podbor_auchan = str(names[0])
                price_auchan[int(podbor_str_index)] = dba.get_price(product_name_podbor_auchan)[0]
                price_auchan_name[int(podbor_str_index)] = str(product_name_podbor_auchan)
            elif len(names) >= 1:

                for name in names:
                    inline_btn = InlineKeyboardButton(name, callback_data='a_n,' + str(dba.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                await bot.edit_message_text(text='Уточните запрос',
                                            chat_id=callback_query.from_user.id,
                                            message_id=int(id_message),
                                            reply_markup=inline_kb)
            else:
                product_name_podbor_auchan = str(product_name_podbor)
                price_auchan[int(podbor_str_index)] = 0
                price_auchan_name[int(podbor_str_index)] = str(product_name_podbor_auchan)
        if dbv.get_price(product_name_podbor) and not check_levels(price_varus) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
            price_varus[int(podbor_str_index)] = dbv.get_price(product_name_podbor)[0]
            price_varus_name[int(podbor_str_index)] = str(product_name_podbor)
        elif dbv.get_price(product_name_podbor) is None and not check_levels(price_varus) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
            names = find_name_x(product_name_podbor, dbv, 30)
            if len(names) == 1:
                product_name_podbor_varus = str(names[0])
                price_varus[int(podbor_str_index)] = dbv.get_price(product_name_podbor_varus)[0]
                price_varus_name[int(podbor_str_index)] = str(product_name_podbor_varus)
            elif len(names) >= 1:
                for name in names:
                    inline_btn = InlineKeyboardButton(name, callback_data='v_n,' + str(dbv.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                await bot.edit_message_text(text='Уточните запрос',
                                            chat_id=callback_query.from_user.id,
                                            message_id=int(id_message),
                                            reply_markup=inline_kb)
            else:
                product_name_podbor_varus = str(product_name_podbor)
                price_varus[int(podbor_str_index)] = 0
                price_varus_name[int(podbor_str_index)] = str(product_name_podbor_varus)
        if dbm.get_price(product_name_podbor) and not check_levels(price_mm) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
            price_mm[int(podbor_str_index)] = dbm.get_price(product_name_podbor)[0]
            price_mm_name[int(podbor_str_index)] = str(product_name_podbor)
        elif dbm.get_price(product_name_podbor) is None and not check_levels(price_mm) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
            names = find_name_x(product_name_podbor, dbm, 30)
            if len(names) == 1:
                product_name_podbor_mm = str(names[0])
                price_mm[int(podbor_str_index)] = dbm.get_price(product_name_podbor_mm)[0]
                price_mm_name[int(podbor_str_index)] = str(product_name_podbor_mm)
            elif len(names) >= 1:
                for name in names:
                    inline_btn = InlineKeyboardButton(name, callback_data='m_n,' + str(dbm.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                await bot.edit_message_text(text='Уточните запрос',
                                            chat_id=callback_query.from_user.id,
                                            message_id=int(id_message),
                                            reply_markup=inline_kb)
            else:
                product_name_podbor_mm = str(product_name_podbor)
                price_mm[int(podbor_str_index)] = 0
                price_mm_name[int(podbor_str_index)] = str(product_name_podbor_mm)
        if dbn.get_price(product_name_podbor) and not check_levels(price_novus) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
            price_novus[int(podbor_str_index)] = dbn.get_price(product_name_podbor)[0]
            price_novus_name[int(podbor_str_index)] = str(product_name_podbor)
        elif dbn.get_price(product_name_podbor) is None and not check_levels(price_novus) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
            names = find_name_x(product_name_podbor, dbn, 30)
            if len(names) == 1:
                product_name_podbor_novus = str(names[0])
                price_novus[int(podbor_str_index)] = dbn.get_price(product_name_podbor_novus)[0]
                price_novus_name[int(podbor_str_index)] = str(product_name_podbor_novus)
            elif len(names) >= 1:
                inline_kb = InlineKeyboardMarkup(row_width=1)
                for name in names:
                    inline_btn = InlineKeyboardButton(name, callback_data='n_n,' + str(dbn.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                await bot.edit_message_text(text='Уточните запрос',
                                            chat_id=callback_query.from_user.id,
                                            message_id=int(id_message),
                                            reply_markup=inline_kb)
            else:
                product_name_podbor_novus = str(product_name_podbor)
                price_novus[int(podbor_str_index)] = 0
                price_novus_name[int(podbor_str_index)] = str(product_name_podbor_novus)

        # BILL
        print('BILL')
        print(price_auchan)
        print(price_novus)
        print(price_varus)
        print(price_mm)
        if check_levels(price_novus) and check_levels(price_auchan) and check_levels(price_varus) and check_levels(
                price_mm):
            if price_auchan and price_novus and price_varus and price_mm:
                print('BILL')
                print(price_auchan)
                print(price_novus)
                print(price_varus)
                print(price_mm)
                all_prices = []
                r = 0
                repeat = 0
                for num in range(len(price_auchan)):
                    res = num - r
                    all_prices_name = [int(price_auchan[res]), int(price_novus[res]), int(price_varus[res]),
                                       int(price_mm[res])]
                    count_elements = all_prices_name.count(0)
                    if int(count_elements) >= 3:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
                                "--------------------\r\n")
                        del price_auchan[res]
                        del price_novus[res]
                        del price_varus[res]
                        del price_mm[res]
                        del price_auchan_name[res]
                        del price_novus_name[res]
                        del price_varus_name[res]
                        del price_mm_name[res]
                        r += 1
                    else:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
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
                price_prices = price_prices + '--------------------\r\n'
                for n in counter:
                    if counter[n] > 1:
                        repeat = 1
                    else:
                        repeat = 0
                if repeat == 0:
                    min_item = min(all_prices)
                    if int(name_price_auchan) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Auchan\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_novus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Novus\r\n' + str(price_prices) + str(price_names))
                    elif int(name_price_mm) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в MegaMarket\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_varus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Varus\r\n' + str(price_prices) + str(price_names))
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
                    if len(repeat_list) == 4:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая\r\n' + str(price_prices) + str(price_names))
                    else:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая в магазинах ' + str(repeat_string) + '\r\n' + str(
                                                   price_prices) + str(
                                                   price_names))

        podbor_name_auchan_novus_dict.update({'podbor_name_auchan_novus_' + str(callback_query.from_user.id) + '_' + str(
            product_id): podbor_name_auchan_novus})
        podbor_str_index_podbor_dict.update({'podbor_str_index_podbor_' + str(callback_query.from_user.id) + '_' + str(
            product_id): podbor_str_index_podbor})

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
        if check_levels(price_novus) and check_levels(price_auchan) and check_levels(price_varus) and check_levels(
                price_mm):
            if price_auchan and price_novus and price_varus and price_mm:
                print('BILL')
                print(price_auchan)
                print(price_novus)
                print(price_varus)
                print(price_mm)
                all_prices = []
                r = 0
                repeat = 0
                for num in range(len(price_auchan)):
                    res = num - r
                    all_prices_name = [int(price_auchan[res]), int(price_novus[res]), int(price_varus[res]),
                                       int(price_mm[res])]
                    count_elements = all_prices_name.count(0)

                    if int(count_elements) >= 3:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
                                "--------------------\r\n")
                        del price_auchan[res]
                        del price_novus[res]
                        del price_varus[res]
                        del price_mm[res]
                        del price_auchan_name[res]
                        del price_novus_name[res]
                        del price_varus_name[res]
                        del price_mm_name[res]
                        r += 1
                    else:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
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
                price_prices = price_prices + '--------------------\r\n'
                for n in counter:
                    if counter[n] > 1:
                        repeat = 1
                    else:
                        repeat = 0
                if repeat == 0:
                    min_item = min(all_prices)
                    if int(name_price_auchan) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Auchan\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_novus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Novus\r\n' + str(price_prices) + str(price_names))
                    elif int(name_price_mm) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в MegaMarket\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_varus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Varus\r\n' + str(price_prices) + str(price_names))
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
                    if len(repeat_list) == 4:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая\r\n' + str(price_prices) + str(price_names))
                    else:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая в магазинах ' + str(repeat_string) + '\r\n' + str(
                                                   price_prices) + str(
                                                   price_names))
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
        if check_levels(price_novus) and check_levels(price_auchan) and check_levels(price_varus) and check_levels(
                price_mm):
            if price_auchan and price_novus and price_varus and price_mm:
                print('BILL')
                print(price_auchan)
                print(price_novus)
                print(price_varus)
                print(price_mm)

                all_prices = []
                r = 0
                repeat = 0
                for num in range(len(price_auchan)):
                    res = num - r
                    all_prices_name = [int(price_auchan[res]), int(price_novus[res]), int(price_varus[res]),
                                       int(price_mm[res])]
                    count_elements = all_prices_name.count(0)

                    if int(count_elements) >= 3:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
                                "--------------------\r\n")
                        del price_auchan[res]
                        del price_novus[res]
                        del price_varus[res]
                        del price_mm[res]
                        del price_auchan_name[res]
                        del price_novus_name[res]
                        del price_varus_name[res]
                        del price_mm_name[res]
                        r += 1
                    else:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
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
                price_prices = price_prices + '--------------------\r\n'
                for n in counter:
                    if counter[n] > 1:
                        repeat = 1
                    else:
                        repeat = 0
                if repeat == 0:
                    min_item = min(all_prices)
                    if int(name_price_auchan) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Auchan\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_novus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Novus\r\n' + str(price_prices) + str(price_names))
                    elif int(name_price_mm) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в MegaMarket\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_varus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Varus\r\n' + str(price_prices) + str(price_names))
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
                    if len(repeat_list) == 4:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая\r\n' + str(price_prices) + str(price_names))
                    else:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая в магазинах ' + str(repeat_string) + '\r\n' + str(
                                                   price_prices) + str(
                                                   price_names))
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
        if check_levels(price_novus) and check_levels(price_auchan) and check_levels(price_varus) and check_levels(
                price_mm):
            if price_auchan and price_novus and price_varus and price_mm:
                print('BILL')
                print(price_auchan)
                print(price_novus)
                print(price_varus)
                print(price_mm)

                all_prices = []
                r = 0
                repeat = 0
                for num in range(len(price_auchan)):
                    res = num - r
                    all_prices_name = [int(price_auchan[res]), int(price_novus[res]), int(price_varus[res]),
                                       int(price_mm[res])]
                    count_elements = all_prices_name.count(0)

                    if int(count_elements) >= 3:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
                                "--------------------\r\n")
                        del price_auchan[res]
                        del price_novus[res]
                        del price_varus[res]
                        del price_mm[res]
                        del price_auchan_name[res]
                        del price_novus_name[res]
                        del price_varus_name[res]
                        del price_mm_name[res]
                        r += 1
                    else:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
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
                price_prices = price_prices + '--------------------\r\n'
                for n in counter:
                    if counter[n] > 1:
                        repeat = 1
                    else:
                        repeat = 0
                if repeat == 0:
                    min_item = min(all_prices)
                    if int(name_price_auchan) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Auchan\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_novus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Novus\r\n' + str(price_prices) + str(price_names))
                    elif int(name_price_mm) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в MegaMarket\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_varus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Varus\r\n' + str(price_prices) + str(price_names))
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
                    if len(repeat_list) == 4:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая\r\n' + str(price_prices) + str(price_names))
                    else:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая в магазинах ' + str(repeat_string) + '\r\n' + str(
                                                   price_prices) + str(
                                                   price_names))
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
        if check_levels(price_novus) and check_levels(price_auchan) and check_levels(price_varus) and check_levels(
                price_mm):
            if price_auchan and price_novus and price_varus and price_mm:

                all_prices = []
                r = 0
                repeat = 0
                for num in range(len(price_auchan)):
                    res = num - r
                    all_prices_name = [int(price_auchan[res]), int(price_novus[res]), int(price_varus[res]),
                                       int(price_mm[res])]
                    count_elements = all_prices_name.count(0)

                    if int(count_elements) >= 3:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
                                "--------------------\r\n")
                        del price_auchan[res]
                        del price_novus[res]
                        del price_varus[res]
                        del price_mm[res]
                        del price_auchan_name[res]
                        del price_novus_name[res]
                        del price_varus_name[res]
                        del price_mm_name[res]
                        r += 1
                    else:
                        price_names = str(price_names) + (
                                str(price_auchan_name[res]) + " = " + str(price_auchan[res]) + " [Auchan]\r\n" +
                                str(price_novus_name[res]) + " = " + str(price_novus[res]) + " [Novus]\r\n" +
                                str(price_varus_name[res]) + " = " + str(price_varus[res]) + " [Varus]\r\n" +
                                str(price_mm_name[res]) + " = " + str(price_mm[res]) + " [MegaMarket]\r\n" +
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
                price_prices = price_prices + '--------------------\r\n'
                for n in counter:
                    if counter[n] > 1:
                        repeat = 1
                    else:
                        repeat = 0
                if repeat == 0:
                    min_item = min(all_prices)
                    if int(name_price_auchan) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Auchan\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_novus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Novus\r\n' + str(price_prices) + str(price_names))
                    elif int(name_price_mm) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в MegaMarket\r\n' + str(price_prices) + str(
                                                   price_names))
                    elif int(name_price_varus) == int(min_item):
                        await bot.send_message(callback_query.from_user.id,
                                               'Выгоднее купить в Varus\r\n' + str(price_prices) + str(price_names))
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
                    if len(repeat_list) == 4:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая\r\n' + str(price_prices) + str(price_names))
                    else:
                        await bot.send_message(callback_query.from_user.id,
                                               'Цена одинаковая в магазинах ' + str(repeat_string) + '\r\n' + str(
                                                   price_prices) + str(
                                                   price_names))
    dba_int_dict.update({'dba_int_' + str(callback_query.from_user.id): dba_int})
    dbn_int_dict.update({'dbn_int_' + str(callback_query.from_user.id): dbn_int})
    dbv_int_dict.update({'dbv_int_' + str(callback_query.from_user.id): dbv_int})
    dbm_int_dict.update({'dbm_int_' + str(callback_query.from_user.id): dbm_int})
    price_auchan_dict.update({'price_auchan_' + str(callback_query.from_user.id): price_auchan})
    price_novus_dict.update({'price_novus_' + str(callback_query.from_user.id): price_novus})
    price_mm_dict.update({'price_mm_' + str(callback_query.from_user.id): price_mm})
    price_varus_dict.update({'price_varus_' + str(callback_query.from_user.id): price_varus})
    price_novus_name_dict.update({'price_novus_name_' + str(callback_query.from_user.id): price_novus_name})
    price_auchan_name_dict.update({'price_auchan_name_' + str(callback_query.from_user.id): price_auchan_name})
    price_varus_name_dict.update({'price_varus_name_' + str(callback_query.from_user.id): price_varus_name})
    price_mm_name_dict.update({'price_mm_name_' + str(callback_query.from_user.id): price_mm_name})
    name_price_auchan_dict.update({'name_price_auchan_' + str(callback_query.from_user.id): name_price_auchan})
    name_price_novus_dict.update({'name_price_novus_' + str(callback_query.from_user.id): name_price_novus})
    name_price_varus_dict.update({'name_price_varus_' + str(callback_query.from_user.id): name_price_varus})
    name_price_mm_dict.update({'name_price_mm_' + str(callback_query.from_user.id): name_price_mm})
    podbor_name_mm_dict.update({'podbor_name_mm_' + str(callback_query.from_user.id): podbor_name_mm})
    podbor_name_varus_dict.update({'podbor_name_varus_' + str(callback_query.from_user.id): podbor_name_varus})
    podbor_name_novus_dict.update({'podbor_name_novus_' + str(callback_query.from_user.id): podbor_name_novus})
    podbor_name_auchan_dict.update({'podbor_name_auchan_' + str(callback_query.from_user.id): podbor_name_auchan})


if __name__ == '__main__':
    executor.start_polling(dp)
