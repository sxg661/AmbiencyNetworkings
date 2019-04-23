#author Sophie Guile

class VenueInfo:


  def __init__(self, ID, name, venueType, occ, humid, light, temp, sound, dist):
    self.ID = ID
    self.name = name
    self.venueType = venueType
    self.occupancy = occ
    self.humidity = humid
    self.light = light
    self.temperature = temp
    self.sound = sound
    self.distance = dist

  def __str__(self):
    return "{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}".format(self.ID, self.name, self.venueType,self.occupancy,self.humidity,self.light,self.temperature,self.sound,self.distance)
          
    



def getVenues():
    venues = []
    venues.append(VenueInfo(12,"Joe's Bar", "Bar", 50, 0, 50, 1000, 23, 60));
    venues.append(VenueInfo(14,"Bad Libary", "Library", 90, 1, 80, 1000, 13, 70));
    return venues

def filter(venues, venueType):
    newVenues = []
    for venue in venues:
      print("venue being checked")
      if(venue.venueType == venueType):
          print("found venue of this type")
          newVenues.append(venue)
    return newVenues

def displayVenues(venues):
    for venue in venues:
        print(venue.name)
