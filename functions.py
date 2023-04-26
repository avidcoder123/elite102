import db

#Register a new bank account
def register(username: str, password: str) -> bool:
    result = db.execute(f'insert into users (username, password, balance, admin) values (%s, %s, 0, false)', (username, password))

    db.connection.commit()
    return result[0]

#Login to an account
def login(username: str, password: str) -> bool:
    #Find the user trying to log in
    q = db.query("select * from users where username=%s and password=%s", (username, password))
    return q[0]

#Get user ID from username
def getid(username: str) -> int:
    user = db.query("select * from users where username=%s", (username,))
    
    #Error or no user found
    if not user[0] or len(user[1]) < 1:
        return -1
    else:
        return user[1][0]["id"]

#Delete account
def delete_account(uid: int, password: str) -> bool:
    q = db.query("select * from users where id=%s and password=%s", (uid, password))
    if not q[0]:
        return False
    
    q = db.execute("delete from users where id=%s and password=%s", (uid, password))
    db.connection.commit()

    return q[0]

#Change username
def change_username(uid: int, newname: str) -> bool:
    q = db.execute("update users set username=%s where id=%s", (newname, uid))
    db.connection.commit()

    return q[0]

def change_password(uid: int, oldpass: str, newpass: str) -> bool:
    q = db.query("select * from users where id=%s and password=%s", (uid, oldpass))
    if not q[0]:
        return False
    q = db.execute("update users set password=%s where id=%s and password=%s", (newpass, uid, oldpass))
    db.connection.commit()

    return q[0]

#Check balance
def balance(uid: int) -> float:
    b = db.query("select * from users where id=%s", (uid, ))
    if not b[0]:
        return float(0)
    else:
        return b[1][0]["balance"]

#Desposit money
def deposit(uid: int, amount: float) -> bool:
    bal = balance(uid)
    q = db.execute("update users set balance=%s where id=%s", (float(bal) + amount, uid))
    db.connection.commit()

    return q[0]

#Withdraw money
withdraw = lambda uid, amount: deposit(uid, 0 - amount)

#Wire money between accounts
def wire(sender: int, recipient: int, amount: float) -> bool:
    s = withdraw(sender, amount)
    r = deposit(recipient, amount)

    return s and r

