import sqlite3


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_to_do_table()

    def create_to_do_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
        id INTEGER Primary key,
        Title TEXT,
        Description TEXT
        _is_done boolean
        _is_deleted boolean
        CreatedOn Date DEFAULT CURRENT_DATE,
        DueDate Date,
        UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );"""
        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "User"
        id INTEGER, PRIMARY KEY, AUTO_INCREMENT
        user_name TEXT, AUTO_INCREMENT
        emial TEXT, NOT NULL
        """
        self.conn.execute(query)


class TodoModel:
    TABLENAME = 'Todo'

    def __int__(self):
        self.conn = sqlite3.connect('todo.db')

    def create(self, text, description):
        query = f'insert into {self.TABLENAME}' \
                f'(Title, Description)' \
                f'values ("{text}", "{description}")'
        result = self.conn.execute(query)
        return result

    def update(self, item_id, update_dict):
        """
        column : value
        Title : new title

        """

        set_query = "".join([f'{column} = {value}'
                            for column, value in update_dict.items()])
        query = f"UPDATE {self.TABLENAME}"\
                f"SET {set_query}"\
                f"WHERE id = {item_id}"

        self.conn.execute(query)
        return self.select()

    def delete(self, item_id):
        query = f'UPDATE{self.TABLENAME}' \
                f"SET _is_deleted = {True} " \
                f"WHERE id = {item_id}"
        self.conn.execute(query)
        return self.list_items()

    def select(self,_id):
        # couldn't name parameter as id coz of bulidin func
        where_clause = f"AND id={_id}"
        return self.list_items(where_clause)

    def list_items(self, where_clause=""):
        query = f"SELECT id, Title, Description, DueDate, _is_done " \
                f"from {self.TABLENAME} WHERE _is_deleted != {1} " + where_clause
        print (query)
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result

    def __del__(self):
        self.conn.commit()
        self.conn.close()
