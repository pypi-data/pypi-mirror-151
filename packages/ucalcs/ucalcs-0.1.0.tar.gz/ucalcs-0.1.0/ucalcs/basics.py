class Basics:
    def __init__(self):
        self.value = int()

    def some_all(self, *args):
        for value in args:
            self.value += value
        return self.value
    
    def subtract_all(self, *args):
        for value in args:
            if self.value == 0:
                self.value = value
            else:
                self.value -= value
        return self.value
    
    def multiply_all(self, *args):
        for value in args:
            self.value *= value
            if self.value == 0:
                self.value = value
        return self.value
    
    def divide_all(self, *args):
        for value in args:
            if self.value == 0:
                self.value = value
            else:
                self.value /= value
        return self.value