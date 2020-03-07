import MySQLdb
import itertools

diml_db = MySQLdb.connect(
    host="192.168.1.231",
    user="brian",
    passwd="Nrd^730&",
    database="dimensionl"
)


class DataBase:
    column = []

    def __init__(self, database, _table=None):
        self.database = database
        self.table = _table
        self.cursor = database.cursor()
        if self.table is not None:
            self.set_table(self, _table)

    def set_table(self, table):
        self.table = table
        column_query = "SELECT *" \
                       "FROM INFORMATION_SCHEMA.COLUMNS" \
                       "--WHERE TABLE_NAME = N'" + table + ''""
        self.column = self.cursor.execute(column_query).fetchall()

    def select(self, _columns=None, _table=None, _conditions=None, redundant=False):
        if _table is not None:
            self.set_table(self, _table)

        if _columns == "*" or None:
            query_string = "SELECT * FROM " + self.table + " " + _conditions
        else:
            query_string = "SELECT " + self.column_string(_columns) + " FROM " + self.table + " " + _conditions

        return self.cursor.execute(query_string).fetchall()

    def insert(self, _values, _columns=None, _conditions=None, redundant=False):
        # Check if the data being input is a copy
        is_copy = self.select(self, _columns)
        x = ""
        if is_copy.rowcount > 0:
            for x in is_copy:
                print("Copy record found recid = " + x)
            # first column is the unique recid
            return x[0]

        # If passed values are not copies of already existing data them create the query and execute
        insert_string = self.value_logic(_values, _columns)
        if _columns == "*" or None:
            query_string = "INSERT INTO " + self.table + " (*) VALUES (" + insert_string + ") " + _conditions
        else:
            query_string = "INSERT INTO " + self.table + " (" + self.column_string(_columns) + \
                           ") " + "VALUES (" + insert_string + ") " + _conditions

        self.cursor.execute(query_string)

        return self.cursor.lastrowid

    def update(self, _values, _columns=None, _table=None, _conditions=None, redundant=False):
        update_string = []
        if _table is not None:
            self.set_table(self, _table)

        if self.subset(_values.keys, _columns):
            subset = []
            for col in _columns:
                if col in _values.keys:
                    subset.append(col)
            update_string = self.create_relation_string(_values, subset)
        else:
            update_string = self.create_relation_string(_values, columns)

        query_string = "UPDATE " + self.table + " SET (" + update_string + ") WHERE" + _conditions

        self.cursor.execute(query_string)
        return self.cursor.lastrowid

    # Function to determine how to create the value input for queries
    # If the passed list are key value pairs then it creates a string that orders it with the columns of the table
    def value_logic(self, _values, _columns):
        value_string = "'"
        if _values is None:
            return ""
        elif self.subset(_values.keys, _columns):
            subset = []
            # Create the subset list of key value pairs
            for col in _columns:
                if col in _values.keys:
                    subset.append(col)
            value_string = self.create_value_string(subset)
        else:
            value_string = self.create_value_string(_values)

        return value_string

    # Takes an array of columns and create a sql sequence of columns
    def column_string(self, _columns):
        col_string = ""
        for col in _columns:
            col_string = col_string + str(col) + ","
        col_string[:-1]
        return col_string

    def subset(self, arr1, arr2):
        for value in arr1:
            if value not in arr2:
                return False
        return True

    # Takes an array of values and converts them to string 'value1', 'value2' ... 'value3' form
    def create_value_string(self, _values):
        value_string = ""
        for value in _values:
            value_string = value_string + "'" + value + "',"
        return value_string[:-1]

    def create_relation_string(self, _values, _columns):
        relation_string = ""
        for col, value in itertools.izip(_columns, _values):
            relation_string = relation_string + " " + col + "=" + value + ","
        return relation_string[:-1]
