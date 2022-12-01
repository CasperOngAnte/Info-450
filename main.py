import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def main():
    df1 = pd.read_csv('WorldCupMatches.csv')
    df2 = pd.read_csv('WorldCups.csv')
    # Read in from the tables

    temp = df2.groupby("Winner").size().reset_index(name='World Cups')
    fig = px.pie(temp, values="World Cups", names="Winner", title="Every World Cup Winner (Since 2014)")
    fig.update_traces(textinfo='value', textfont_size=20)
    # fig.show()
    # Finds the world cup winners and the amount of times they've won, pie chart





    tlist = {}
    temp = df2[["Winner", "Runners-Up", "Third", "Fourth"]]
    # selects placed columns

    for r, row in temp.iterrows():
        for c, value in row.items():
            # iterate through each element
            if value in tlist:
                tlist[value] += 1
            else:
                tlist[value] = 1
            # add values for each country that exists
            # this represents each time a country places

    cts = list(tlist.keys())
    dft = pd.DataFrame(cts)
    dft.reset_index()
    dft.columns = ["Country"]
    # creates a dataframe consisting of each country

    for x in range(4):
        t = list(temp.iloc[:, x].to_dict().values())
        ret = []
        for ct in cts:
            # for each country placed in a certain place
            ret.append(t.count(ct))
            # add the amount of times they appear in that place
        dft[temp.columns[x]] = ret
        # add to data frame

    fig = px.bar(dft, x="Country", y=["Winner", "Runners-Up", "Third", "Fourth"], title="Times placed at World Cup",
                 labels={"value": "Times placed", "variable": "Position"})
    # fig.show()
    # amount of times each country has placed and in what position, stacked bar graph




    temp1 = df1[["Home Team Name", "Home Team Goals"]].groupby("Home Team Name").size().reset_index()
    temp2 = df1[["Away Team Name", "Away Team Goals"]].groupby("Away Team Name").size().reset_index()
    # group by aggregation to collect goal count

    dftemp1 = pd.DataFrame(temp1)
    dftemp1.columns = ["Team", "Goals"]
    dftemp2 = pd.DataFrame(temp2)
    dftemp2.columns = ["Team", "Goals"]
    # fixes columns

    temp = dftemp1.set_index('Team').add(dftemp2.set_index('Team'), fill_value=0).reset_index()
    fig = px.bar(temp, x='Team', y='Goals')
    # fig.show()
    # shows total goals scored by country, bar graph




    recent = df1[df1["Year"] > 2001]
    # only takes the most recent years
    temp1 = recent[["Home Team Name", "Home Team Goals"]].groupby("Home Team Name").size().reset_index()
    temp2 = recent[["Away Team Name", "Away Team Goals"]].groupby("Away Team Name").size().reset_index()
    # group by aggregation to collect goal count

    dftemp1 = pd.DataFrame(temp1)
    dftemp1.columns = ["Team", "Goals"]
    dftemp2 = pd.DataFrame(temp2)
    dftemp2.columns = ["Team", "Goals"]
    # fixes columns

    temp = dftemp1.set_index('Team').add(dftemp2.set_index('Team'), fill_value=0).reset_index()
    fig = px.bar(temp, x='Team', y='Goals')
    # fig.show()
    # shows total goals scored by country since 2002 wc, bar graph



    temp = df2[['Year', 'Cup #', 'Host']]
    # Only keep year, cup #, and host country in the df
    df = df1.merge(temp, how="left", on="Year")
    # left merge on df1 to include host country and cup number
    clist = df2['Host'].to_list()
    temp = df[['Home Team Name', 'Home Team Goals', 'Away Team Goals', 'Away Team Name', 'Host']]
    # create a list of countries who have hosted

    chgoal = {}
    cngoal = {}
    hostc = {}
    hostn = {}
    # initalize dictionaries for goals as host countries and not as host countries

    for x in clist:
        if x not in chgoal:
            chgoal[x] = 0
            cngoal[x] = 0
            hostc[x] = 1
            hostn[x] = 20 - hostc[x]
        else:
            hostc[x] += 1
            hostn[x] = 20 - hostc[x]
    # populate necessary dictionaries for countries



    for r, row in temp.iterrows():
        if row[0] in clist or row[2] in clist:
            active = row[0]
            # if home or away team is in the list of host countries
            if row[0] == row[4]:
                # if home team name is host
                chgoal[row[0]] += row[1]
                # add goals scored to host dict
            elif row[2] == row[4]:
                # if away team name is host
                chgoal[row[2]] += row[3]
                # add goals scored to host dict
            else:
                if row[0] == active:
                    # if home team is the given country
                    cngoal[row[0]] += row[1]
                else:
                    # if away team is the given country
                    cngoal[row[2]] += row[3]

    goalsPerHost = []
    goalsPerNot = []
    t1 = list(chgoal.values())
    t2 = list(hostc.values())
    t3 = list(cngoal.values())
    t4 = list(hostn.values())
    # creates lists which can be appended to and accessed easier for each sector

    for x in range(len(t1)):
        goalsPerHost.append(float(t1[x])/t2[x])
        goalsPerNot.append(float(t3[x])/t4[x])
    # appends the percentages of goals to games based on hosting

    ndclist = list(cngoal.keys())

    data = {
        "Not Hosting": goalsPerNot,
        "Hosting": goalsPerHost,
        "Country": ndclist
    }
    # creates dictionary for hosting percentages and country

    ret = pd.DataFrame(data)
    print(ret)
    fig = px.bar(ret, x="Country", y=["Hosting", "Not Hosting"], title="%Goals per Appearance")
    fig.show()

if __name__ == '__main__':
    main()
