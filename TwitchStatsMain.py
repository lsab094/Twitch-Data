import sqlite3, pandas as pd, numpy as np, matplotlib.pyplot as plt

con = sqlite3.connect("TwitchData.db")
curs = con.cursor()

def CSVtoDB(fileName, tabName):
    file = pd.read_csv(fileName)
    file.columns = file.columns.str.replace('_', '')
    file.to_sql(tabName, con, if_exists='append', index = False)

# run once
# CSVtoDB('StreamerData.csv', 'StreamerTable')
# CSVtoDB('GameData.csv', 'GamesTable')
# CSVtoDB('MonthlyData.csv', 'MonthsTable')

#

def topPlots(xArray, yArray, xLabel, yLabel, title):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bars = ax.bar(xArray, np.round(yArray, 2), color=['red', 'orange', 'gold', 'limegreen', 'blue', 'purple'])
    ax.set_xticklabels(xArray, rotation='vertical')
    ax.bar_label(bars, padding=2, rotation='vertical')
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    plt.title(title, fontsize=10)
    plt.tight_layout()
    plt.show()

def plotFunc(yUnit, xLabel, yLabel, title):
    xVar = np.array([])
    yVar = np.array([])
    for row in curs.fetchmany(25):
        row0 = str(row[0])
        if row0.isdigit() == True:
            row0 = monthNum(row0)
        xVar = np.append(xVar, str(row0))
        row1 = (row[1] / yUnit)
        yVar = np.append(yVar, row1)
    topPlots(xVar, yVar, xLabel, yLabel, title)

def streamerPlots(yArray, varName1, varName2, xLabel, yLabel, title, plotNum):
    xArray = [varName1, varName2]
    fig = plt.figure(1)
    ax = fig.add_subplot(2,2,plotNum)
    bars = ax.bar(xArray, np.round(yArray, 2), color=['red', 'blue'])
    ax.set_xticklabels(xArray)
    ax.bar_label(bars, padding=2)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    plt.title(title, fontsize=10)

def streamerPlotFunc(yUnit, var1, var2, xLabel, yLabel, title, plotNum):
    xVar = np.array([])
    yVar = np.array([])
    for row in curs.fetchall():
        xVar = np.append(xVar, str(row[0]))
        row1 = (row[1] / yUnit)
        yVar = np.append(yVar, row1)
    streamerPlots(yVar, var1, var2, xLabel, yLabel, title, plotNum)\

def linePlots(xArray, yArray, xLabel, yLabel, title):
    plt.plot(xArray, yArray)
    plt.xticks(rotation=90)
    for x, y in zip(xArray, yArray):
        label = str(np.round(y, 2))
        plt.annotate(label, (x, y), rotation=90, fontsize=8)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title, fontsize=10)
    plt.plot()
    plt.show()

def gamePlotFunc(yUnit, xLabel, yLabel, title):
    xVar = np.array([])
    yVar = np.array([])
    for row in curs.fetchall():
        xVar = np.append(xVar, (str(row[0]) + " " + "(" + (str(row[1]) + ")")))
        r = str(row[2]).split(' ')
        row2 = (int(r[0]) / yUnit)
        yVar = np.append(yVar, row2)
    linePlots(xVar, yVar, xLabel, yLabel, title)

def monthNum(month):
    monthName = ''
    if month == '1':
        monthName = "January"
    if month == '2':
        monthName = "February"
    if month == '3':
        monthName = "March"
    if month == '4':
        monthName = "April"
    if month == '5':
        monthName = "May"
    if month == '6':
        monthName = "June"
    if month == '7':
        monthName = "July"
    if month == '8':
        monthName = "August"
    if month == '9':
        monthName = "September"
    if month == '10':
        monthName = "October"
    if month == '11':
        monthName = "November"
    if month == '12':
        monthName = "December"
    return monthName

def monthPlotFunc(yUnit, xLabel, yLabel, title):
    xVar = np.array([])
    yVar = np.array([])
    for row in curs.fetchall():
        xVar = np.append(xVar, (str(row[0])))
        r = str(row[1]).split(' ')
        row2 = (int(r[0]) / yUnit)
        yVar = np.append(yVar, row2)
    linePlots(xVar, yVar, xLabel, yLabel, title)

#

