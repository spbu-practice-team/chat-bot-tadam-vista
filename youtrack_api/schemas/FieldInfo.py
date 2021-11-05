class FieldInfo:
    def __init__(self, name, value, is_valid=True):
        self.name = name  # always string
        self.value = value  # not always string
        self.is_valid = is_valid

    def show(self):
        if self.is_valid:
            print(f"{self.name}: {self.value}")
        else:
            print("Not valid")
