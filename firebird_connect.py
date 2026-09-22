#!/usr/bin/env python3
"""
Скрипт для подключения к СУБД Firebird.
Адрес сервера: 10.20.20.6:3050
База данных: docs_kpp_test.db
"""

from firebird.driver import connect, ServerConfig


def main():
    # Конфигурация подключения
    host = "10.20.20.6"
    port = 3050
    database = "docs_kpp_test.db"
    
    # Учетные данные
    username = "FADMIN_KRS"
    password = "adminkpp"
    
    # Формирование строки подключения
    # Формат: host/port:database
    dsn = f"{host}/{port}:{database}"
    
    print(f"\nПопытка подключения к {dsn}...")
    
    try:
        # Подключение к базе данных
        with connect(dsn, user=username, password=password) as con:
            print("Подключение успешно установлено!")
            
            # Получение информации о базе данных
            print(f"\nИнформация о базе данных:")
            print(f"  ODS версии: {con.ods_version}")
            print(f"  Страниц базы данных: {con.page_size}")
            print(f"  Кодировка: {con.character_set}")
            
            # Пример выполнения запроса
            cursor = con.cursor()
            
            # Попытка получить список таблиц
            query = """
                SELECT TRIM(rdb$relation_name) AS table_name
                FROM rdb$relations
                WHERE rdb$view_blr IS NULL
                  AND (rdb$system_flag IS NULL OR rdb$system_flag = 0)
                ORDER BY table_name
            """
            
            print("\nТаблицы в базе данных:")
            cursor.execute(query)
            tables = cursor.fetchall()
            
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("  Таблицы не найдены или недоступны.")
            
            cursor.close()
            
    except Exception as e:
        print(f"\nОшибка подключения: {e}")
        print("\nВозможные причины:")
        print("  - Неверный логин или пароль")
        print("  - Сервер Firebird недоступен по сети")
        print("  - База данных не существует")
        print("  - Проблемы с сетевым подключением")


if __name__ == "__main__":
    main()