def plotStreamersByWatchtime():
    curs.execute("""
    SELECT Channel, Watchtime
    FROM StreamerTable 
    ORDER BY Watchtime DESC
    """)
    plotFunc(60000000, "Streamers", "Hours Watched (Millions)", "Top 25 Streamers by Total Hours Watched")

def plotStreamersByStreamtime():
    curs.execute("""
    SELECT Channel, StreamTime
    FROM StreamerTable 
    ORDER BY StreamTime DESC
    """)
    plotFunc(60000, "Streamers", "Hours Streamed (Thousands)", "Top 25 Streamers by Total Hours Streamed")

def plotStreamersByAvgViews():
    curs.execute("""
    SELECT Channel, Averageviewers
    FROM StreamerTable 
    ORDER BY Averageviewers DESC
    """)
    plotFunc(1000, "Streamers", "Average Viewers (Thousands)", "Top 25 Streamers by Average Viewers per Stream")

def plotStreamersByFollowers():
    curs.execute("""
    SELECT Channel, Followers
    FROM StreamerTable 
    ORDER BY Followers DESC
    """)
    plotFunc(1000000, "Streamers", "Followers (Millions)", "Top 25 Streamers by Total Followers")

def plotPartnerStatus():
    curs.execute("""
        SELECT Partnered, avg(Watchtime)
        FROM StreamerTable 
        GROUP BY Partnered
        ORDER BY Partnered
        """)
    streamerPlotFunc(1000000, "Not Partnered", "Partnered", "Partner Status", "Hours Watched (Millions)",
                     "Average Hours Watched by Partner Status", 1)
    curs.execute("""
        SELECT Partnered, avg(Streamtime)
        FROM StreamerTable 
        GROUP BY Partnered
        ORDER BY Partnered
        """)
    streamerPlotFunc(1000, "Not Partnered", "Partnered", "Partner Status", "Hours Streamed (Thousands)",
                     "Average Hours Streamed by Partner Status", 2)
    curs.execute("""
    SELECT Partnered, avg(Averageviewers)
        FROM StreamerTable 
        GROUP BY Partnered
        ORDER BY Partnered
        """)
    streamerPlotFunc(1000, "Not Partnered", "Partnered", "Partner Status", "Average Views (Thousands)",
                     "Average Views by Partner Status", 3)
    curs.execute("""
        SELECT Partnered, avg(Followers)
        FROM StreamerTable 
        GROUP BY Partnered
        ORDER BY Partnered
        """)
    streamerPlotFunc(1000, "Not Partnered", "Partnered", "Partner Status", "Followers (Thousands)",
                     "Average Followers by Partner Status", 4)
    plt.show()

def plotAgeRating():
    curs.execute("""
        SELECT Mature, avg(Watchtime)
        FROM StreamerTable 
        GROUP BY Mature
        ORDER BY Mature
        """)
    streamerPlotFunc(1000000, "All Ages", "18+", "Rating", "Hours Watched (Millions)",
                     "Average Hours Watched by Age Rating", 1)
    curs.execute("""
            SELECT Mature, avg(Streamtime)
            FROM StreamerTable 
            GROUP BY Mature
            ORDER BY Mature
            """)
    streamerPlotFunc(1000, "All Ages", "18+", "Rating", "Hours Streamed (Thousands)",
                     "Average Hours Streamed by Age Rating", 2)
    curs.execute("""
                SELECT Mature, avg(Averageviewers)
                FROM StreamerTable 
                GROUP BY Mature
                ORDER BY Mature
                """)
    streamerPlotFunc(1000, "All Ages", "18+", "Rating", "Average Views (Thousands)",
                     "Average Views by Age Rating", 3)
    curs.execute("""
                    SELECT Mature, avg(Followers)
                    FROM StreamerTable 
                    GROUP BY Mature
                    ORDER BY Mature
                    """)
    streamerPlotFunc(1000, "All Ages", "18+", "Rating", "Followers (Thousands)",
                     "Average Followers by Age Rating", 4)
    plt.show()

def plotLangsbyWatchtime():
    curs.execute("""
        SELECT Language, avg(Watchtime)
        FROM StreamerTable
        GROUP BY Language 
        ORDER BY avg(Watchtime) DESC
        """)
    plotFunc(60000000, "Langauges", "Average Hours Watched (Millions)", "Average Hours Watched of Top 1000 Streamers by Language")

