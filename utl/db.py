# Matthew Chan (PM), Hannah Fried, Coby Sontag, Jionghao Wu [Team SOS]
# SoftDev1 pd2
# P00 -- Da Art of Storytellin'
# 2019-10-28

import sqlite3 # enable control of an sqlite database

def uniqueTitle(curse, title): # return a boolean for whether or not a given title matches one already in the table.
    repeats = curse.execute("SELECT Title FROM stories;")
    for names in repeats:
        if (names[0] == title):
            return False
    return True

def uniqueUsername(curse, username): # return a boolean for whether or not a given username matches one already in the table
    repeats = curse.execute("SELECT Username FROM users;")
    for names in repeats:
        if (names[0] == username):
            return False
    return True

def addUser(curse, username, password): # add a row to the users database, with the given username/passwrd combo. Return nothing.
    curse.execute("INSERT INTO users (Username, Password) VALUES(?, ?);", (username, password))

def addEntry(curse, title, entry, author): # add a row to the stories database, with the given title/entry/author combo. Return nothing.
    print("\nTitle: "+title+"\nText: "+entry+"\nAuthor: "+author+"\n")#debug statement
    curse.execute("INSERT INTO stories (Title, Entries, Author) VALUES(?, ?, ?);", (title, entry, author))

def authenticate(curse, username, password): # return true if the username/password combo exists within the database, otherwise return false.
    #givenUser = (username, password)
    cursorObject = curse.execute("SELECT Password FROM users WHERE Username = ?;", (username,))
    for passwordTuple in cursorObject:
        if (passwordTuple[0] != password):
            return False
        return True
    return False

def getFullStory(curse, title): # return a list of every entry associated with a story within a list for the story
    textEntries = []
    cursorObject = curse.execute("SELECT Entries FROM stories WHERE Title = ?;", (title,))
    for storyTuple in cursorObject:
        textEntries.append(storyTuple[0])
    return textEntries

def lastEntry(curse, title):#return the most recent entry in a given story identified by the title
    mostRecentEntry = ""
    cursorObject = curse.execute("SELECT Entries FROM stories WHERE Title = ?;", (title,))
    for storyTuple in cursorObject:
        mostRecentEntry = storyTuple[0]
    return mostRecentEntry

def getContributedStories(curse, username): # return a list of the titles of every story contributed to by an author
    contributedStories = []
    cursorObject = curse.execute("SELECT Title FROM stories WHERE Author = ?;", (username,))
    for titleTuple in cursorObject:
        if (titleTuple[0] not in contributedStories):
            contributedStories.append(titleTuple[0])
        print(contributedStories)
    return contributedStories

def getOtherStories(curse, username): # return a list of the titles of every NOT story contributed to by an author
    notContributedStories = []
    executionStr = ("SELECT Title FROM stories WHERE Author != ?", (username,))
    for contrTitle in getContributedStories(curse, username):
        executionStr += ("AND Title != ?", (contrTitle,))
    cursorObject = curse.execute(executionStr)
    for titlesTuple in cursorObject:
        if (titlesTuple[0] not in notContributedStories):
            notContributedStories.append(titlesTuple[0])
    return notContributedStories

def getTitlesAndStories(curse, username): # return a dict of each story for a given username
    titlesToStories = dict()
    storytitles = getContributedStories(curse, username)
    for titles in storytitles:
        titlesToStories[titles] = getFullStory(curse,titles)
    return titlesToStories
