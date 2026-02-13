class Tool:

    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return f"Tool(name={self.name}, description={self.description})"

    def __repr__(self):
        return self.__str__()