def plotLangsbyStreamtime():
    curs.execute("""
        SELECT Language, avg(Streamtime)
        FROM StreamerTable
        GROUP BY Language 
        ORDER BY avg(Streamtime) DESC
        """)
    plotFunc(60000, "Langauges", "Average Hours Streamed (Thousands)", "Average Hours Streamed of Top 1000 Streamers by Language")

def plotLangsbyAvgViews():
    curs.execute("""
        SELECT Language, avg(Averageviewers)
        FROM StreamerTable
        GROUP BY Language 
        ORDER BY avg(Averageviewers) DESC
        """)
    plotFunc(1000, "Langauges", "Average Viewers (Thousands)", "Average Viewers of Top 1000 Streamers by Language")

def plotLangsbyFollowers():
    curs.execute("""
        SELECT Language, avg(Followers)
        FROM StreamerTable
        GROUP BY Language 
        ORDER BY avg(Followers) DESC
        """)
    plotFunc(1000, "Langauges", "Followers (Thousands)", "Average Followers of Top 1000 Streamers by Language")

def plotGamesByWatchtime():
    curs.execute("""
    SELECT Game, avg(Hourswatched)
    FROM GamesTable
    GROUP BY Game
    ORDER BY avg(Hourswatched) DESC
    """)
    plotFunc(1000000, "Games", "Average Hours Watched (Millions)", "Top 25 Games by Hours Watched per Month")

def plotGamesByStreamtime():
    curs.execute("""
    SELECT Game, avg(HoursStreamed)
    FROM GamesTable
    GROUP BY Game
    ORDER BY avg(HoursStreamed) DESC
    """)
    plotFunc(1000000, "Games", "Average Hours Streamed (Millions)", "Top 25 Games by Hours Streamed per Month")

def plotGamesByAvgViews():
    curs.execute("""
        SELECT Game, avg(Avgviewers)
        FROM GamesTable
        GROUP BY Game
        ORDER BY avg(Avgviewers) DESC
        """)
    plotFunc(1000, "Games", "Average Viewers (Thousands)", "Top 25 Games by Average Viewers per Month")

def plotLineGameWatchtime(game):
    curs.execute(("""
           SELECT Year, Month, HoursWatched, Game
           FROM GamesTable
           WHERE Game = ?
           ORDER BY Year, Month
           """), (game,))
    if curs.fetchone() == None:
        print("\nGame has not reached the top 150.")
    else:
        gamePlotFunc(1000000, "Years (Month)", "Hours Watched (Millions)", "Total Hours Watched by Month: " + game)

def plotLineGameStreamtime(game):
    curs.execute(("""
           SELECT Year, Month, HoursStreamed
           FROM GamesTable
           WHERE Game = ?
           ORDER BY Year, Month
           """), (game,))
    if curs.fetchone() == None:
        print("\nGame has not reached the top 150.")
    else:
        gamePlotFunc(1000000, "Years (Month)", "Hours Streamed (Millions)", "Total Hours Streamed by Month: " + game)

def plotLineGameAvgviews(game):
    curs.execute(("""
           SELECT Year, Month, Avgviewers
           FROM GamesTable
           WHERE Game = ?
           ORDER BY Year, Month
           """), (game,))
    if curs.fetchone() == None:
        print("\nGame has not reached the top 150.")
    else:
        gamePlotFunc(1000, "Years (Month)", "Average Viewers (Thousands)", "Average Viewers by Month: " + game)

def plotMonthsByWatchtime():
    curs.execute("""
    SELECT Month, avg(Hourswatched)
    FROM MonthsTable
    GROUP BY Month
    ORDER BY avg(Hourswatched) DESC
    """)
    plotFunc(1000000000, "Months", "Average Hours Watched (Billions)", "Months by Hours Watched")

def plotMonthsByStreams():
    curs.execute("""
    SELECT Month, avg(Streams)
    FROM MonthsTable
    GROUP BY Month
    ORDER BY avg(Streams) DESC
    """)
    plotFunc(1000000, "Months", "Average Streams (Millions)", "Months by Number of Streams")

def plotMonthsByAvgViews():
    curs.execute("""
        SELECT Month, avg(Avgviewers)
        FROM MonthsTable
        GROUP BY Month
        ORDER BY avg(Avgviewers) DESC
        """)
    plotFunc(1000000, "Months", "Average Viewers (Millions)", "Months by Average Viewers")

