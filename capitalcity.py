import tkinter
from tkinter import *
from random import randrange
import time
import json
import countrymodule
from countrymodule import Country
import playermodule
from playermodule import Player


'''

    @authors                                     Loris Mayr / Flavian Neggri / Eymeric Zougs 
    @date                                        18.12.2020

'''


#==--------------------------------------------------------------------------------------------------------------------------------------------==#
#   Data
#==--------------------------------------------------------------------------------------------------------------------------------------------==#


# open json file which contains the data about the countries
with open('data.json') as f:
    data = json.load(f)

# store all the data inside this list
countries_cap = []


for i in data:
    country = i['Country']
    capital = i['City']
    alternate = i['alternate']
    picture = i['picture']
    countries_cap.append(Country(country, capital, alternate, picture))


# open json file which keeps track of current rank
with open('players.json') as f:
    data = json.load(f)


#==--------------------------------------------------------------------------------------------------------------------------------------------==#
#   Methods
#==--------------------------------------------------------------------------------------------------------------------------------------------==#


def levenshtein(word1, word2):
    '''
        Return the minimum editing distance of two words 
                using dynamic programming 
                runtime O(n*m)
                we use this algorithm to detect spelling errors
                for a more detailed view check https://de.wikipedia.org/wiki/Levenshtein-Distanz

                @param word1 the first word
                @param word2 the second word

                @return the minimal editing distance between word1 and word2
'''
    s = " "
    word1 = s + word1
    word2 = s + word2

    n = len(word1)
    m = len(word2)

    # initialize table
    table = []
    for i in range(n):
        table.append([0] * m)

    # filling entries correct to start with dp
    for i in range(n):
        table[i][0] = i

    # filling entries correct to start with dp
    for i in range(m):
        table[0][i] = i

    # dp algorithm
    for i in range(1, n):
        for j in range(1, m):
            tmp = 1
            if(word1[i] == word2[j]):
                tmp = 0
            table[i][j] = min(table[i - 1][j - 1] + tmp,
                              table[i - 1][j] + 1, table[i][j - 1] + 1)

    return table[n - 1][m - 1]


def ranlist(n):
    '''
            generate a random permutation of the (0,1,2,...,n-1) and returns it as a list
    '''
    l = []
    while len(l) != n:
        r = randrange(n)
        if r not in l:
            l.append(r)
    return l


def endGame():
    '''
            end of the game, shows rank of the player and the points they achieved
    '''
    weiterbutton.destroy()
    entryanswer.destroy()
    richtiglabel.destroy()
    countrylabelimage.destroy()
    questionlabel.config(text="Game Over! You have " +
                         str(spieler.points) + " Points!")
    if spieler.name.lower() in data.keys():
        if spieler.points > data[spieler.name.lower()]:
            data[spieler.name.lower()] = spieler. points
    else:
        data[spieler.name.lower()] = spieler.points
    with open('players.json', 'w') as f:
        json.dump(data, f)
    bestrank = sorted(data.items(), key=lambda k, v: v, reverse=True)
    for i in range(len(bestrank)):
        if i > 19:
            break
        namep = bestrank[i][0]
        q = len(namep)
        r = 35 - q
        for j in range(r):
            namep = namep + "."
        namep = namep + "Points: "
        listbox.insert(i, str(i + 1) + ".   " +
                       namep.upper() + str(bestrank[i][1]))

    rankinglabel.pack(pady=(20, 0))
    listbox.pack()


def isCorrect(e):
    '''
            checks wheter answer is corret, or just a spelling error
            adds one point when answer is corret
            adds one strike when answer is wrong 
            shows correct spelling in case of spelling error
    '''
    answer = entryanswer.get().lower()
    answer = answer.rstrip()

    global i
    sol = countries_cap[r[i]].getCap().lower()
    entryanswer.unbind("<Return>")

    if answer == sol or answer in countries_cap[r[i]].alternate_names:
        richtiglabel.config(text="Correct !")
        richtiglabel.pack(pady=(20, 0))
        spieler.points += 1
        pointlabel.config(text="Points: " + str(spieler.points))

    elif levenshtein(answer, sol) <= len(sol) / 3:
        richtiglabel.config(text="Pay attention to your spelling! The correct spelling is " +
                            countries_cap[r[i]].getCap(), font=("sans-serif", 10, "bold"))
        richtiglabel.pack(pady=(20, 0))

    elif len(countries_cap[r[i]].alternate_names) != 0 and min([levenshtein(answer, x) for x in countries_cap[r[i]].alternate_names]) < len(sol) / 3:
        richtiglabel.config(text="Pay attention to your spelling! The correct spelling is " +
                            countries_cap[r[i]].getCap(), font=("sans-serif", 10, "bold"))
        richtiglabel.pack(pady=(20, 0))

    else:
        richtiglabel.config(
            text="Wrong! The right answer is " + countries_cap[r[i]].getCap())
        richtiglabel.pack(pady=(20, 0))
        spieler.strikes += 1
        strikelabel.config(text="Strikes: " + str(spieler.strikes))

    i += 1

    weiterbutton.pack(pady=(20, 0))


