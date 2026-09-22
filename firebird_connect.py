#!/usr/bin/env python3
"""
Скрипт для подключения к СУБД Firebird.
Адрес сервера: 10.20.20.6:3050
База данных: docs_kpp_test.db
"""

from firebird.driver import connect, ServerConfig
import socket


def main():
    # Конфигурация подключения
    host = "10.20.20.6"
    port = 3050
    database = "docs_kpp_test.db"
    
    # Учетные данные
    username = "FADMIN_KRS"
    password = "adminkpp"
    
    print(f"\nПопытка подключения к {host}:{port}/{database}...")
    
    # Проверка доступности порта
    print("Проверка доступности порта...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((host, port))
    sock.close()
    
    if result != 0:
        print(f"Ошибка: Порт {host}:{port} недоступен!")
        print("Возможные причины:")
        print("  - Сервер выключен или не отвечает")
        print("  - Брандмауэр блокирует соединение")
        print("  - Неверный IP-адрес")
        return
    
    print(f"Порт {host}:{port} открыт.")
    
    try:
        # Попытка подключения через ServerConfig (более явный способ)
        config = ServerConfig(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        
        print("Попытка подключения через ServerConfig...")
        with connect(config) as con:
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
        print(f"\nОшибка подключения: {type(e).__name__}: {e}")
        print("\nВозможные причины:")
        print("  - Неверное имя базы данных (путь на сервере)")
        print("  - Пользователь не имеет прав доступа к этой БД")
        print("  - База данных не зарегистрирована в aliases.conf")
        print("  - Требуется полный путь к файлу БД на сервере")


if __name__ == "__main__":
    main()