def plotLineMonthWatchtime(month):
    monthName = monthNum(month)
    curs.execute(("""
           SELECT year, HoursWatched
           FROM MonthsTable
           WHERE Month = ?
           ORDER BY year
           """), (month,))
    if curs.fetchone() == None:
        print("\nPlease enter the month number (i.e. January = 1) and try again.")
    else:
        monthPlotFunc(1000000000, "Years", "Hours Watched (Billions)", "Total Hours Watched by Year: " + monthName)

def plotLineMonthStreams(month):
    monthName = monthNum(month)
    curs.execute(("""
        SELECT year, Streams
        FROM MonthsTable
        WHERE Month = ?
        ORDER BY year
        """), (month,))
    if curs.fetchone() == None:
        print("\nPlease enter the month number (i.e. January = 1) and try again.")
    else:
        monthPlotFunc(1000000, "Years", "Streams (Millions)", "Total Streams by Year: " + monthName)

def plotLineMonthAvgviews(month):
    monthName = monthNum(month)
    curs.execute(("""
        SELECT year, Avgviewers
        FROM MonthsTable
        WHERE Month = ?
        ORDER BY year
        """), (month,))
    if curs.fetchone() == None:
        print("\nPlease enter the month number (i.e. January = 1) and try again.")
    else:
        monthPlotFunc(1000000, "Years", "Average Viewers (Millions)", "Average Viewers by Year: " + monthName)

#

def getStreamerStats(streamer):
    curs.execute(("""
        SELECT
            Channel,
            Watchtime,
            DENSE_RANK() over (ORDER BY Watchtime DESC) as watchRank,
            Streamtime,
            DENSE_RANK() over (ORDER BY Streamtime DESC) as streamRank,
            Averageviewers,
            DENSE_RANK() over (ORDER BY Averageviewers DESC) as viewRank,
            Followers,
            DENSE_RANK() over (ORDER BY Followers DESC) as followRank,
            Partnered, Mature, Language
        FROM StreamerTable
        """))
    for row in curs.fetchall():
        if row[0] == streamer:
            name = row[0]
            watchtime = str(np.round(row[1] / 60, 1))
            watchRank = str(row[2])
            streamtime = str(np.round(row[3] / 60, 1))
            streamRank = str(row[4])
            avgviews = str(row[5])
            viewRank = str(row[6])
            followers = str(row[7])
            followRank = str(row[8])
            if row[9] == 0:
                part = "No"
            else:
                part = "Yes"
            if row[10] == 0:
                rating = "All Ages"
            else:
                rating = "18+"
            lang = row[11]
            print("\nChannel Name: " + name +
                  "\nTotal Hours Watched: " + watchtime + " (Rank " + watchRank + ")" +
                  "\nTotal Hours Streamed: " + streamtime + " (Rank " + streamRank + ")" +
                  "\nAverage Views per Stream: " + avgviews + " (Rank " + viewRank + ")" +
                  "\nTotal Followers: " + followers + " (Rank " + followRank + ")" +
                  "\nTwitch Partnered? " + part +
                  "\nAge Rating: " + rating +
                  "\nLanguage: " + lang +
                  "\n")
            return
    if curs.fetchall() == []:
        print("\nStreamer is not in the top 1000.")

def getGameStats(game):
    curs.execute(("""
        SELECT
            Game,
            avg(Hourswatched),
            DENSE_RANK() over (ORDER BY avg(Hourswatched) DESC) as watchRank,
            avg(HoursStreamed),
            DENSE_RANK() over (ORDER BY avg(HoursStreamed) DESC) as streamRank,
            avg(Avgviewers),
            DENSE_RANK() over (ORDER BY avg(Avgviewers) DESC) as viewRank
        FROM GamesTable
        GROUP BY Game
        """))
    for row in curs.fetchall():
        if row[0] == game:
            name = row[0]
            watchtime = str(np.round(row[1], 1))
            watchRank = str(row[2])
            streamtime = str(np.round(row[3], 1))
            streamRank = str(row[4])
            avgviews = str(int(row[5]))
            viewRank = str(row[6])
            print("Game: " + name +
                  "\nAverage Hours Watched per Month: " + watchtime + " (Rank " + watchRank + ")" +
                  "\nAverage Hours Streamed per Month: " + streamtime + " (Rank " + streamRank + ")" +
                  "\nAverage Views per Month: " + avgviews + " (Rank " + viewRank + ")" +
                  "\n")
            return
    if curs.fetchall() == []:
        print("\nGame has not reached the top 150.")

