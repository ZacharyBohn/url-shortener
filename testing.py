from typing import Type


class This:
	@staticmethod
	def something() -> int:
		return 55

class DI:
	def __init__(self) -> None:
		self.this: Type[This] = This
		return

di = DI()
def something_else() -> int:
	return 66
di.this.something = something_else
print(di.this.something())
