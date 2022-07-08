import time
from typing import ClassVar
from dataclasses import dataclass

class A:
    slept: bool = False

    @classmethod
    def x(cls):
        if not cls.slept:
            time.sleep(3)
            cls.slept = True
        return True

@dataclass
class B(A):
    pass