def monthToStreamGame(game):
    curs.execute(("""
            SELECT Game, Month, Avgviewers, Avgchannels
            FROM GamesTable
            WHERE Game = ?
            GROUP BY Month
            ORDER BY Avgviewers DESC, Avgchannels ASC
            """), (game,))
    for row in curs.fetchall():
            name = row[0]
            month = monthNum(str(row[1]))
            views = int(row[2])
            channels = int(row[3])
            ratio = str(int(views/channels))
            print("\n" + name + " has the greatest viewer/channel ratio in " + month + ", at about " + ratio +
                  " viewers per channel.")
            return
    if curs.fetchall() == []:
        print("\nGame has not reached the top 150.")

def gameAndMonth(game, month):
    if month.isdigit() == False:
        print("\nPlease enter the month number (i.e. January = 1) and try again.")
        return
    elif int(month) < 1 or int(month) > 12:
        print("\nPlease enter the month number (i.e. January = 1) and try again.")
        return
    curs.execute(("""
        SELECT Game, Month, avg(Hourswatched), avg(HoursStreamed), avg(Avgviewers)
        FROM GamesTable
        WHERE Game = ? AND Month = ?
        GROUP BY Month
        """), (game, month,))
    for row in curs.fetchall():
        name = row[0]
        month = monthNum(str(row[1]))
        watchtime = str(np.round(row[2], 1))
        streamtime = str(np.round(row[3], 1))
        views = str(int(row[4]))
        print("\nStats for " + name + " in " + month +
              "\nAverage Hours Watched: " + watchtime +
              "\nAverage Hours Streamed: " + streamtime +
              "\nAverage Views: " + views +
              "\n")
        return
    if curs.fetchall() == []:
        print("\nGame has not reached the top 150.")

def getMonthStats(month):
    curs.execute(("""
        SELECT
            Month,
            avg(Hourswatched),
            DENSE_RANK() over (ORDER BY avg(Hourswatched) DESC) as watchRank,
            avg(Streams),
            DENSE_RANK() over (ORDER BY avg(Streams) DESC) as streamRank,
            avg(Avgviewers),
            DENSE_RANK() over (ORDER BY avg(Avgviewers) DESC) as viewRank
        FROM MonthsTable
        GROUP BY Month
        """))
    for row in curs.fetchall():
        if str(row[0]) == month:
            month = monthNum(str(row[0]))
            watchtime = str(np.round(row[1], 1))
            watchRank = str(row[2])
            streams = str(np.round(row[3], 1))
            streamRank = str(row[4])
            avgviews = str(int(row[5]))
            viewRank = str(row[6])
            print("\nMonth: " + month +
                  "\nAverage Hours Watched per Year: " + watchtime + " (Rank " + watchRank + ")" +
                  "\nAverage Streams per Year: " + streams + " (Rank " + streamRank + ")" +
                  "\nAverage Views per Year: " + avgviews + " (Rank " + viewRank + ")" +
                  "\n")
            return
    if curs.fetchall() == []:
        print("\nPlease enter the month number (i.e. January = 1) and try again.")

def gameToStreamDuringMonth(month):
    curs.execute(("""
        SELECT Month, Game, Avgviewers, Avgchannels
        FROM GamesTable
        WHERE Month = ?
        GROUP BY Game
        ORDER BY Avgviewers DESC, Avgchannels ASC
        """), (month,))
    for row in curs.fetchall():
        month = monthNum(str(row[0]))
        game = row[1]
        views = int(row[2])
        channels = int(row[3])
        ratio = str(int(views/channels))
        print("\nThe game with the greatest viewer/channel ratio in " + month + " is " + game + ", at about " + ratio +
              " viewers per channel.")
        return
    if curs.fetchall() == []:
        print("\nPlease enter the month number (i.e. January = 1) and try again.")

#

