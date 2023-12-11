
def generate_properties(cls):
    names = [func for func in dir(cls) if callable(getattr(cls, func))]
    names = [func.split('_',1)[1] for func in names if func.startswith('get_') or func.startswith('set_')]
    for name in names:
        getter = None
        if hasattr(cls, f'get_{name}'):
            getter = getattr(cls, f'get_{name}')

        setter = None
        setter_name = f'set_{name}'
        if hasattr(cls, setter_name):
            setter = getattr(cls, setter_name)

        if setter and not getter:
            # print('generate getter and wrap setter for', name)
            continue


        # print('make property:', name, getter, setter)
        setattr(cls, name, property(getter, setter))




if __name__ == '__main__':
    class TestClass:
        def __init__(self, **kwargs):
            self.hp = 10

        def get_a(self):
            return 'a'


        def get_b(self):
            return 'b'
        def set_b(self, value):
            print('set b to:', value)


        def set_hp(self, value):
            # self._hp = value
            print('set hp')


    generate_properties(TestClass)
    print([e for e in dir(TestClass) if not e.startswith('__')])

    e = TestClass()
    print(e.a)
    print(e.b)
    e.b = 2
    print(e.b)

    print(e.hp)
    # e.hp += 4
    # print(e.hp)
    from GamePlusEditor.ursina import *

    invoke(setattr, e, 'position', (0,0,0), delay=1)
    # invoke(e.set_position, (0,0,0))
    # invoke(e.hp.__add__, 10)
    # invoke(exec, 'e.hp += 11', globals())
    print(e.hp)
