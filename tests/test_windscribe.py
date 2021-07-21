import unittest
import windscribe
import getpass
import socket
import os
from loguru import logger
from windscribe.exceptions import (
    NotLoggedInException,
    ProAccountRequiredException,
    InvalidCredentialsException,
    InvalidPasswordException,
    InvalidUsernameException,
)

# Stop the logger
logger.remove()

# Check if connected to internet
try:
    socket.setdefaulttimeout(3)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("8.8.8.8", 53))
    s.close()
    connected = True

except socket.error as ex:
    connected = False

# Ask username and password
username = os.environ.get("WINDSCRIBE_USER")
if username is None:
    username = input("Username: ")

password = os.environ.get("WINDSCRIBE_PW")
if password is None:
    password = getpass.getpass("Password: ")


def is_pro_account():
    """ Checks if the user has a pro account."""
    try:
        windscribe.login(username, password)
        return "Free" in windscribe.account().plan
    except:
        return False


def is_logged_in():
    """ Checks if the user is logged in."""
    try:
        windscribe.login(username, password)
        return True
    except:
        return False


class TestLoginLogout(unittest.TestCase):
    def setUp(self):
        # Setups the test.
        windscribe.logout()

    @unittest.skipIf(not connected, "Not connected to internet")
    def test_normal(self):
        # Tests login() and logout().
        self.assertTrue(windscribe.login(username, password))
        self.assertFalse(windscribe.login(username, password))
        self.assertTrue(windscribe.logout())
        self.assertFalse(windscribe.logout())

    @unittest.skipIf(connected, "Connected to internet")
    def test_no_connection(self):
        # Tests login() while not connected to internet.
        with self.assertRaises(ConnectionError):
            windscribe.login(username, password)

        print(windscribe.logout())

    @unittest.skipIf(
        not connected or os.environ.get(
            "WINDSCRIBE_USER") or os.environ.get("WINDSCRIBE_PW"),
        "Not connected to internet or creditials already in environment",
    )
    def test_environment_parameters(self):
        # Tests login() with the environment variables.
        with self.assertRaises(InvalidUsernameException):
            windscribe.login()
        with self.assertRaises(InvalidPasswordException):
            windscribe.login(user="test")

        os.environ.setdefault("WINDSCRIBE_USER", username)
        os.environ.setdefault("WINDSCRIBE_PW", password)

        self.assertTrue(windscribe.login())
        self.assertFalse(windscribe.login())

    @unittest.skipIf(not connected, "Not connected to internet")
    def test_invalid_creditials(self):
        # Tests login() with the invalid creditials.
        with self.assertRaises(InvalidCredentialsException):
            windscribe.login("test", "test")


class TestStatusVersion(unittest.TestCase):
    def setUp(self):
        # Setups the test.
        windscribe.logout()

    @unittest.skipIf(not connected, "Not connected to internet")
    def test_normal(self):
        # Tests status() and version().
        windscribe.login(username, password)
        windscribe.connect()
        self.assertIsInstance(windscribe.status(), windscribe.WindscribeStatus)
        self.assertIsInstance(windscribe.version(), str)

    @unittest.skipIf(not connected, "Not connected to internet")
    def test_not_logged(self):
        # Tests status() and version() while not logged in.
        self.assertIsInstance(windscribe.status(), windscribe.WindscribeStatus)
        self.assertIsInstance(windscribe.version(), str)

    @unittest.skipIf(connected, "Connected to internet")
    def test_no_connection(self):
        # Tests status() and version() while not connected to internet.
        with self.assertRaises(ConnectionError):
            windscribe.status()
        self.assertIsInstance(windscribe.version(), str)


class TestLocationsAccount(unittest.TestCase):
    def setUp(self):
        # Setups the test.
        windscribe.logout()

    @unittest.skipIf(not connected, "Not connected to internet")
    def test_normal(self):
        # Tests locations() and account().
        windscribe.login(username, password)
        windscribe.connect()
        self.assertIsInstance(windscribe.locations(), list)
        self.assertIsInstance(windscribe.account(),
                              windscribe.WindscribeAccount)

    def test_not_logged(self):
        # Tests locations() and account() while not logged in.
        with self.assertRaises(NotLoggedInException):
            windscribe.locations()

        with self.assertRaises(NotLoggedInException):
            windscribe.account()

    @unittest.skipIf(connected, "Connected to internet")
    def test_no_connection(self):
        # Tests locations() and account() while not connected to internet.
        self.assertIsInstance(windscribe.locations(), list)
        self.assertIsInstance(windscribe.account(),
                              windscribe.WindscribeAccount)


class TestConnectDisconnect(unittest.TestCase):
    def setUp(self):
        # Setups the test.
        windscribe.logout()

    @unittest.skipIf(not connected, "Not connected to internet")
    def test_normal(self):
        # Tests connect(), and disconnect().
        windscribe.login(username, password)
        self.assertIsNone(windscribe.disconnect())
        self.assertIsNone(windscribe.connect())
        self.assertIsNone(windscribe.connect(windscribe.locations()[0]))
        self.assertIsNone(windscribe.disconnect())

    def test_not_logged(self):
        # Tests connect(), and disconnect() while not logged in.
        with self.assertRaises(NotLoggedInException):
            windscribe.connect()

        self.assertIsNone(windscribe.disconnect())

    @unittest.skipIf(connected or not is_logged_in(), "Connected to internet or not logged in.")
    def test_no_connection(self):
        # Tests connect(), and disconnect() while not connected to internet.
        with self.assertRaises(ConnectionError):
            windscribe.connect()

        with self.assertRaises(ConnectionError):
            windscribe.disconnect()

    @unittest.skipIf(not connected or is_pro_account(), "Not connected to internet or free account")
    def test_pro_location(self):
        # Tests connect() with a pro account location.
        windscribe.login(username, password)
        with self.assertRaises(ProAccountRequiredException):
            windscribe.connect("WINDFLIX US")


if __name__ == "__main__":
    unittest.main()
