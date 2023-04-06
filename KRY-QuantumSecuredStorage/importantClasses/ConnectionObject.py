class ConnectionObject:
    connected = False  # static variable
    key = ""  # static variable
    name =""
    password=""


    # Declaring a constructor, taking length and colour as a parameter
    def __init__(self,name, password):
        self.name = name  # instance variable
        self.password = password
