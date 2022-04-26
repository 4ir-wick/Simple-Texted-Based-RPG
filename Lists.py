# Author: Eric Stevens

from opcode import hasnargs
import os
import sys
import csv

# class import
from Item import Item
from Room import Room
from RoomSpecial import RoomSpecial

# global item variables
items = {}
itemsFileName = os.path.join(sys.path[0], "items.tsv")
inventory = []
winningItemName = "Lamp"

# global room variables
rooms = {}
roomsFilename = os.path.join(sys.path[0], "rooms.tsv") # file from current directory

# utility functions

# checks if a string is equal to another string
# returns true when equal
# returns true when string is only equal to first letter of compare
# ignores caps
def generousStringCompare(string, compare):
    string = string.lower()
    return (string == compare) | (string == compare[0])

# opens a file and returns a list from the data
def getFileList(filename):
    with open(filename, "r") as file:
        reader = csv.reader(file, delimiter = "\t")
        readerList = list(reader) # make list from reader
        return readerList

# items functions
def makeItems(itemsList):
    for i in range(1, len(itemsList)):
        itemProperties = itemsList[i]
        items[itemProperties[0]] = Item(itemProperties)

# rooms functions
def makeRooms(roomsList):
    for i in range(1, len(roomsList)): # add rooms but skip first row
        roomProperties = roomsList[i]
        if(roomProperties[6] != ""): # if not special room
            rooms[roomProperties[0]] = RoomSpecial(roomProperties) # add special room to rooms
        else:
            rooms[roomProperties[0]] = Room(roomProperties) # add room to rooms
        if roomProperties[7] != "": # if room should start with an item
            rooms[roomProperties[0]].items.append(items[roomProperties[7]]) # add item to room form items dictionary

# returns an item from the inventory
def getInventoryItem(itemName):
    for item in inventory:
        if item.name == itemName:
            return item
    return None

# handles drop requests
def dropRequest(roomName, userInput):
    itemName = userInput.split(" ")[1]
    item = getInventoryItem(itemName)
    if(item != None): # make sure the item exists
        room = rooms[roomName]
        room.accept = True
        room.drop(item)
        inventory.remove(item)
        print("You dropped " + itemName + ".")
    else:
        print(itemName + " is not in your inventory.")

# handles pickup requests
def pickupRequest(message):
    itemName = message.split("-")[1]
    item = items[itemName]
    inventory.append(item)
    print("You picked up " + itemName + ".")

# handle the message
def handleMessage(message, roomName, userInput):
    if message == "drop_request":
        dropRequest(roomName, userInput)
    elif message.__contains__("pickup_request"):
        pickupRequest(message)

# handles the room output
def handleOutput(outputString, userInput):
    output = outputString.split(";")
    roomName = output[0]
    if len(output) > 1: # if the room wanted to communicate
        message = output[1]
        handleMessage(message, roomName, userInput) # handle the message
    return roomName

# event loop
def start():
    startingRoomName = list(rooms.keys())[0]
    currentRoom = rooms[startingRoomName]

    hasNotQuit = True

    print("\ntitle\nsubtitle")
    while(hasNotQuit):
        print("\nType quit/q to exit the game.")
        userInput = input("\n> ")
        print()
        if(generousStringCompare(userInput, "quit")):
            hasNotQuit = False
        else:
            rawOutput = currentRoom.processInput(userInput)
            nextRoomName = handleOutput(rawOutput, userInput)
            currentRoom = rooms[nextRoomName]
            if getInventoryItem(winningItemName) != None:
                print("\nYou win!")
                hasNotQuit = False

# initialize game
def initialize():
    itemsList = getFileList(itemsFileName)
    makeItems(itemsList)
    roomsList = getFileList(roomsFilename)
    makeRooms(roomsList)
    start()

# begins here
initialize()