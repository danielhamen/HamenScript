class staticproperty(property):
    """
    Decorator for a static property. Sort of like an @staticmethod, but for a property

    Example:
    ```python
    class MyClass:
        def __init__(self): ...

        @staticproperty
        def a(self):
            return 123

    MyClass.a
    # Output: 123
    ```
    """

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()