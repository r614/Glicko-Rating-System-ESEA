import csv
import math
from operator import itemgetter


class Player:
    # Class attribute
    # The system constant, which constrains
    # the change in volatility over time.
    _tau = 0.3

    def finalRating(self):
        return self.tname, self.rating, self.rd, self.vol

    def GetName(self, tname):
        return '{}'.format(self.tname)

    def getRating(self):
        return (self.__rating * 173.7178) + 1500

    def setRating(self, rating):
        self.__rating = (rating - 1500) / 173.7178

    rating = property(getRating, setRating)

    def getRd(self):
        return self.__rd * 173.7178

    def setRd(self, rd):
        self.__rd = rd / 173.7178

    rd = property(getRd, setRd)

    def __init__(self, tname, rating=1500, rd=350, vol=0.06):
        # For testing purposes, preload the values
        # assigned to an unrated player.
        self.setRating(rating)
        self.tname = tname
        self.setRd(rd)
        self.vol = vol

    def _preRatingRD(self):
        """ Calculates and updates the player's rating deviation for the
        beginning of a rating period.

        preRatingRD() -> None

        """
        self.__rd = math.sqrt(math.pow(self.__rd, 2) + math.pow(self.vol, 2))

    def update_player(self, rating_list, RD_list, outcome_list):
        """ Calculates the new rating and rating deviation of the player.

        update_player(list[int], list[int], list[bool]) -> None

        """
        # Convert the rating and rating deviation values for internal use.
        rating_list = [(x - 1500) / 173.7178 for x in rating_list]
        RD_list = [x / 173.7178 for x in RD_list]

        v = self._v(rating_list, RD_list)
        self.vol = self._newVol(rating_list, RD_list, outcome_list, v)
        self._preRatingRD()

        self.__rd = 1 / math.sqrt((1 / math.pow(self.__rd, 2)) + (1 / v))

        tempSum = 0
        for i in range(len(rating_list)):
            tempSum += self._g(RD_list[i]) * \
                (outcome_list[i] - self._E(rating_list[i], RD_list[i]))
        self.__rating += math.pow(self.__rd, 2) * tempSum

    def _newVol(self, rating_list, RD_list, outcome_list, v):
        """ Calculating the new volatility as per the Glicko2 system.

        _newVol(list, list, list) -> float

        """
        i = 0
        delta = self._delta(rating_list, RD_list, outcome_list, v)
        a = math.log(math.pow(self.vol, 2))
        tau = self._tau
        x0 = a
        x1 = 0

        while x0 != x1:
            # New iteration, so x(i) becomes x(i-1)
            x0 = x1
            d = math.pow(self.__rating, 2) + v + math.exp(x0)
            h1 = -(x0 - a) / math.pow(tau, 2) - 0.5 * math.exp(x0) \
                / d + 0.5 * math.exp(x0) * math.pow(delta / d, 2)
            h2 = -1 / math.pow(tau, 2) - 0.5 * math.exp(x0) * \
                (math.pow(self.__rating, 2) + v) \
                / math.pow(d, 2) + 0.5 * math.pow(delta, 2) * math.exp(x0) \
                * (math.pow(self.__rating, 2) + v - math.exp(x0)) / math.pow(d, 3)
            x1 = x0 - (h1 / h2)

        return math.exp(x1 / 2)

    def _delta(self, rating_list, RD_list, outcome_list, v):
        """ The delta function of the Glicko2 system.

        _delta(list, list, list) -> float

        """
        tempSum = 0
        for i in range(len(rating_list)):
            tempSum += self._g(RD_list[i]) * (outcome_list[i] - self._E(rating_list[i], RD_list[i]))
        return v * tempSum

    def _v(self, rating_list, RD_list):
        """ The v function of the Glicko2 system.

        _v(list[int], list[int]) -> float

        """
        tempSum = 0
        for i in range(len(rating_list)):
            tempE = self._E(rating_list[i], RD_list[i])
            tempSum += math.pow(self._g(RD_list[i]), 2) * tempE * (1 - tempE)
        return 1 / tempSum

    def _E(self, p2rating, p2RD):
        """ The Glicko E function.

        _E(int) -> float

        """
        return 1 / (1 + math.exp(-1 * self._g(p2RD) *
                                 (self.__rating - p2rating)))

    def _g(self, RD):
        """ The Glicko2 g(RD) function.

        _g() -> float

        """
        return 1 / math.sqrt(1 + 3 * math.pow(RD, 2) / math.pow(math.pi, 2))

    def did_not_compete(self):
        """ Applies Step 6 of the algorithm. Use this for
        players who did not compete in the rating period.

        did_not_compete() -> None

        """
        self._preRatingRD()


class Match:
    def __init__(self, tname, home, away, map, result, score, date):
        self.tname = tname
        self.home = home
        self.away = away
        self.map = map
        self.date = date
        self.result = result
        self.score = score

    # Override equality operator for this class
    def __eq__(self, other):
        # print(self.home == other.home)
        return self.home == other.home and self.away == other.away and self.map == other.map and self.date == other.date

    def stat_row(self):
        return self.tname, self.home, self.away, self.map, self.result, self.score, self.date

def calculateRating():
    obj = []
    team_name = []
    rating_list = []
    duplicate_list = []

    with open('big_data.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        big_match_list = list(reader)

    for i in range(0, len(big_match_list)):
        match = Match(big_match_list[i][0], big_match_list[i][1], big_match_list[i][2], big_match_list[i][3], big_match_list[i][4], big_match_list[i][5], big_match_list[i][6])
        if(str(match.tname) == str(match.home)):
            tname2 = match.away

        elif(str(match.tname) == str(match.away)):
            tname2 = match.home

        if match.tname not in team_name:
            team1 = Player(match.tname, 1500, 350, 0.06)
            obj.append(team1)
            team_name.append(match.tname)

        else:
            for row in obj:
                if(row.tname == match.tname):
                    team1 = row
                    t1_loc = obj.index(row)


        if tname2 not in team_name:
            team2 = Player(tname2,1500, 350, 0.06)
            obj.append(team2)
            team_name.append(tname2)
            t2_loc = obj.index(team2)
        else:
            for row in obj:
                if(row.tname == tname2):
                    team2 = row


        if (match.result == 'Win'):
            team1.update_player([x for x in [team2.rating]],
                                [x for x in [team2.rd]], [1])
            team2.update_player([x for x in [team1.rating]],
                                [x for x in [team1.rd]], [0])
        elif(match.result == 'Loss'):
            team1.update_player([x for x in [team2.rating]],
                                [x for x in [team2.rd]], [0])
            team2.update_player([x for x in [team1.rating]],
                                [x for x in [team1.rd]], [1])
        else:
            pass

        for row in obj:
            if(row.tname == match.tname):
                row = team1

        for row in obj:
            if(row.tname == tname2):
                row = team2

    for row in obj:
        stat_row = row.finalRating()
        rating_list.append(stat_row)

    with open('finalrating.csv', 'w', newline='') as f:
       writer = csv.writer(f, delimiter=',')
       for match in rating_list:
           writer.writerow(match)
