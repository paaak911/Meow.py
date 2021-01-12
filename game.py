# My resolution: 1920*1080
from tkinter import *
from time import sleep
from datetime import datetime
import time
import math
import random
import threading
import os.path
import re

root = Tk()
root.resizable(False, False)
root.title("Meow.py")

width = 1000
height = 700
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (width/2)
y = (hs/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
canvas = Canvas(root, bg="black", width=width, height=height)

# buttons
btn_start = Button(canvas, text="I think I'm ready", width="20", height="1")
btn_submit = Button(canvas, text="submit", width="20", height="1")
btn_quit = Button(canvas, text="ok bye", width="20", height="1")
btn_LeaderBrd = Button(canvas, text="Show me the Wall of Fame",
                       width="20", height="1")
# Var
# State of Game
global gameStartTime
gameStartTime = time.time()
global gameFinished
gameFinished = False
global paused
paused = False
global pausedStart
global pausedTimer
global boss_en
boss_en = False
# Player Ship
# global spaceShip
global spaceShipSize
spaceShipSize = 30
global spaceShipHealth
spaceShipHealth = 3
global spaceShipHealthText
global spaceShipHealthList
spaceShipHealthList = ["\u2764", "\u2764", "\u2764"]
global reloaded
reloaded = True
global spaceShipHit
spaceShipHit = datetime.now()
global lastInjured
lastInjured = datetime.now()
# Enemy Ship
# global enemyShip
global lastFired
lastFired = datetime.now()
global enemyShipHealth
enemyShipHealth = 300
global enemyShipSize
enemyShipSize = 30
# Leaderboard
global cheated
cheated = False
# Coords for Player Ship wall collision
global walls
walls = [spaceShipSize / 2, spaceShipSize / 2, width - spaceShipSize / 2,
         height - spaceShipSize / 2]
# game_ini
# spaceShip
cat0 = PhotoImage(file="./images/cat0.png")
cat1 = PhotoImage(file="./images/cat1.png")
work = PhotoImage(file="./images/work.png")
# background images
menu_bg = PhotoImage(file="./images/menu_bg.png")
game_bg = PhotoImage(file="./images/game_bg.png")
lost_bg = PhotoImage(file="./images/lost_bg.png")
won_bg = PhotoImage(file="./images/won_bg.png")
ldr_bg = PhotoImage(file="./images/ldrboard_bg.png")


def quit():
    root.destroy()


def updateLeaderBoard(time):
    # leaderboard.txt example included in directory
    # Keep leaderboard.txt in directory to test when file exists
    filename = "leaderboard.txt"
    under_10 = True
    if cheated:
        btn_submit.destroy()
    # update and show if won
    if gameState == "won" and not cheated:
        name = entry.get()
        canvas.delete("all")
        btn_submit.destroy()
        time = round(time, 4)
        if os.path.isfile(filename) is False:
            # file does not exist
            leaderboard = open(filename, "w")
            leaderboard.write(name + "," + str(time) + ";")
            leaderboard.close()
            lst_name = [name]
            lst_time = [time]
            showLeaderBoard(lst_name, lst_time, name, under_10)
        else:
            # file exists
            regex_name = "^.+,"
            regex_time = "\d+\.\d+;$"
            lst_name = []
            lst_time = []
            appended = False
            data = tuple(open(filename, 'r'))
            for i in data:
                i_name = re.search(regex_name, i).group()
                i_time = re.search(regex_time, i).group()
                # delete trialing ;
                i_name = i_name[:-1]
                i_time = i_time[:-1]
                i_time = round(float(i_time), 4)
                if time < i_time:
                    if not appended:
                        appended = True
                        lst_name.append(name)
                        lst_name.append(i_name)
                        lst_time.append(time)
                        lst_time.append(i_time)
                    else:
                        lst_name.append(i_name)
                        lst_time.append(i_time)
                elif i == data[-1]:
                    if not appended:
                        appended = True
                        lst_name.append(i_name)
                        lst_name.append(name)
                        lst_time.append(i_time)
                        lst_time.append(time)
                    else:
                        lst_name.append(i_name)
                        lst_time.append(i_time)
                else:
                    lst_name.append(i_name)
                    lst_time.append(i_time)
            # write updated list to txt
            open(filename, 'w').close()
            leaderboard = open(filename, 'a')
            i = 0
            for item in lst_name:
                if i < 10:
                    leaderboard.write(item + "," + str(lst_time[i]) + ";\n")
                    i += 1
                elif name == lst_name[i]:
                    under_10 = False
                    lst_name.remove(item)
                    lst_time.remove(lst_time[i])
            leaderboard.close()
            lst_name = lst_name[:10]
            lst_time = lst_time[:10]
            showLeaderBoard(lst_name, lst_time, name, under_10)
    # only show if lost
    else:
        if os.path.isfile(filename) is False:
            # file does not exist
            leaderboard = open(filename, "w")
            leaderboard.close()
            showLeaderBoard([], [], "", False)
        # file exists
        else:
            regex_name = "^.+,"
            regex_time = "\d+\.\d+;$"
            lst_name = []
            lst_time = []
            data = tuple(open(filename, 'r'))
            for i in data:
                i_name = re.search(regex_name, i).group()
                i_time = re.search(regex_time, i).group()
                # delete trialing ;
                i_name = i_name[:-1]
                i_time = i_time[:-1]
                i_time = round(float(i_time), 4)
                lst_name.append(i_name)
                lst_time.append(i_time)
            name = ""
            under_10 = True
            showLeaderBoard(lst_name, lst_time, name, under_10)


def showLeaderBoard(lst_name, lst_time, name, under_10):
    canvas.delete("all")
    btn_LeaderBrd.destroy()
    canvas.create_image(width/2, height/2, image=ldr_bg)
    x = 30
    rank = 1
    if not under_10:
        text = "You tried. . . but it wasn't enough to be on the Wall of Fame"
        canvas.create_text(width/2, height-175, fill="white", font="Arial 8",
                           text="You're underperforming >:(")
        canvas.create_text(width/2, height-200, fill="white", font="Arial 12",
                           text=text)
    elif cheated:
        text = "You cheated. . . you're not gonna be on the Wall of Fame"
        canvas.create_text(width/2, height-175, fill="white", font="Arial 8",
                           text="Try not to cheat next time >:(")
        canvas.create_text(width/2, height-200, fill="white", font="Arial 12",
                           text=text)
    canvas.create_text(width/2, 100, fill="white", font="Times 25 bold",
                       text="The Wall of Fame")
    canvas.create_text(width/2 - 210, 150, fill="white", font="Arial 12 bold",
                       text="Rank")
    canvas.create_text(width/2 - 60, 150, fill="white", font="Arial 12 bold",
                       text="Name")
    canvas.create_text(width/2 + 170, 150, fill="white", font="Arial 12 bold",
                       text="Time")
    for item in lst_name:
        if name == item and under_10:
            canvas.create_text(width/2 - 210, 150 + x, fill="gold",
                               font="Arial 12 bold", text=str(rank))
            canvas.create_text(width/2 - 60, 150 + x, fill="gold",
                               font="Arial 12 bold", text=name)
            canvas.create_text(width/2 + 170, 150 + x, fill="gold",
                               font="Arial 12 bold",
                               text=str(lst_time[rank-1]) + "(s)")
        else:
            canvas.create_text(width/2 - 210, 150 + x, fill="light gray",
                               font="Arial 12 bold", text=str(rank))
            canvas.create_text(width/2 - 60, 150 + x, fill="light gray",
                               font="Arial 12 bold", text=item)
            canvas.create_text(width/2 + 170, 150 + x, fill="light gray",
                               font="Arial 12 bold",
                               text=str(lst_time[rank-1]) + "(s)")
        rank += 1
        x += 30
    btn_quit.place(x=width/2 - 75, y=height - 100)
    btn_quit['command'] = quit


def gameWon():
    global gameState
    global gameStartTime
    global entry
    gameState = "won"
    canvas.delete("all")
    timeElapsed = time.time() - gameStartTime
    canvas.create_image(width/2, height/2, image=won_bg)
    canvas.create_text(width/2, height/2 - 60, fill="white",
                       font="Times 25 italic bold", text="YOU WON!")
    canvas.create_text(width/2, height/2 - 30, fill="white",
                       font="Times 18 italic bold",
                       text="You destoryed the enemy in " +
                       "{:.2f}".format(float(timeElapsed)) +
                       " seconds!")
    canvas.create_text(width/2, height/2 + 30, fill="white",
                       font="Times 20  bold", text="Enter your name!")
    entry = Entry(root)
    canvas.create_window(width/2, height/2 + 80, window=entry)
    btn_submit.place(x=width/2 - 75, y=height/2 + 100)
    btn_submit['command'] = lambda arg=timeElapsed: updateLeaderBoard(arg)


def gameLost():
    global gameState
    gameState = "lost"
    canvas.delete("all")
    timeElapsed = time.time() - gameStartTime
    canvas.create_image(width/2, height/2, image=lost_bg)
    canvas.create_text(width / 2, height - 200, fill="white",
                       font="Times 25 italic bold", text="YOU DIED!")
    canvas.create_text(width / 2, height - 150, fill="white",
                       font="Times 20 italic bold",
                       text="The enemy destoryed you in " +
                       "{:.2f}".format(float(timeElapsed)) + " seconds!")
    btn_LeaderBrd.place(x=width/2 - 75, y=height - 100)
    btn_LeaderBrd['command'] = lambda arg = timeElapsed: updateLeaderBoard(arg)


def checkMyLaser(movementTag):
    global myLaser
    global reloaded
    global myLaser
    global enemyShipHealth
    a = False
    b = False
    hitSomething = False
    enemyCoords = canvas.coords(enemyShip)
    myLaserCoords = canvas.coords(myLaser)

    if hitSomething is False:
        a = overlapping(myLaserCoords, enemyCoords)
        b = hitWall(myLaserCoords, "right", False)

        # if laser hit enemyShip
        if a is True:
            canvas.delete(myLaser)
            enemyShipHealth = enemyShipHealth - 10
            reloaded = True
            canvas.itemconfig(spaceShip, image=cat0)

            # update enemyShipHealthText
            temp = str(enemyShipHealth) + "/300"
            canvas.itemconfig(enemyShipHealthText, text=temp)
            canvas.itemconfig(enemyShip, fill="orange")
            root.update()

            if movementTag == "up_down":
                fill = "blue"
            elif movementTag == "circular":
                fill = "red"
            elif movementTag == "spam":
                fill = "purple"
            elif movementTag == "idek":
                fill = "green"
            canvas.after(50, canvas.itemconfig(enemyShip, fill=fill))
            root.update()

            # check for win condition
            if enemyShipHealth == 0:
                gameWon()

        # if laser hit wall
        elif b is True:
            canvas.delete(myLaser)
            reloaded = True
            canvas.itemconfig(spaceShip, image=cat0)

        # laser hit nothing keep traveling to right
        else:
            pace = 0
            # speed of laser
            if movementTag == "up_down":
                pace = 25
            elif movementTag == "circular":
                pace = 8.5
            elif movementTag == "spam":
                pace = 3.25
            elif movementTag == "idek":
                pace = 8.5
            canvas.move(myLaser, pace, 0)


def immunityFlasher(movementTag):
    # flashes for 1 second
    color = ""
    if movementTag == "up_down":
        color = "blue"
    elif movementTag == "circular":
        color = "red"
    elif movementTag == "spam":
        color = "purple"
    elif movementTag == "idek":
        color = "green"
    for i in range(3):
        if i % 2 != 0:
            canvas.itemconfig(enemyShip, fill="white")
        else:
            canvas.itemconfig(enemyShip, fill=color)
        root.update()
        sleep(0.25)


def getmyCoords():
    myCoords = canvas.coords(spaceShip)
    myCoords.append(myCoords[0] + 17.5)
    myCoords.append(myCoords[1] + 17.5)
    return myCoords


def shipsCollision():
    global spaceShipHealth
    global spaceShipHit
    global movementTag
    myCoords = getmyCoords()

    if overlapping(canvas.coords(enemyShip), myCoords) is True:
        # grant 1 seconds of immunity
        timeDiff = (datetime.now() - spaceShipHit).seconds

        # only take away health if got hit 1s ago
        if timeDiff > 0.5:
            spaceShipHit = datetime.now()
            spaceShipHealth = spaceShipHealth - 1
            # update amount of hearts
            spaceShipHealthList.clear()

            for i in range(spaceShipHealth):
                spaceShipHealthList.append("\u2764")
            canvas.itemconfig(spaceShipHealthText, text=spaceShipHealthList)
            # if health = 0 then lost

            if spaceShipHealth < 1:
                gameLost()
        else:
            immunityFlasher("game")


def enemyShipFiringSequence(bullet, pos, pace, movementTag, isReturning):
    global lastFired
    global spaceShipHealth
    global lastInjured

    if checkFire(lastFired, movementTag, isReturning):
        if movementTag == "idek":
            # five bombs
            # bomb N
            bullet.append(
                canvas.create_oval(pos[0] + 5, pos[1] + 25, pos[2] - 5,
                                   pos[1] + 5, fill="pink", tags="N"))
            # bomb NW
            bullet.append(canvas.create_oval(pos[0] - 22.5, pos[1] - 22.5,
                                             pos[0] - 2.5, pos[1] - 2.5,
                                             fill="pink", tags="NW"))
            # bomb W
            bullet.append(
                canvas.create_oval(pos[0] + 25, pos[1] + 5, pos[0] - 5,
                                   pos[3] - 5, fill="pink", tags="W"))
            # bomb SW
            bullet.append(canvas.create_oval(pos[0] - 22.5, pos[3] + 22.5,
                                             pos[0] - 2.5, pos[3] + 2.5,
                                             fill="pink", tags="SW"))
            # bomb S
            bullet.append(
                canvas.create_oval(pos[0] + 5, pos[3] + 2.5, pos[2] - 5,
                                   pos[3] + 22.5, fill="pink", tags="S"))
            lastFired = datetime.now()
        else:
            # three lasers
            bullet.append(canvas.create_rectangle(pos[0] - 40, pos[1] - 15,
                                                  pos[0] - 5, pos[1] - 7.5,
                                                  fill="pink"))
            bullet.append(canvas.create_rectangle(pos[0] - 40, pos[1] + 7.5,
                                                  pos[0] - 5, pos[3] - 7.5,
                                                  fill="pink"))
            bullet.append(canvas.create_rectangle(pos[0] - 40, pos[3] + 7.5,
                                                  pos[0] - 5, pos[3] + 15,
                                                  fill="pink"))
            lastFired = datetime.now()

    if len(bullet) > 0:
        for i in bullet:
            a = False
            b = False
            hitSomething = False
            myCoords = getmyCoords()

            if hitSomething is False:
                a = overlapping(canvas.coords(i), myCoords)
                if movementTag == "idek":
                    b = hitWall(canvas.coords(i), "", True)
                else:
                    b = hitWall(canvas.coords(i), "left", False)

                # if hit me
                if a is True:
                    timeDiff = (datetime.now() - lastInjured).seconds
                    canvas.delete(i)
                    bullet.remove(i)
                    if timeDiff > 1.5:
                        spaceShipHealth = spaceShipHealth - 1
                        # update amount of hearts
                        lastInjured = datetime.now()
                        spaceShipHealthList.clear()
                        for i in range(spaceShipHealth):
                            spaceShipHealthList.append("\u2764")
                        canvas.itemconfig(spaceShipHealthText,
                                          text=spaceShipHealthList)
                        root.update()
                        # if health = 0 then lost
                        if spaceShipHealth < 1:
                            gameLost()
                        else:
                            immunityFlasher(movementTag)

                # laser hit wall
                elif b is True:
                    canvas.delete(i)
                    bullet.remove(i)
                    root.update()

                # laser hit nothing keep traveling
                else:
                    if movementTag == "idek":
                        temp = 0
                        while temp == 0:
                            temp = random.randint(-10, 10)

                        temp_2 = 0
                        while temp_2 == 0:
                            temp_2 = random.randint(-5, 5)

                        tag = canvas.gettags(i)
                        if tag[0] == "N":
                            canvas.move(i, temp, -pace)
                        elif tag[0] == "NW":
                            canvas.move(i, temp_2 - pace, temp_2 - pace)
                        elif tag[0] == "W":
                            canvas.move(i, -pace, temp_2)
                        elif tag[0] == "SW":
                            canvas.move(i, temp_2 - pace, temp_2 + pace)
                        elif tag[0] == "S":
                            canvas.move(i, temp_2, pace)
                        root.update()
                    else:
                        canvas.move(i, pace, 0)
                    root.update()


def checkFire(lastFired, movementTag, isReturning):
    time_D = (datetime.now() - lastFired).seconds

    # cool down for firing laser
    if isReturning is False:
        if movementTag == "up_down":
            if (time_D > 1.25):
                return True
            else:
                return False
        elif movementTag == "circular":
            if (time_D > 0.85):
                return True
            else:
                return False
        elif movementTag == "spam":
            if (time_D > 0.001):
                return True
            else:
                return False
        elif movementTag == "idek":
            if (time_D > 0.5):
                return True
            else:
                return False
    else:
        return False


def up_down():
    global lastFired
    global reloaded
    isReturning = False
    movementTag = "up_down"
    canvas.itemconfig(enemyShip, fill="blue")
    root.update()

    pace = random.randint(3, 6)
    pos = canvas.coords(enemyShip)
    laser = []
    laser_pace = -6
    laser.append(canvas.create_rectangle(pos[0] - 40, pos[1] - 15, pos[0] - 5,
                                         pos[1] - 7.5, fill="pink"))
    laser.append(canvas.create_rectangle(pos[0] - 40, pos[1] + 7.5, pos[0] - 5,
                                         pos[3] - 7.5, fill="pink"))
    laser.append(canvas.create_rectangle(pos[0] - 40, pos[3] + 7.5, pos[0] - 5,
                                         pos[3] + 15, fill="pink"))
    lastFired = datetime.now()
    bounce_count = 0
    while (bounce_count < 5):
        if paused is False and boss_en is False:
            if reloaded is False:
                checkMyLaser(movementTag)
            pos = canvas.coords(enemyShip)
            enemyShipFiringSequence(
                                    laser, pos, laser_pace, movementTag,
                                    isReturning
                                    )

            # if reached top/bottom then move to bottom/top
            if pos[3] > 690 or pos[1] < 70:
                pace = -pace
                bounce_count += 1
            canvas.move(enemyShip, 0, pace)
            sleep(0.02)
            root.update()
            shipsCollision()

    laser_pace = -3
    isReturning = True
    notDone = True

    while notDone or len(laser) > 0:
        if paused is False and boss_en is False:
            if reloaded is False:
                checkMyLaser(movementTag)
            pos = canvas.coords(enemyShip)

            if round(pos[3]) > height / 2 + enemyShipSize / 2:
                canvas.move(enemyShip, 0, -1)

            elif round(pos[3]) < height / 2 + enemyShipSize / 2:
                canvas.move(enemyShip, 0, 1)
            enemyShipFiringSequence(
                                    laser, pos, laser_pace, movementTag,
                                    isReturning
                                    )
            shipsCollision()

            if round(pos[3]) == height / 2 + enemyShipSize / 2:
                canvas.coords(
                              enemyShip, width - 10 - enemyShipSize,
                              height / 2 - enemyShipSize / 2, width - 10,
                              height / 2 + enemyShipSize / 2
                              )
                notDone = False
            sleep(0.00375)
            root.update()


def circular():
    isReturning = False

    # starting x,y of the orbit
    x = width / 2 + 250
    y = height / 2 - enemyShipSize / 2
    movementTag = "circular"
    canvas.itemconfig(enemyShip, fill="red")

    # move enemyShip to orbit center
    pos = canvas.coords(enemyShip)
    while pos[0] > width / 2 + 250:
        if paused is False and boss_en is False:
            if reloaded is False:
                checkMyLaser(movementTag)
            canvas.move(enemyShip, -1, 0)
            sleep(0.005)
            root.update()
            shipsCollision()
            pos = canvas.coords(enemyShip)

    # Greater E = more circular
    E = 500
    dtheta = (2 * math.pi) / E

    # how big the orbit
    radius = 150

    # center of obit
    xc = x - radius
    yc = y

    laser = []
    laser.append(canvas.create_rectangle(pos[0] - 40, pos[1] - 15, pos[0] - 5,
                                         pos[1] - 7.5, fill="pink"))
    laser.append(canvas.create_rectangle(pos[0] - 40, pos[1] + 7.5, pos[0] - 5,
                                         pos[3] - 7.5, fill="pink"))
    laser.append(canvas.create_rectangle(pos[0] - 40, pos[3] + 7.5, pos[0] - 5,
                                         pos[3] + 15, fill="pink"))
    lastFired = datetime.now()
    timeofOrbit = 0
    e = 0

    for timeofOrbit in range(5):
        theta = 0
        if e == 500:
            e = 0
        while e < E:
            if paused is False and boss_en is False:
                if reloaded is False:
                    checkMyLaser(movementTag)
                pos = canvas.coords(enemyShip)
                laser_pace = -3
                enemyShipFiringSequence(
                                        laser, pos, laser_pace, movementTag,
                                        isReturning
                                        )

                # calculate new coord in the orbit
                theta += dtheta
                x = radius * math.cos(theta) + xc
                y = radius * math.sin(theta) + yc

                # get coord of enemyShip
                x0, y0, x1, y1 = canvas.coords(enemyShip)

                # get current center point
                current_x, current_y = (x0 + x1) // 2, (y0 + y1) // 2

                # calculate how much to move to next orbit coord
                dx, dy = x - current_x, y - current_y

                # move to next orbit coor
                canvas.move(enemyShip, dx, dy)
                sleep(0.005)
                root.update()
                shipsCollision()
                e += 1

    # return to inital position
    isReturning = True
    laser_pace = -5
    pos = canvas.coords(enemyShip)
    while pos[2] < width - 15 or len(laser) > 0:
        if paused is False and boss_en is False:
            if reloaded is False:
                checkMyLaser(movementTag)

            if pos[2] < width - 15:
                canvas.move(enemyShip, 10, 0)

            if len(laser) > 0:
                enemyShipFiringSequence(
                                        laser, pos, laser_pace, movementTag,
                                        isReturning
                                        )
            sleep(0.02)
            root.update()
            pos = canvas.coords(enemyShip)
            shipsCollision()


def spam():
    global lastFired
    global reloaded
    isReturning = False
    movementTag = "spam"
    canvas.itemconfig(enemyShip, fill="purple")
    root.update()

    pace = 1
    pos = canvas.coords(enemyShip)
    laser = []
    laser_pace = -2.5
    laser.append(canvas.create_rectangle(pos[0] - 40, pos[1] - 15, pos[0] - 5,
                                         pos[1] - 7.5, fill="pink"))
    laser.append(canvas.create_rectangle(pos[0] - 40, pos[1] + 7.5, pos[0] - 5,
                                         pos[3] - 7.5, fill="pink"))
    laser.append(canvas.create_rectangle(pos[0] - 40, pos[3] + 7.5, pos[0] - 5,
                                         pos[3] + 15, fill="pink"))
    lastFired = datetime.now()
    bounce_count = 0

    while (bounce_count < 5):
        if paused is False and boss_en is False:
            if reloaded is False:
                checkMyLaser(movementTag)
            pos = canvas.coords(enemyShip)
            enemyShipFiringSequence(
                                    laser, pos, laser_pace, movementTag,
                                    isReturning
                                    )
            # if reached top/bottom then move to bottom/top
            if pos[3] > 690 or pos[1] < 70:
                pace = -pace
                bounce_count += 1
            canvas.move(enemyShip, 0, pace)
            sleep(0.001)
            root.update()
            shipsCollision()

    isReturning = True
    notDone = True

    while notDone or len(laser) > 0:
        if paused is False and boss_en is False:
            if reloaded is False:
                checkMyLaser(movementTag)
            pos = canvas.coords(enemyShip)

            if round(pos[3]) > height / 2 + enemyShipSize / 2:
                canvas.move(enemyShip, 0, -1)

            elif round(pos[3]) < height / 2 + enemyShipSize / 2:
                canvas.move(enemyShip, 0, 1)
            enemyShipFiringSequence(
                                    laser, pos, laser_pace, movementTag,
                                    isReturning
                                    )
            shipsCollision()

            if round(pos[3]) == height / 2 + enemyShipSize / 2:
                canvas.coords(enemyShip, width - 10 - enemyShipSize,
                              height / 2 - enemyShipSize / 2, width - 10,
                              height / 2 + enemyShipSize / 2)
                notDone = False
            sleep(0.00125)
            root.update()


def idek():
    isReturning = False

    # starting x,y of the orbit
    x = width / 2 + 350
    y = height / 2 - enemyShipSize / 2
    movementTag = "idek"
    canvas.itemconfig(enemyShip, fill="green")

    # move enemyShip to orbit center
    pos = canvas.coords(enemyShip)
    while ((pos[0] + pos[2]) / 2 > width / 2 + 350):
        if paused is False and boss_en is False:
            if reloaded is False:
                checkMyLaser(movementTag)
            canvas.move(enemyShip, -1.5, 0)
            sleep(0.005)
            root.update()
            shipsCollision()
            pos = canvas.coords(enemyShip)

    # Greater E = more circular
    E = 500
    dtheta = (2 * math.pi) / E

    # how big the orbit
    radius = 70

    # center of obit
    xc = x - radius
    yc = y

    pace = 3
    pos = canvas.coords(enemyShip)

    bomb = []
    bomb_pace = 2
    # bomb size = 20width 20height
    # bomb N
    bomb.append(
        canvas.create_oval(pos[0] + 5, pos[1] + 25, pos[2] - 5, pos[1] + 5,
                           fill="pink", tags="N"))
    # bomb NW
    bomb.append(
        canvas.create_oval(pos[0] - 22.5, pos[1] - 22.5, pos[0] - 2.5,
                           pos[1] - 2.5, fill="pink", tags="NW"))
    # bomb W
    bomb.append(
        canvas.create_oval(pos[0] + 25, pos[1] + 5, pos[0] - 5, pos[3] - 5,
                           fill="pink", tags="W"))
    # bomb SW
    bomb.append(
        canvas.create_oval(pos[0] - 22.5, pos[3] + 22.5, pos[0] - 2.5,
                           pos[3] + 2.5, fill="pink", tags="SW"))
    # bomb S
    bomb.append(
        canvas.create_oval(pos[0] + 5, pos[3] + 2.5, pos[2] - 5, pos[3] + 22.5,
                           fill="pink", tags="S"))
    lastFired = datetime.now()
    timeofOrbit = 0
    e = 0

    for timeofOrbit in range(5):
        theta = 0
        if e == 500:
            e = 0
        while e < E:
            if paused is False and boss_en is False:
                if reloaded is False:
                    checkMyLaser(movementTag)
                pos = canvas.coords(enemyShip)
                enemyShipFiringSequence(
                                        bomb, pos, bomb_pace, movementTag,
                                        isReturning
                                        )

                # calculate new coord in the orbit
                theta += dtheta
                x = radius * math.cos(theta) + xc
                y = radius * math.sin(theta) + yc

                # get coord of enemyShip
                x0, y0, x1, y1 = canvas.coords(enemyShip)

                # get current center point
                current_x, current_y = (x0 + x1) // 2, (y0 + y1) // 2

                # calculate how much to move to next orbit coord
                dx, dy = x - current_x, y - current_y

                # move to next orbit coor
                canvas.move(enemyShip, dx, dy)
                sleep(0.01)
                root.update()
                shipsCollision()
                e += 1

    # return to inital position
    isReturning = True
    pos = canvas.coords(enemyShip)
    while (pos[2] < width - 15 or len(bomb) > 0):
        if paused is False and boss_en is False:
            if reloaded is False:
                checkMyLaser(movementTag)

            if pos[2] < width - 15:
                canvas.move(enemyShip, 10, 0)

            if len(bomb) > 0:
                bomb_pace = 4
                enemyShipFiringSequence(
                                        bomb, pos, bomb_pace, movementTag,
                                        isReturning
                                        )
            sleep(0.02)
            root.update()
            pos = canvas.coords(enemyShip)
            shipsCollision()


def enemyMovement():
    global gameStartTime
    gameStartTime = time.time()
    global gameFinished
    while gameFinished is False:
        idek()
        spam()
        circular()
        up_down()


def overlapping(a, b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False


def hitWall(coords, direction, isBomb):
    if isBomb:
        if ((coords[0] > 15) and (coords[1] > 67.5) and (coords[2] < 987.5) and
           (coords[3] < 685)):
            return False
        else:
            return True
    else:
        if direction == "left":
            if coords[0] > 15:
                return False
            else:
                return True
        elif direction == "right":
            if coords[2] < 987.5:
                return False
            else:
                return True
        elif direction == "up":
            if coords[1] > 67.5:
                return False
            else:
                return True
        elif direction == "down":
            if coords[3] < 685:
                return False
            else:
                return True


def spaceKey(event):
    global reloaded
    global cat1
    global myLaser

    # only one laser can exist
    if reloaded is True:
        canvas.itemconfig(spaceShip, image=cat1)
        reloaded = False
        uShip = getmyCoords()
        x0, y0, x1, y1 = uShip
        myLaser = canvas.create_rectangle(x1 + 5, y0 - 7.5, x1 + 40, y1 - 7.5,
                                          fill="yellow")
    else:
        pass


def leftKey(event):
    if paused is False:
        x = -15
        y = 0
        myCoords = getmyCoords()
        wall_collision = hitWall(myCoords, "left", False)
        if wall_collision is False:
            canvas.move(spaceShip, x, y)


def rightKey(event):
    if paused is False:
        x = 15
        y = 0
        myCoords = getmyCoords()
        wall_collision = hitWall(myCoords, "right", False)
        if wall_collision is False:
            canvas.move(spaceShip, x, y)


def upKey(event):
    if paused is False:
        x = 0
        y = -15
        myCoords = getmyCoords()
        wall_collision = hitWall(myCoords, "up", False)
        if wall_collision is False:
            canvas.move(spaceShip, x, y)


def downKey(event):
    if paused is False:
        x = 0
        y = 15
        myCoords = getmyCoords()
        wall_collision = hitWall(myCoords, "down", False)
        if wall_collision is False:
            canvas.move(spaceShip, x, y)


def bossKey(event):
    global gameState
    global boss_en
    global boss_screen
    if ((gameState != "menu") and (gameState != "paused") and
       (gameState != "won") and
       (gameState != "lost")):
        if boss_en is False:
            boss_en = True
            gameState = "boss"
            root.title("boss im wokring plz")
            boss_screen = canvas.create_image(width/2, height/2, image=work)
        else:
            boss_en = False
            gameState = "game"
            root.title("Meow.py")
            canvas.delete(boss_screen)


def pauseKey(event):
    global gameState
    global paused
    global pause_text
    if ((gameState != "menu") and (gameState != "boss") and
       (gameState != "won") and
       (gameState != "lost")):
        if paused is False:
            paused = True
            gameState = "paused"
            pause_text = canvas.create_text(width / 2, height / 2,
                                            fill="white",
                                            font="Times 20 italic bold",
                                            text="Paused")
        else:
            paused = False
            gameState = "game"
            canvas.delete(pause_text)


def cheatKey(event):
    global gameState
    if gameState == "game":
        global spaceShipHealth
        global cheated
        if spaceShipHealth < 15:
            cheated = True
            spaceShipHealth = spaceShipHealth + 1
            # update amount of hearts
            spaceShipHealthList.clear()
            for i in range(spaceShipHealth):
                spaceShipHealthList.append("\u2764")
            canvas.itemconfig(spaceShipHealthText, text=spaceShipHealthList)
            root.update()


# Key press events
root.bind("<Left>", leftKey)
root.bind("<Right>", rightKey)
root.bind("<Up>", upKey)
root.bind("<Down>", downKey)

root.bind("<b>", bossKey)
root.bind("<B>", bossKey)

root.bind("<p>", pauseKey)
root.bind("<P>", pauseKey)

root.bind("<Right><Left><Right><C>", cheatKey)
root.bind("<Right><Left><Right><c>", cheatKey)

# Fire laser when space is pressed
root.bind("<space>", spaceKey)


def game_ini():
    # refersh widgets
    canvas.delete("all")
    btn_start.destroy()
    # update state
    global gameState
    gameState = "game"
    # widgets gen
    canvas.create_image(width/2, height/2, image=game_bg)
    global spaceShip
    spaceShip = canvas.create_image(10, height / 2 - spaceShipSize / 2,
                                    image=cat0)
    global myLaser
    myLaser = canvas.create_rectangle(0, 0, 0, 0)
    global enemyShip
    enemyShip = canvas.create_rectangle(width - 10 - enemyShipSize,
                                        height / 2 - enemyShipSize / 2,
                                        width - 10,
                                        height / 2 + enemyShipSize / 2,
                                        fill="blue")
    global spaceShipHealthText
    spaceShipHealthText = canvas.create_text(width / 2, 50, fill="red",
                                             text=spaceShipHealthList)
    global enemyShipHealthText
    enemyShipHealthText = canvas.create_text(width - 100, 50, fill="white",
                                             text=str(enemyShipHealth) + "/" +
                                             str(enemyShipHealth))
    canvas.create_text(48, 10, fill="white", font="Airal 10",
                       text="[P] - Pause")
    canvas.create_text(44, 25, fill="white", font="Airal 10",
                       text="[B] - Boss")
    # canvas.create_text(75, 40, fill="white", font="Airal 10",
    #                    text="[C] - Cheat for health")
    canvas.create_text(80, 40, fill="white", font="Airal 10",
                       text="[Arrorw] - Move around")
    canvas.create_text(76, 55, fill="white", font="Airal 10",
                       text="[Space] - Shoot laser")

    # multithreading so that two functions can ran at same time when paused
    t1 = threading.Thread(target=enemyMovement)
    t1.start()
    canvas.focus_set()
    canvas.pack()


def menu():
    gameState = "menu"
    canvas.pack()
    canvas.create_image(width/2, height/2, image=menu_bg)
    btn_start.place(x=width / 2 - 90, y=height - 250)
    btn_start['command'] = game_ini


menu()
root.mainloop()

# Image Reference
# cat0.png & cat1
# Wide-Mouthed Singing Cat [Digital Image]. (2020). Retrieved from
# https://knowyourmeme.com/memes/wide-mouthed-singing-cat
# _________________________________________________________________
# work.png
# Screenshot of MS Excel [Digital Image]. (2020). Pak's
# private collection
# _________________________________________________________________
# menu_bg.png
# Meow.py menu background image [Digital Image]. (2020). Pak's
# private collection
# _________________________________________________________________
# game_bg.png
# Game background image [Digital Image]. (2020). Pak's
# private collection
# _________________________________________________________________
# lost_bg.png
# Lost background image [Digital Image]. (2020). Pak's
# private collection
# _________________________________________________________________
# won_bg.png
# won background image [Digital Image]. (2020). Pak's
# private collection
# _________________________________________________________________
# ldrboard_bg.png
# Leaderboard background image [Digital Image]. (2020). Pak's
# private collection
# _________________________________________________________________
# End
