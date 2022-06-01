import sqlite3


class User:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def all_user(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM user WHERE "id" = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO user ('id') VALUES(?)", (user_id,))

    def lenuser(self):
        """Считам сколько людей заходило в бота"""
        with self.connection:
            result = self.cursor.execute("SELECT id FROM `user`;").fetchall()
            return len(result)

    def len_sub_user(self):
        """Считам сколько активный подписок"""
        with self.connection:
            result = self.cursor.execute("SELECT id FROM `sub`;").fetchall()
            return len(result)

    def id_user(self):
        """Получаем id юзеров"""
        with self.connection:
            result = self.cursor.execute("SELECT id FROM `user`;").fetchall()
            return result

    def add_sub(self, user_id, photo):
        """Добавляем id подписчика и скрин оплаты"""
        with self.connection:
            return self.cursor.execute("INSERT INTO manager ('id', 'photo') VALUES(?, ?)", (user_id, photo))

    def photo_sub(self):
        """Получаем id юзеров и фото"""
        with self.connection:
            result = self.cursor.execute('SELECT id, photo FROM manager LIMIT 1').fetchall()
            return result

    def lenrec(self):
        with self.connection:
            result = self.cursor.execute('SELECT id FROM manager').fetchall()
            return result

    def del_sub(self, photo):
        """Удаляем id подписчика и скрин оплаты"""
        with self.connection:
            return self.cursor.execute("DELETE FROM manager WHERE photo ==?", (photo,))


    def add_subuser(self, user_id):
        """Добавляем id подписчика и срок подписки"""
        with self.connection:
            return self.cursor.execute("INSERT INTO sub ('id', 'date_buy', 'date_2day', date_del) VALUES(?,date('now'),date('now','28 days'),date('now','30 days'))", (user_id,))

    def all_subuser(self, user_id):
        """Проверяем, есть ли уже подписчик в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM sub WHERE "id" = ?', (user_id,)).fetchall()
            return bool(len(result))



    def update_subusers(self, user_id):
        """Обнавляем  подписчика"""
        with self.connection:
            return self.cursor.execute("UPDATE sub SET date_del = date(date_del,'30 days'),date_2day = date(date_2day, '28 days') WHERE id = ?", (user_id,))



    def status_sub(self,user_id):
        """Проверка подписки"""
        with self.connection:
            return self.cursor.execute("SELECT date_del FROM sub WHERE id = ?",(user_id,)).fetchall()


    def buy_user_check(self, user_id):
        """Проверяем, отправлял ли человек скрин"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM manager WHERE "id" = ?', (user_id,)).fetchall()
            return bool(len(result))


    def id_sub_user(self):
        """Получаем id активных подписчиков"""
        with self.connection:
            result = self.cursor.execute("SELECT id FROM `sub`;").fetchall()
            return result


    def two_day(self):
        """Получаем id подписчиков осталось 2 дня"""
        with self.connection:
            result = self.cursor.execute("SELECT id FROM `sub` WHERE date_2day = date('now')").fetchall()
            return result


    def all_finish(self):
        """Получаем id подписчиков у кого кончилась подписка"""
        with self.connection:
            result = self.cursor.execute("SELECT id FROM `sub` WHERE date_del = date('now')").fetchall()
            return result

    def del_day_sub(self):
        """Получаем id подписчиков осталось 2 дня"""
        with self.connection:
            result = self.cursor.execute("DELETE  FROM `sub` WHERE date_del == date('now')")
            return result


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()