import sqlite3


class sqlight:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def delete(self):
        with self.connection:
            return self.cursor.execute('DELETE FROM `products`')

    def get_names(self):
        with self.connection:
            return self.cursor.execute('SELECT `name` FROM `products`').fetchall()

    def get_names_lower(self):
        with self.connection:
            return self.cursor.execute('SELECT `name_lower` FROM `products`').fetchall()

    def get_id(self, product_name):
        with self.connection:
            id = self.cursor.execute('SELECT `id` FROM `products` WHERE `name_lower` = ?', (product_name.lower(), )).fetchone()
            return id

    def get_name_id(self, id):
        with self.connection:
            name = self.cursor.execute('SELECT `name` FROM `products` WHERE `id` = ?', (id, )).fetchone()
            return name


    def get_price(self, product_name):
        with self.connection:
            price = self.cursor.execute('SELECT `price` FROM `products` WHERE `name_lower` = ?', (product_name.lower(), )).fetchone()
            return price



    def save_file(self, product_name, price, product_name_lower, id):
        with self.connection:
            return self.cursor.execute('INSERT INTO `products` (`name`, `price`, `name_lower`, `id`) VALUES(?,?,?,?)', (product_name, price, product_name_lower, id))


    def close(self):
        self.connection.close()
