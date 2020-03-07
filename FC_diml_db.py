import MySQLdb.connector

diml_db = MySQLdb.connector.connect(
    host="192.168.1.231",
    user="brian",
    passwd="Nrd^730&",
    database="dimensionl"
)

diml_cursor = diml_db.cursor()

key_str = 'caption'
array_head = 'chart'
key_type = 'chart'
key_description = 'key description'
key_range = 'range'

diml_cursor.execute("SELECT t.* FROM dimensionl.FC_Keys t where ((key_name = '" +
                    key_str + "') AND (array_head = '" + array_head + "'))")

qry_result = diml_cursor.fetchall()

recid = 0
x = ""
if diml_cursor.rowcount > 0:
    for x in qry_result:
        print("\nKey found. RECID = "+str(x[0]))
    recid = x[0]
# else:
#     diml_cursor.execute("INSERT INTO FC_Keys ( key_name, array_head, type, Description, Input_range) VALUES ('" +
#                         key_str +
#                         "', '" + array_head +
#                         "', '" + key_type +
#                         "', '" + key_description +
#                         "', '" + key_range + "')")
#     diml_db.commit()
#     print("\nKey: '"+key_str+"' added.")
