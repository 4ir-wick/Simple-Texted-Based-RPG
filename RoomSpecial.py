from Room import Room

class RoomSpecial(Room):
    def __init__(self, roomProperties):
        super().__init__(roomProperties) # construct using super
        specialString = roomProperties[6]
        specialProperties = specialString.split(" ", 1) # split string only once
        self.specialCommand = specialProperties[0]
        self.specialExit = specialProperties[1]
        
        def special(): # create function for the new command
            print("You go into the " + self.specialExit + ".")
            return self.specialExit

        # give this object that function
        # the name of the function is specified by the properties
        setattr(self, self.specialCommand, special)

    def help(self):
        for command in dir(self):
            if(command.__contains__("__") == False): # if not private
                if callable(getattr(self, command)): # if it is a function
                    if(command != "processInput"): # exclude main function
                        if(command != self.specialCommand): # exclude special command
                            print(command)