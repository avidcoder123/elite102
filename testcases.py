import unittest

import functions as f
import db

userIDs = []

class TestAuthCapabilities(unittest.TestCase):
    def test_a_register(self):
        global userIDs
        self.assertTrue(f.register("testinguser1", "changed"))
        self.assertTrue(f.register("testinguser2", "test"))

        #No duplicate usernames
        self.assertFalse(f.register("testinguser1", "test"))

        uid1 = f.getid("testinguser1")
        self.assertTrue(uid1 > 0)
        uid2 = f.getid("testinguser2")
        self.assertTrue(uid2 > 0)
        userIDs = [uid1, uid2]

    def test_b_login(self):
        self.assertTrue(f.login("testinguser1", "changed"))
        self.assertTrue(f.login("testinguser2", "test"))

        #Wrong password
        self.assertFalse(f.login("testinguser1", "wrong"))
        #Nonexistant user
        self.assertFalse(f.login("doesnotexist", "test"))
    
    def test_c_changeusername(self):
        self.assertTrue(f.change_username(userIDs[0], "newname"))
        self.assertEqual(f.getid("newname"), userIDs[0])

    def test_d_changepassword(self):
        self.assertTrue(f.change_password(userIDs[0], "changed", "test"))
        self.assertTrue(f.login("newname", "test"))

class TestMoney(unittest.TestCase):
    def test_a_balance(self):
        self.assertEqual(f.balance(userIDs[0]), 0.00)
    
    def test_b_deposit(self):
        self.assertTrue(f.deposit(userIDs[0], 10))
        self.assertEqual(f.balance(userIDs[0]), 10)

    def test_c_withdraw(self):
        self.assertTrue(f.withdraw(userIDs[0], 5))
        self.assertEqual(f.balance(userIDs[0]), 5)

        #No withdrawing more than in account
        self.assertFalse(f.withdraw(userIDs[0], 100))

    def test_d_wire(self):
        #Make sure no money is created or destroyed
        total = f.balance(userIDs[0]) + f.balance(userIDs[1])

        self.assertTrue(f.wire(userIDs[0], userIDs[1], 2))

        self.assertEqual(f.balance(userIDs[0]), 3)
        self.assertEqual(f.balance(userIDs[1]), 2)

        self.assertEqual(f.balance(userIDs[0]) + f.balance(userIDs[1]), total)
        

if __name__ == "__main__":
    unittest.main()
    for id in userIDs:
            f.delete_account(id, "test")

