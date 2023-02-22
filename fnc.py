
import math
import Levenshtein as lev

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


def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper


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


async def db_is_none(db, db_int, name_list, podbor_name, price, price_name, podbor_name_auchan_novus):
    if db.get_price(name_list) is None:
        names = find_name(name_list, db)
        db_int = 1
        if names:
            for name in names:
                podbor_name.append(name)
                podbor_name_auchan_novus.append(name)
            podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
            price.append(podbor_name)
            price_name.append(podbor_name)
        else:
            all_names_metro = db.get_names()
            all_names_metro_list = list(x for t in all_names_metro for x in t)
            names = [sub_list for sub_list in all_names_metro_list if
                     all(s in sub_list.lower() for s in name_list.lower().split())]
            if names:
                for name in names:
                    podbor_name.append(name)
                    podbor_name_auchan_novus.append(name)
                podbor_name_auchan_novus = list(dict.fromkeys(podbor_name_auchan_novus))
                price.append(podbor_name)
                price_name.append(podbor_name)
            else:
                price.append(0)
                price_name.append(name_list)
                db_int = 0


async def check_db_dbk(db, product_name_podbor, price, price_name, podbor_str_index, InlineKeyboardButton, id_message,
                       inline_kb, bot, callback_query, db_name):
    if db.get_price(product_name_podbor) and not check_levels(
            price) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
        price[int(podbor_str_index)] = db.get_price(product_name_podbor)[0]
        price_name[int(podbor_str_index)] = str(product_name_podbor)
    elif db.get_price(product_name_podbor) is None and not check_levels(
            price) and product_name_podbor != 'NEXT BTN' and product_name_podbor != 'PAST BTN':
        names = find_name_x(product_name_podbor, db, 30)
        if len(names) == 1:
            product_name_podbor_auchan = str(names[0])
            price[int(podbor_str_index)] = db.get_price(product_name_podbor_auchan)[0]
            price_name[int(podbor_str_index)] = str(product_name_podbor_auchan)
        elif len(names) >= 1:
            id_message = int(id_message) + 2
            for name in names:
                if db_name == 'Auchan':
                    inline_btn = InlineKeyboardButton(name, callback_data='a_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'Novus':
                    inline_btn = InlineKeyboardButton(name, callback_data='n_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'Varus':
                    inline_btn = InlineKeyboardButton(name, callback_data='v_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'MegaMarket':
                    inline_btn = InlineKeyboardButton(name, callback_data='m_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'EkoMarket':
                    inline_btn = InlineKeyboardButton(name, callback_data='eko_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'Metro':
                    inline_btn = InlineKeyboardButton(name, callback_data='metro_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'Tavria V':
                    inline_btn = InlineKeyboardButton(name, callback_data='tv_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'Vostorg':
                    inline_btn = InlineKeyboardButton(name, callback_data='vs_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'CityMarket':
                    inline_btn = InlineKeyboardButton(name, callback_data='cm_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'UltraMarket':
                    inline_btn = InlineKeyboardButton(name, callback_data='um_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                
                elif db_name == 'Kosmos':
                    inline_btn = InlineKeyboardButton(name, callback_data='ks_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'Stol':
                    inline_btn = InlineKeyboardButton(name, callback_data='stl_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
                elif db_name == 'Pchelka':
                    inline_btn = InlineKeyboardButton(name, callback_data='pch_n,' + str(db.get_id(name)[0]) + ',' + str(
                        id_message) + ',' + str(podbor_str_index))
                    inline_kb.add(inline_btn)
            await bot.send_message(text='В магазине ' + db_name + ' нет товара ' + str(product_name_podbor),
                                        chat_id=callback_query.from_user.id,
                                        reply_markup=inline_kb)
        else:
            product_name_podbor_auchan = str(product_name_podbor)
            price[int(podbor_str_index)] = 0
            price_name[int(podbor_str_index)] = str(product_name_podbor_auchan)


async def bill(price_novus, price_auchan, price_varus, price_mm, price_eko,
               price_metro, price_vs, price_cm, price_um, price_tv, price_stol, price_ksms, price_pch,
               price_auchan_name, price_novus_name, price_varus_name,
               price_cm_name, price_mm_name, price_tv_name, price_vs_name, price_um_name, price_metro_name,
               price_eko_name, price_ksms_name, price_stol_name, price_pch_name,
               bot, callback_query, price_names, name_price_novus, name_price_tv, name_price_cm, name_price_um,
               name_price_metro, name_price_eko, name_price_vs, name_price_mm, name_price_varus, name_price_auchan,
               name_price_ksms, name_price_stol, name_price_pch):
    if check_levels(price_novus) and check_levels(price_auchan) and check_levels(price_varus) and check_levels(
            price_mm) and check_levels(price_eko) and check_levels(price_metro) and check_levels(
        price_vs) and check_levels(
        price_cm) and check_levels(price_um) and check_levels(price_tv) and check_levels(price_stol) and \
            check_levels(price_ksms) and check_levels(price_pch):
        if price_auchan and price_novus and price_varus and price_mm and price_tv and price_eko and \
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
            a_a = 0
            a_n = 0
            a_v = 0
            a_mm = 0
            a_tv = 0
            a_metro = 0
            a_eko = 0
            a_cm = 0
            a_ksms = 0
            a_stol = 0
            a_um = 0
            a_vs = 0
            a_pch = 0
            price_prices = '--------------------\r\n' + 'В сравнении участвовали такие магазины:\r\n'
            print(all_prices)
            for a in all_prices:
                if a == name_price_auchan and a_a == 0:
                    price_prices = price_prices + 'Auchan: ' + str(truncate(a, 2)) + '\r\n'
                    a_a = 1
                elif a == name_price_novus and a_n == 0:
                    price_prices = price_prices + 'Novus: ' + str(truncate(a, 2)) + '\r\n'
                    a_n = 1
                elif a == name_price_varus and a_v == 0:
                    price_prices = price_prices + 'Varus: ' + str(truncate(a, 2)) + '\r\n'
                    a_v = 1
                elif a == name_price_mm and a_mm == 0:
                    price_prices = price_prices + 'MegaMarket: ' + str(truncate(a, 2)) + '\r\n'
                    a_mm = 1
                elif a == name_price_tv and a_tv == 0:
                    price_prices = price_prices + 'Tavria V: ' + str(truncate(a, 2)) + '\r\n'
                    a_tv = 1
                elif a == name_price_metro and a_metro == 0:
                    price_prices = price_prices + 'Metro: ' + str(truncate(a, 2)) + '\r\n'
                    a_metro = 1
                elif a == name_price_eko and a_eko == 0:
                    price_prices = price_prices + 'EkoMarket: ' + str(truncate(a, 2)) + '\r\n'
                    a_eko = 1
                elif a == name_price_cm and a_cm == 0:
                    price_prices = price_prices + 'CityMarket: ' + str(truncate(a, 2)) + '\r\n'
                    a_cm = 1
                elif a == name_price_vs and a_vs == 0:
                    price_prices = price_prices + 'Vostorg: ' + str(truncate(a, 2)) + '\r\n'
                    a_vs = 1
                elif a == name_price_um and a_um == 0:
                    price_prices = price_prices + 'UltraMarket: ' + str(truncate(a, 2)) + '\r\n'
                    a_um = 1
                elif a == name_price_ksms and a_ksms == 0:
                    price_prices = price_prices + 'Kosmos: ' + str(truncate(a, 2)) + '\r\n'
                    a_ksms = 1
                elif a == name_price_stol and a_stol == 0:
                    price_prices = price_prices + 'Stol: ' + str(truncate(a, 2)) + '\r\n'
                    a_stol = 1
                elif a == name_price_pch and a_pch == 0:
                    price_prices = price_prices + 'Pchelka: ' + str(truncate(a, 2)) + '\r\n'
                    a_pch = 1
            price_prices = price_prices + '--------------------\r\n'
            print(price_prices)
            for n in counter:
                if counter[n] > 1:
                    repeat = 1
                else:
                    repeat = 0
            if repeat == 0:
                min_item = min(all_prices)
                if int(name_price_auchan) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в Auchan\r\n' + str(price_prices) + str(
                            price_names), chat_id=callback_query.from_user.id)
                elif int(name_price_novus) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в Novus\r\n' + str(price_prices) + str(price_names),
                        chat_id=callback_query.from_user.id)
                elif int(name_price_mm) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в MegaMarket\r\n' + str(price_prices) + str(
                            price_names), chat_id=callback_query.from_user.id)
                elif int(name_price_varus) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в Varus\r\n' + str(price_prices) + str(price_names),
                        chat_id=callback_query.from_user.id)
                elif int(name_price_vs) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в Vostorg\r\n' + str(price_prices) + str(price_names),
                        chat_id=callback_query.from_user.id)
                elif int(name_price_cm) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в CityMarket\r\n' + str(price_prices) + str(
                            price_names), chat_id=callback_query.from_user.id)
                elif int(name_price_tv) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в Tavria V\r\n' + str(price_prices) + str(price_names),
                        chat_id=callback_query.from_user.id)
                elif int(name_price_metro) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в Metro\r\n' + str(price_prices) + str(price_names),
                        chat_id=callback_query.from_user.id)
                elif int(name_price_um) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в UltraMarket\r\n' + str(price_prices) + str(
                            price_names), chat_id=callback_query.from_user.id)
                elif int(name_price_eko) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в EkoMarket\r\n' + str(price_prices)
                        + str(price_names), chat_id=callback_query.from_user.id)

                elif int(name_price_ksms) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в Kosmos\r\n' + str(price_prices) + str(price_names), chat_id=callback_query.from_user.id)
                elif int(name_price_pch) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в Pchelka\r\n' + str(price_prices) + str(
                            price_names), chat_id=callback_query.from_user.id)
                elif int(name_price_stol) == int(min_item):
                    await bot.send_message(text=
                        'Выгоднее купить в Stol\r\n' + str(price_prices) + str(price_names), chat_id=callback_query.from_user.id)
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
                    await bot.send_message(text=
                        'Цена одинаковая\r\n' + str(price_prices) + str(price_names), chat_id=callback_query.from_user.id)
                else:
                    await bot.send_message(text=
                        'Цена одинаковая в магазинах ' + str(repeat_string) + '\r\n' + str(
                            price_prices) + str(
                            price_names), chat_id=callback_query.from_user.id)