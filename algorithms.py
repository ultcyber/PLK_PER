class PERCalculator(object):
     def __init__(self, name):
          self.name = name

     # Different statistics' setters - just for making the other functions work, to be removed

     def setGeneralStats(self, minutes, steals, assists, blocks, turnovers, pfouls):
          self.minutes = minutes
          self.assists = assists
          self.steals = steals
          self.blocks = blocks
          self.turnovers = turnovers
          self.pfouls = pfouls

     def setOffensiveStats(self, threepoints, fieldgoals, afieldgoals, freethrows, afreethrows):
          self.threepoints = threepoints
          self.fieldgoals = fieldgoals
          self.afieldgoals = afieldgoals
          self.freethrows = freethrows
          self.afreethrows = afreethrows

     def setDefensiveStats(self, trebounds, orebounds):
          self.trebounds = trebounds
          self.orebounds = orebounds

     def setTeamStats(self, tassists, tfieldgoals):
          self.tassists = tassists
          self.tfieldgoals = tfieldgoals

     def setLeagueStats(self, lassists, ltrebounds, lorebounds, lfieldgoals, lafieldgoals, lafreethrows, lfreethrows, lpfouls, lafthrows, lpoints, lturnovers):
          self.lassists = lassists
          self.ltrebounds = ltrebounds
          self.lorebounds = lorebounds
          self.lfreethrows = lfreethrows
          self.lpfouls = lpfouls
          self.lpoints = lpoints
          self.lturnovers = lturnovers
          self.lfieldgoals = lfieldgoals
          self.lafieldgoals = lafieldgoals
          self.lafreethrows = lafreethrows
          self.lfreethrows = lfreethrows

     # Methods for calculating additional factors

     def calculateDRBpct(self):
          self.DRBpct = (self.lg_TRB - self.lg_ORB)/self.lg_TRB

     def calculateVOP(self):
          self.VOP = self.lpoints / (self.lafieldgoals - self.lorebounds + self.lturnovers + 0.44 * self.lafreethrows)

     def calculateFactor(self):
          self.factor = (2/3) - (0.5 * (self.lassists / self.lfieldgoals)) / (2* (self.lfieldgoals / self.lfreethrows))

     # Calculating the uPER

     def calculateuPER(self):
          uPER = ( (1 / self.minutes) * 
          ( self.threepoints + 
          (2/3) * self.assists
          + (2 - self.factor * (self.team_AST / self.team_FG)) * self.fieldgoals
          + (self.freethrows *0.5 * (1 + (1 - (self.team_AST / self.team_FG)) + (2/3) * (self.team_AST / self.team_FG)))
          - self.VOP * self.turnovers
          - self.VOP * self.DRBpct * (self.afieldgoals - self.fieldgoals)
          - self.VOP * 0.44 * (0.44 + (0.56 * self.DRBpct)) * (self.afreethrows - self.freethrows)
          + self.VOP * (1 - self.DRBpct) * (self.trebounds - self.orebounds)
          + self.VOP * self.DRBpct * self.orebounds
          + self.VOP * self.steals
          + self.VOP * self.DRBpct * self.blocks
          - self.pfouls * ((self.lafreethrows / self.lpfouls) - 0.44 * (self.afreethrows / self.lpfouls) * self.VOP) ) )

          return uPER