def mainMenu():
    print("\nMAIN MENU"
          "\nType in a number to view data and press Enter."
          "\n1. Streamer Data"
          "\n2. Game Data"
          "\n3. Monthly Data"
          "\n4. Exit")
    choice = input()
    if choice.isdigit() == False:
        print("\nPlease enter a number.")
        mainMenu()
    elif int(choice) == 1:
        streamerData()
    elif int(choice) == 2:
        gameData()
    elif int(choice) == 3:
        monthlyData()
    elif int(choice) == 4:
        quit()
    else:
        print("\nPlease enter a number.")
        mainMenu()

def streamerData():
    print("\nDATA FROM TOP 1000 STREAMERS (JAN 2016 - APR 2021)"
          "\nType in a number to view data and press Enter."
          "\n1. Top Streamers by Watch Time"
          "\n2. Top Streamers by Stream Time"
          "\n3. Top Streamers by Average Views"
          "\n4. Top Streamers By Followers"
          "\n5. Partnered vs Unpartnered Streamers"
          "\n6. Mature vs All Ages Streams"
          "\n7. Language Data"
          "\n8. Search by Channel Name"
          "\n9. Main Menu"
          "\n10. Exit")
    choice = input()
    if choice.isdigit() == False:
        print("\nPlease enter a number.")
        streamerData()
    elif int(choice) == 1:
        plotStreamersByWatchtime()
    elif int(choice) == 2:
        plotStreamersByStreamtime()
    elif int(choice) == 3:
        plotStreamersByAvgViews()
    elif int(choice) == 4:
        plotStreamersByFollowers()
    elif int(choice) == 5:
        plotPartnerStatus()
    elif int(choice) == 6:
        plotAgeRating()
    elif int(choice) == 7:
        langData()
    elif int(choice) == 8:
        print("\nSearch Channel Name (case sensitive): ")
        search = str(input())
        getStreamerStats(search)
    elif int(choice) == 9:
        mainMenu()
    elif int(choice) == 10:
        quit()
    else:
        print("\nPlease enter a number.")
        streamerData()
    streamerData()

def langData():
    print("\nLANGUAGE DATA FROM TOP 1000 STREAMERS (JAN 2016 - APR 2021)"
          "\nType in a number to view data and press Enter."
          "\n1. Languages by Watch Time"
          "\n2. Languages by Stream Time"
          "\n3. Languages by Average Views"
          "\n4. Languages By Followers"
          "\n5. Streamer Data"
          "\n6. Main Menu"
          "\n7. Exit")
    choice = input()
    if choice.isdigit() == False:
        print("\nPlease enter a number.")
        langData()
    elif int(choice) == 1:
        plotLangsbyWatchtime()
    elif int(choice) == 2:
        plotLangsbyStreamtime()
    elif int(choice) == 3:
        plotLangsbyAvgViews()
    elif int(choice) == 4:
        plotLangsbyFollowers()
    elif int(choice) == 5:
        streamerData()
    elif int(choice) == 6:
        mainMenu()
    elif int(choice) == 7:
        quit()
    else:
        print("\nPlease enter a number.")
        langData()
    langData()

def gameData():
    print("\nMONTHLY DATA FROM TOP 150 GAMES (JAN 2016 - APR 2021)"
          "\nType in a number to view data and press Enter."
          "\n1. Top Games by Watch Time"
          "\n2. Top Games by Stream Time"
          "\n3. Top Games by Average Views"
          "\n4. Search by Game Name (line graphs)"
          "\n5. Search by Game Name (stats)"
          "\n6. Search Stats by Game and Month"
          "\n7. Best Month to Stream Game?"
          "\n8. Main Menu"
          "\n9. Exit")
    choice = input()
    if choice.isdigit() == False:
        print("\nPlease enter a number.")
        gameData()
    elif int(choice) == 1:
        plotGamesByWatchtime()
    elif int(choice) == 2:
        plotGamesByStreamtime()
    elif int(choice) == 3:
        plotGamesByAvgViews()
    elif int(choice) == 4:
        gameLines()
    elif int(choice) == 5:
        print("\nSearch Game Name (case sensitive): ")
        search = str(input())
        getGameStats(search)
    elif int(choice) == 6:
        print("\nSearch Game Name (case sensitive): ")
        search1 = str(input())
        print("\nEnter Month Number (i.e. January = 1): ")
        search2 = str(input())
        gameAndMonth(search1, search2)
    elif int(choice) == 7:
        print("\nSearch Game Name (case sensitive): ")
        search = str(input())
        monthToStreamGame(search)
    elif int(choice) == 8:
        mainMenu()
    elif int(choice) == 9:
        quit()
    else:
        print("\nPlease enter a number.")
        gameData()
    gameData()

