import sqlite3
from flask import jsonify



class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_blog_table()

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def create_blog_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "Blog" (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          Username TEXT,
          Blog VARCHAR(0,200),
          _is_done boolean DEFAULT 0,
          _is_deleted boolean DEFAULT 0,
          CreatedOn Date DEFAULT CURRENT_DATE,
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """

        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "User" (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        CreatedOn Date default CURRENT_DATE
        );
        """
        self.conn.execute(query)



class BlogModel:
    TABLENAME = "Blog"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        where_clause = f"AND id={_id}"
        return self.list_items(where_clause)

    def create(self, params):
        print("IN CREATE METHOD")
        values = params.get_json()
        query = f'insert into {self.TABLENAME} ' \
                f'(Username, Blog) ' \
                f'values ("{values.get("name")}","{values.get("blog")}")'

        
        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def delete(self, item_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET _is_deleted =  {1} " \
                f"WHERE id = {item_id}"
        print (query)
        self.conn.execute(query)
        return self.list_items()

    def update(self, item_id, update_dict):
        """
        column: value
        Title: new title
        """
        set_query = ", ".join([f'{column} = "{value}"'
                     for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_query} " \
                f"WHERE id = {item_id}"
    
        self.conn.execute(query)
        return self.get_by_id(item_id)

    def list_items(self, where_clause=""):
        print(self.TABLENAME)
        query = f"SELECT id, Username, Blog " \
                f"from {self.TABLENAME}" \
                f" WHERE _is_deleted != {1} " + where_clause
        print(query)
        result_set = self.conn.execute(query).fetchall()
        print (result_set)
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


class User:
    TABLENAME = "User"

    def create(self, name):
        query = f'insert into {self.TABLENAME} ' \
                f'(Name) ' \
                f'values ({name})'
        result = self.conn.execute(query)
        return result
