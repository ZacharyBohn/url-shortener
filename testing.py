class MyClass:
	class_variable: int | None =  None

	@classmethod
	def setup(cls):
		cls.class_variable = 42
		return

	@classmethod
	def test(cls):
		print(cls.class_variable)
		return

class ThirdClass:
	testing: int = 99

class SubClass(MyClass, ThirdClass):
	subclass_variable: int = 9
	@classmethod
	def test2(cls):
		print(cls.subclass_variable)
		print(cls.class_variable)
		return

SubClass.setup()
SubClass.test2()