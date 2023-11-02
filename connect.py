import pypyodbc  as odbc #pip install pypyodbc
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'MTN-Academy\SQLEXPRESS'
DATABASE_NAME = 'exercice_group'


#   uid=<username>
#     pwd =<password>

connection_string = f"""   
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_connection=yes;
"""

conn = odbc.connect(connection_string)
print("conn")

