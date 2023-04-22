import mysql.connector
from typing import Tuple, TypedDict

credentials = {
    "user": "root",
    "database": "bank",
    "password": "northkoreabestkorea"
}

connection = mysql.connector.connect(**credentials)
connection.autocommit = False

class UserSchema(TypedDict):
    id: int
    username: str
    password: str
    balance: float
    admin: int

#Execute a raw query
def execute(querytext: str, params = tuple()) -> Tuple[bool, list[tuple] | str]:
    try:
        cursor = connection.cursor()

        cursor.execute(querytext, params)

        data = [x for x in cursor]

        cursor.close()
        return (True, data)
    except Exception as err:
        cursor.close()
        return (False, err)
    
#Execute a select query
def query(querytest: str, params = tuple()) -> Tuple[bool, list[tuple] | str]:
    result = execute(querytest, params)

    #If query fails, return err as is
    #Otherwise, return structured data
    if not result[0]:
        return result
    else:
        data = [structure(x) for x in result[1]]
        if len(data) < 1:
            return (False, "No data returned")
        return (True, data)
    

#Turn tuples returned by MySQL into a dictionary
def structure(raw: tuple) -> UserSchema:
    keys = ["id", "username", "password", "balance", "admin"]

    #Assign each tupe value to a key
    dictionary = dict(
        zip(keys, list(raw))
    )

    #Replease 1/0 booleans with Python booleans
    if dictionary["admin"] == 1:
        dictionary["admin"] = True
    else:
        dictionary["admin"] = False

    return dictionary