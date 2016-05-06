class PERCalculator(object):
     def __init__(self, name, team):
          self.name = name
          self.team = team

     # Methods for calculating additional factors

     def calculateDRBpct(self):
          self.DRBpct = (self.ltrebounds - self.lorebounds)/self.ltrebounds
          return print("Calculated DRBpct")

     def calculateVOP(self):
          self.VOP = self.lpoints / (self.lafieldgoals - self.lorebounds + self.lturnovers + 0.44 * self.lafreethrows)
          return print("Calculated VOP")

     def calculateFactor(self):
          self.factor = (2/3) - (0.5 * (self.lassists / self.lfieldgoals)) / (2* (self.lfieldgoals / self.lfreethrows))
          return print("Calculated Factor")

     # Calculating the uPER

     def calculateuPER(self):
          self.uPER = (1 / self.minutes) \
          * ( self.threepoints \
          + (2/3) * self.assists \
          + (2 - self.factor * (self.tassists / self.tfieldgoals)) * self.fieldgoals \
          + (self.freethrows *0.5 * (1 + (1 - (self.tassists / self.tfieldgoals)) + (2/3) * (self.tassists / self.tfieldgoals))) \
          - self.VOP * self.turnovers \
          - self.VOP * self.DRBpct * (self.afieldgoals - self.fieldgoals) \
          - self.VOP * 0.44 * (0.44 + (0.56 * self.DRBpct)) * (self.afreethrows - self.freethrows) \
          + self.VOP * (1 - self.DRBpct) * (self.trebounds - self.orebounds) \
          + self.VOP * self.DRBpct * self.orebounds \
          + self.VOP * self.steals \
          + self.VOP * self.DRBpct * self.blocks \
          - self.pfouls * ((self.lafreethrows / self.lpfouls) - 0.44 * (self.afreethrows / self.lpfouls) * self.VOP) ) 

          self.uPER = round(self.uPER, 2)

          return print("Calculated uPER")

     def estimatePaceAdjustment(self):
          self.ePA = 2*self.lpointspg / (self.tpointspg + self.opointspg )
          self.ePA = round(self.ePA, 2)
          return print("Calculated estimatePaceAdjustment")

     def calculateaPER(self):
          self.aPER = round(self.ePA * self.uPER, 2)