def startgame():
    '''
            starts the game with the first question
    '''
    if i == n or spieler.strikes >= 3:
        endGame()
        return
    weiterbutton.pack_forget()
    richtiglabel.pack_forget()
    usernametext.destroy()
    usernametext2.destroy()
    entryusername.destroy()
    losgehtslabel.destroy()
    pointlabel.pack(side=LEFT, anchor='nw')
    strikelabel.pack(side=RIGHT, anchor='ne')
    strikelabel.config(text="Strikes: " + str(spieler.strikes))
    pointlabel.config(text="Points: " + str(spieler.points))
    questionlabel.config(text="What is the capital of " +
                         countries_cap[r[i]].getCountry() + "?")
    questionlabel.pack(pady=50)
    imagecountry.config(file=countries_cap[r[i]].picturename)
    countrylabelimage.config(image=imagecountry)
    countrylabelimage.pack(pady=30)
    entryanswer.delete(0, END)
    entryanswer.pack()
    entryanswer.bind("<Return>", isCorrect)


def createSpieler(e):
    '''
            cretates a player
    '''
    global spieler
    losgehtslabel.pack(pady=(70, 0))
    spieler = Player(entryusername.get())
    entryusername.unbind("<Return>")


def startUsername():
    '''
            corresponds to the part of the game, where you type in your username
    '''
    usernametext.pack(pady=(30, 0))
    usernametext2.pack()
    entryusername.pack(pady=(30, 0))
    entryusername.bind("<Return>", createSpieler)


def startIsPressed():
    ''' 
            invokes the startUsername() function
    '''
    labeltext.destroy()
    labelimage.destroy()
    btnStart.destroy()
    startUsername()


#==--------------------------------------------------------------------------------------------------------------------------------------------==#
#   Constants
#==--------------------------------------------------------------------------------------------------------------------------------------------==#

# length of countries
n = len(countries_cap)
# random permutation
r = ranlist(n)
# index we use for the game
i = 0


#==--------------------------------------------------------------------------------------------------------------------------------------------==#
#   Graphical User Interface
#==--------------------------------------------------------------------------------------------------------------------------------------------==#


root = tkinter.Tk()

# Title of the Game
root.title("Capital City Game")

# Size of the window
root.geometry("1700x900")

# Background color in hexadecimal
root.config(background="#ffffff")


# Label for the Rank at the end of the game
rankinglabel = Label(text=" Ranking", font=(
    "sans-serif", 20, "bold"), background="#ffffff")
listbox = Listbox(bg="#ffffff", font=(
    "sans-serif", 20, "bold"), width=40, height=10)

# button for the next question
weiterbutton = Button(root, text="next ",
                      font=("sans-serif", 20, "bold"),
                      background="#ffffff",
                      width=7,
                      command=startgame)

# label which shows if the result is correct or not
richtiglabel = Label(root,
                     text=" ",
                     font=("sans-serif", 17, "bold"),
                     background="#ffffff")

# radio box to enter the answer
entryanswer = Entry(root, width=20)

# label for the question, by default empty
questionlabel = Label(root,
                      text=" ",
                      font=("sans-serif", 20, "bold"),
                      background="#ffffff")

# shows number of strikes
strikelabel = Label(root, text="Strikes: ", bg="red")

# shows number of points
pointlabel = Label(root, text="Points: ", bg="green")

# radiobox to enter the username
entryusername = Entry(root, width=20)

# shows "Geben Sie ihren Benutername ein"
usernametext = Label(root,
                     text="Enter your username: ",
                     font=("sans-serif", 24, "bold"),
                     background="#ffffff")

# shows "bestaetigen Sie mit Enter"
usernametext2 = Label(root,
                      text="and confirm with enter ",
                      font=("sans-serif", 18),
                      background="#ffffff")

# button to start the game
losgehtslabel = Button(root, text="Let`s go ",
                       font=("sans-serif", 20, "bold"),
                       background="#ffffff",
                       width=10,
                       command=startgame)

# shows title of the game
labeltext = Label(
    root,
    text="Capital City Game",
    font=("sans-serif", 24, "bold"),
    background="#ffffff")
labeltext.pack(pady=(30, 0))

# for showing the earth icon
imagecountry = PhotoImage(file="Pictures/earthicon.png")

# for showing the country picture
countrylabelimage = Label(root, background="#ffffff")

# earth icon
img1logo = PhotoImage(file="Pictures/earthicon.png")
labelimage = Label(
    root,
    image=img1logo,
    background="#ffffff"
)
labelimage.pack(pady=(30, 0))


# startbutton icon
img2 = PhotoImage(file="Pictures/startbutton.png")
btnStart = Button(
    root,
    image=img2,
    relief=FLAT,
    border=0,
    background="#ffffff",
    command=startIsPressed  )
btnStart.pack(pady=(30, 0))


# starts the game
root.mainloop()
