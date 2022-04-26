from inspect import signature

class Room:
    def __init__(self, roomProperties):
        self.name = roomProperties[0]
        self.description = roomProperties[1]
        self.exits = {"north": roomProperties[2], "south": roomProperties[3], "east": roomProperties[4], "west": roomProperties[5]}
        self.items = []
        self.accept = False # used for event loop communication
    
    def processInput(self, userInput):
        nextRoom = self.name
        userInputSplit = userInput.split(" ")
        command = userInputSplit[0]

        result = getattr(self, command, 0) # get command in object, return 0 if not valid
        if((result == 0) | (callable(result) == False)): # if doesn't exist or not a function
            print("Not a valid command.\nType \"help\" for a list of commands.")
            return nextRoom
        
        functionSignature = signature(result)
        numOfRequiredParams = len(functionSignature.parameters)
        numOfInputParams = len(userInputSplit) - 1
        if(numOfInputParams >= numOfRequiredParams): # there must be at least the minimum num of required parameters
            if((numOfRequiredParams > 0)): # if there is a parameter
                parameter = userInputSplit[1]
                nextRoom = result(parameter)
            else:
                nextRoom = result()
        else:
            print("Incorrect arguments.")
        if(nextRoom == None):
            nextRoom = self.name
        return nextRoom

    def move(self, direction):
        exit = self.__checkExit(direction)
        if(exit != None):
            print("You go " + direction + " into the " + exit + ".")
            return exit

    def __checkExit(self, direction): # private method
        if(direction in self.exits):
            if(self.exits[direction] != ""):
                return self.exits[direction]
            else:
                print("You cannot go that way.")
        else:
            print("Not a valid direction.")
    
    def showExits(self):
        for exit in self.exits.keys():
            print(exit + ": " + self.exits[exit])

    def look(self):
        self.__showDrops()
        print(self.name + "\n" + self.description)

    def drop(self, item):
        if (self.accept == False):
            return self.name + ";drop_request" # send a request
        else: # if the event loop allowed the drop
            self.accept = False
            self.items.append(item)

    def __showDrops(self): # private method
        if len(self.items) > 0:
            print("Dropped Items:")
            for item in self.items:
                print(" " + item.name + "\n  " + item.description)
            print()

    def __getRoomItem(self, itemName): # private method
        for item in self.items:
            if item.name == itemName:
                return item
        return None

    def pickup(self, itemName):
        item = self.__getRoomItem(itemName)
        self.items.remove(item)
        return self.name + ";pickup_request-" + itemName

    def help(self):
        for command in dir(self):
            if(command.__contains__("__") == False): # if not private
                if callable(getattr(self, command)): # if it is a function
                    if(command != "processInput"): # exclude process input function
                        print(command)