import MySQLdb




# Make the database connection
diml_db = MySQLdb.connect(
    host="192.168.1.231",
    user="brian",
    passwd="Nrd^730&",
    database="dimensionl"
)
diml_cursor = diml_db.cursor()


# This function updates table used to connect charts to keys
# RETURNS: recid of key_lnk
def add_keychart_lnk(_recid, _group):
    esc_group = _group.replace("'", "''")
    diml_cursor.execute("SELECT t.* FROM `dimensionl`.`FC_Chart_Keys` t where ((`key_lnk` = " + str(_recid) +
                        ") AND (`Group` = '" + esc_group + "'))")

    qry_result = diml_cursor.fetchall()

    recid = 0
    if diml_cursor.rowcount > 0:
        for x in qry_result:
            recid = x[0]
    else:
        print("   '" + esc_group + "' link added.")
        diml_cursor.execute("INSERT INTO `dimensionl`.`FC_Chart_Keys` ( `key_lnk`, `Group` ) VALUES ( " +
                            str(_recid) + ", '" + esc_group + "')")
        recid = diml_cursor.lastrowid

    return recid


# This function adds keys
# RETURNS: recid of key
def add_key(key_str, array_head, key_type, key_description, key_range):
    # Look for key
    diml_cursor.execute("SELECT t.* FROM dimensionl.FC_Keys t where ((key_name = '" +
                        key_str + "') AND (array_head = '" + array_head + "'))")
    qry_result = diml_cursor.fetchall()

    x = ""
    if diml_cursor.rowcount > 0:
        for x in qry_result:
            print("   '" + key_str + "' key found. RECID = " + str(x[0]))
        # first column is the unique recid
        recid = x[0]
    else:
        esc_description = key_description.replace("'", "''")
        if key_range is None:
            esc_range = "none listed"
        else:
            # Escape quote char in this string
            esc_range = key_range.replace("'", "''")

        diml_cursor.execute("INSERT INTO FC_Keys ( key_name, array_head, type, Description, Input_range) VALUES ('" +
                            key_str +
                            "', '" + array_head +
                            "', '" + key_type +
                            "', '" + esc_description +
                            "', '" + esc_range + "')")
        recid = diml_cursor.lastrowid
        print("   key: '" + key_str + "' added. RECID: " + str(recid))

    return recid


# This function adds keys
# RETURNS: recid of key
def add_key(key_str, array_head, key_type, key_description, key_range):
    # Look for key
    diml_cursor.execute("SELECT t.* FROM dimensionl.FC_Keys t where ((key_name = '" +
                        key_str + "') AND (array_head = '" + array_head + "'))")
    qry_result = diml_cursor.fetchall()

    x = ""
    if diml_cursor.rowcount > 0:
        for x in qry_result:
            print("   '" + key_str + "' key found. RECID = " + str(x[0]))
        # first column is the unique recid
        recid = x[0]
    else:
        esc_description = key_description.replace("'", "''")
        if key_range is None:
            esc_range = "none listed"
        else:
            # Escape quote char in this string
            esc_range = key_range.replace("'", "''")

        diml_cursor.execute("INSERT INTO FC_Keys ( key_name, array_head, type, Description, Input_range) VALUES ('" +
                            key_str +
                            "', '" + array_head +
                            "', '" + key_type +
                            "', '" + esc_description +
                            "', '" + esc_range + "')")
        recid = diml_cursor.lastrowid
        print("   key: '" + key_str + "' added. RECID: " + str(recid))

    return recid


def add_type(_key_type, _name_str, _url):
    # Look for key
    diml_cursor.execute("SELECT * FROM dimensionl.FC_Type where (Type = '" +
                        _key_type + "')")
    qry_result = diml_cursor.fetchall()

    x = ""
    if diml_cursor.rowcount > 0:
        for x in qry_result:
            print("   '" + _key_type + "' key found. RECID = " + str(x[0]))
        # first column is the unique recid
        recid = x[0]
    else:
        esc_description = _name_str.replace("'", "''")
        if _name_str is None:
            esc_range = "none listed"
        else:
            # Escape quote char in this string
            esc_range = _name_str.replace("'", "''")

        diml_cursor.execute("INSERT INTO FC_Type ( Type, Name, url) VALUES ('" +
                            _key_type +
                            "', '" + _name_str +
                            "', '" + _url + "')")
        recid = diml_cursor.lastrowid
        print("   key: '" + _key_type + "' added. RECID: " + str(recid))
    diml_db.commit()
    return recid

