import db

#Register a new bank account
def register(username: str, password: str) -> bool:
    result = db.execute(f'insert into users (username, password, balance, admin) values (%s, %s, 0, false);', (username, password))
    print(result)

    db.connection.commit()
    return result[0]

#Login to an account
def login(username: str, password: str) -> bool:
    #Find the user trying to log in
    user = db.query("select * from users where username=%s", (username,))
    print(user)

    #Error or nonexistent user
    if not user[0] or len(user[1]) < 1:
        return False
    else:
        return password == user[1][0]["password"]

#Get user ID from username
def getid(username: str) -> int:
    user = db.query("select * from users where username=%s", (username,))
    
    #Error or no user found
    if not user[0] or len(user[1]) < 1:
        return -1
    else:
        return user[1][0]["id"]

#Delete account
def delete_account(username: int, password: str) -> bool:
    #make sure user is authenticated to delete account
    if not login(username, password):
        return False
    
    q = db.execute("delete from users where username=%s", (username,))
    db.connection.commit()

    return q[0]

#Change username
def change_username(uid: int, newname: str, password: str) -> bool:
    pass

def change_password(uid: int, oldpass: str, newpass: str) -> bool:
    pass

#Check balance
def balance(uid: int) -> float:
    pass

#Desposit money
def deposit(uid: int, amount: float) -> None:
    pass

#Withdraw money
def withdraw(uid: int, amount: float) -> bool:
    pass

#Wire money between accounts
def wire(sender: int, recipient: int, amount: float) -> bool:
    pass