def gameLines():
    print("\nMONTHLY DATA FROM TOP 150 GAMES (JAN 2016 - APR 2021)"
          "\nType in a number to view graph and press Enter."
          "\n1. Graph Games by Watch Time"
          "\n2. Graph Games by Stream Time"
          "\n3. Graph Games by Average Views"
          "\n4. Game Data"
          "\n5. Main Menu"
          "\n6. Exit")
    choice = input()
    if choice.isdigit() == False:
        print("\nPlease enter a number.")
        gameLines()
    elif int(choice) == 1:
        print("\nSearch Game Name (case sensitive): ")
        search = str(input())
        plotLineGameWatchtime(search)
    elif int(choice) == 2:
        print("\nSearch Game Name (case sensitive): ")
        search = str(input())
        plotLineGameStreamtime(search)
    elif int(choice) == 3:
        print("\nSearch Game Name (case sensitive): ")
        search = str(input())
        plotLineGameAvgviews(search)
    elif int(choice) == 4:
        gameData()
    elif int(choice) == 5:
        mainMenu()
    elif int(choice) == 6:
        quit()
    else:
        print("\nPlease enter a number.")
        gameLines()
    gameLines()

def monthlyData():
    print("\nMONTHLY DATA FROM JAN 2016 - APR 2021"
          "\nType in a number to view data and press Enter."
          "\n1. Months by Watch Time"
          "\n2. Months by Number of Streams"
          "\n3. Months by Average Views"
          "\n4. Search by Month (line graphs)"
          "\n5. Search by Month (stats)"
          "\n6. Search Stats by Game and Month"
          "\n7. Best Game to Stream During Month?"
          "\n8. Main Menu"
          "\n9. Exit")
    choice = input()
    if choice.isdigit() == False:
        print("\nPlease enter a number.")
        monthlyData()
    elif int(choice) == 1:
        plotMonthsByWatchtime()
    elif int(choice) == 2:
        plotMonthsByStreams()
    elif int(choice) == 3:
        plotMonthsByAvgViews()
    elif int(choice) == 4:
        monthLines()
    elif int(choice) == 5:
        print("\nEnter Month Number (i.e. January = 1): ")
        search = str(input())
        getMonthStats(search)
    elif int(choice) == 6:
        print("\nSearch Game Name (case sensitive): ")
        search1 = str(input())
        print("\nEnter Month Number (i.e. January = 1): ")
        search2 = str(input())
        gameAndMonth(search1, search2)
    elif int(choice) == 7:
        print("\nEnter Month Number (i.e. January = 1): ")
        search = str(input())
        gameToStreamDuringMonth(search)
    elif int(choice) == 8:
        mainMenu()
    elif int(choice) == 9:
        quit()
    else:
        print("\nPlease enter a number.")
        monthlyData()
    monthlyData()

def monthLines():
    print("\nMONTHLY DATA FROM JAN 2016 - APR 2021"
          "\nType in a number to view graph and press Enter."
          "\n1. Graph Month by Watch Time"
          "\n2. Graph Month by Stream Time"
          "\n3. Graph Month by Average Views"
          "\n4. Monthly Data"
          "\n5. Main Menu"
          "\n6. Exit")
    choice = input()
    if choice.isdigit() == False:
        print("\nPlease enter a number.")
        monthLines()
    elif int(choice) == 1:
        print("\nEnter Month Number (i.e. January = 1): ")
        search = str(input())
        plotLineMonthWatchtime(search)
    elif int(choice) == 2:
        print("\nEnter Month Number (i.e. January = 1): ")
        search = str(input())
        plotLineMonthStreams(search)
    elif int(choice) == 3:
        print("\nEnter Month Number (i.e. January = 1): ")
        search = str(input())
        plotLineMonthAvgviews(search)
    elif int(choice) == 4:
        monthlyData()
    elif int(choice) == 5:
        mainMenu()
    elif int(choice) == 6:
        quit()
    else:
        print("\nPlease enter a number.")
        monthLines()
    monthLines()

mainMenu()

con.commit()
con.close()
