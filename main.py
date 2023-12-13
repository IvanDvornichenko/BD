import psycopg2


def create_db(conn):
    """Функция, создающая структуру БД (таблицы)."""
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE telephone;
        DROP TABLE information;
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS information(
                id_information SERIAL PRIMARY KEY,
                name VARCHAR (30) NOT NULL,
                last_name VARCHAR (30) NOT NULL,
                email VARCHAR (40) NOT NULL
        );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS telephone(
                id_telephone SERIAL PRIMARY KEY,
                number VARCHAR (20),
                id_information integer not null references information(id_information)
        );
        """)
        conn.commit()


def add_client(conn, first_name, last_name, email, phones):
    """Функция, позволяющая добавить нового клиента."""
    with conn.cursor() as cur:
        vars_i = [first_name, last_name, email]
        cur.execute("""INSERT INTO information (name, last_name, email) VALUES (%s, %s, %s) RETURNING id_information""",
                    vars=vars_i)
        id_information = cur.fetchone()[0]
        if len(phones) == 0:
            vars_p = ['Нет номера', id_information]
            cur.execute(
                """INSERT INTO telephone (number, id_information) VALUES (%s, %s) """, vars=vars_p)
        elif len(phones) == 1:
            vars_p = [phones[0], id_information]
            cur.execute(
                """INSERT INTO telephone (number, id_information) VALUES (%s, %s) """, vars=vars_p)
        elif len(phones) > 1:
            for i in range(len(phones)):
                vars_p = [phones[i], id_information]
                cur.execute(
                    """INSERT INTO telephone (number, id_information) VALUES (%s, %s) """, vars=vars_p)


def add_phone(conn, client_id, phone):
    """Функция, позволяющая добавить телефон для существующего клиента."""
    with conn.cursor() as cur:
        vars_p = [phone, client_id]
        cur.execute("""INSERT INTO telephone (number, id_information) VALUES (%s, %s) """, vars=vars_p)


def change_client(conn, update_client_id, update_id_telephone, update_first_name=None, update_last_name=None,
                  update_email=None, update_phones=None):
    """Функция, позволяющая изменить данные о клиенте."""
    with conn.cursor() as cur:
        if update_first_name is not None:
            cur.execute("""UPDATE information SET name = %s WHERE id_information = %s;""",
                        (update_first_name, update_client_id))
        if update_last_name is not None:
            cur.execute("""UPDATE information SET last_name = %s WHERE id_information = %s;""",
                        (update_last_name, update_client_id))
        if update_email is not None:
            cur.execute("""UPDATE information SET email = %s WHERE id_information = %s;""",
                        (update_email, update_client_id))
        if update_phones is not None:
            cur.execute("""UPDATE telephone SET number = %s WHERE id_telephone = %s;""",
                        (update_phones, update_id_telephone))


def delete_phone(conn, delete_client_id_p):
    """Функция, позволяющая удалить телефон для существующего клиента."""
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM telephone WHERE id_information = %s;""", (delete_client_id_p,))


def delete_client(conn, delete_client_id):
    """Функция, позволяющая удалить существующего клиента."""
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM telephone WHERE id_information = %s;""", (delete_client_id,))
        cur.execute("""DELETE FROM information WHERE id_information = %s;""", (delete_client_id,))


def find_client(conn, find_name=None, find_last_name=None, find_email=None, find_number=None):
    """Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону."""
    if find_name is not None:
        with conn.cursor() as cur:
            cur.execute("""SELECT name, last_name, email, number FROM information  i
            JOIN telephone t ON i.id_information = t.id_information
            WHERE name = %s;""", (find_name,))
            print(cur.fetchall())
    if find_last_name is not None:
        with conn.cursor() as cur:
            cur.execute("""SELECT name, last_name, email, number FROM information  i
            JOIN telephone t ON i.id_information = t.id_information
            WHERE last_name = %s;""", (find_last_name,))
            print(cur.fetchall())
    if find_email is not None:
        with conn.cursor() as cur:
            cur.execute("""SELECT name, last_name, email, number FROM information  i
               JOIN telephone t ON i.id_information = t.id_information
               WHERE email = %s;""", (find_email,))
            print(cur.fetchall())
    if find_number is not None:
        with conn.cursor() as cur:
            cur.execute("""SELECT name, last_name, email, number FROM information  i
               JOIN telephone t ON i.id_information = t.id_information
               WHERE number = %s
               GROUP BY name, last_name, email, number;""", (find_number,))
            print(cur.fetchall())


# Переменные для добавления нового клиента
first_name = 'Петя'
last_name = 'Васечкин'
email = '1@mail.ru'
phones = ["422", "44444"]

# Переменные для добавления телефон для существующего клиента
client_id: int = 1
phone = "7777777"

# Переменные для изменения данных о клиенте.
update_client_id = 1
update_id_telephone = 1
update_first_name = 'Александр'   # Если параметр не нужно менять, ставим значение None.
update_last_name = 'Смирнов'   # Если параметр не нужно менять, ставим значение None.
update_email = 'opa@mail.ru'    # Если параметр не нужно менять, ставим значение None.
update_phones = "44444444"  # Если параметр не нужно менять, ставим значение None.

# Переменные для удаления телефона для существующего клиента.
delete_client_id_p = 2

# Переменные для удаления клиента.
delete_client_id = 1

# Переменная позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
find_name = 'Александр'  # Если поиск не нужен по параметру, ставим значение None.
find_last_name = 'Смирнов'  # Если поиск не нужен по параметру, ставим значение None.
find_email = 'opa@mail.ru'  # Если поиск не нужен по параметру, ставим значение None.
find_number = "422"  # Если поиск не нужен по параметру, ставим значение None.

if __name__ == "__main__":
    with psycopg2.connect(database="PostgreSQL_from_Python", user="postgres", password='suppolz3467') as conn:
        # create_db(conn)     # Функция, создающая структуру БД (таблицы)
        # add_client(conn, first_name, last_name, email, phones)    # Функция, позволяющая добавить нового клиента.
        # add_phone(conn, client_id, phone)   # Функция, позволяющая добавить телефон для существующего клиента.
        # change_client(conn, update_client_id, update_id_telephone, update_first_name, update_last_name, update_email, update_phones)  # Функция, позволяющая изменить данные о клиенте.
        # delete_phone(conn, delete_client_id_p)     # Функция, позволяющая удалить телефон для существующего клиента.
        # delete_client(conn, delete_client_id)  # Функция, позволяющая удалить существующего клиента.
        find_client(conn, find_name, find_last_name, find_email, find_number)  # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.

conn.close()
