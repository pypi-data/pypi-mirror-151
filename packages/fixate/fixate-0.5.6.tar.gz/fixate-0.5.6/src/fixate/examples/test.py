"""
This is a test script that shows basic use case for the fixate library
"""
import time

from fixate.core.common import TestClass
from fixate.core.ui import user_action, user_ok
from fixate.core.checks import chk_true

__version__ = "0"


class InteractiveUserActionTest(TestClass):
    """
    As the user to hit O.K. inside the user_action
    """

    test_desc = "InteractiveUserActionTest"

    def test(self):
        class MyTest:
            def __init__(self):
                self.count = 0

            def my_test(self):
                user_ok("ok in action target: hit enter to continue " + str(self.count))
                self.count += 1
                return self.count > 3

        c = MyTest()
        user_ok("ok: About to call user_action")
        user_action("action: Display This", c.my_test)
        time.sleep(2)
        user_ok("ok: user_action done")


class NonInteractiveUserActionTest(TestClass):
    """
    user_action will timeout, but the use can FAIL early.
    """

    test_desc = "NonInteractiveUserActionTest"

    def test(self):
        class MyTest:
            def __init__(self):
                self.count = 0

            def my_test(self):
                self.count += 1
                time.sleep(0.5)
                return self.count > 10

        c = MyTest()
        chk_true(user_action("Wait 5 s", c.my_test))


TEST_SEQUENCE = [InteractiveUserActionTest(), NonInteractiveUserActionTest()]
