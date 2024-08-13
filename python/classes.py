from python.helper_functions import football_name_normalize, simplify_list
from levenshtein_distance import Levenshtein
from .constants.constants import LIST_OF_NAMES_TAKEN_AS_DRAW
class Bookmaker():
  def __init__(self, name:str,link:str):
    self.name = name.lower()
    self.link = link
    
  def __str__(self):
    return f"{self.name}({self.link})"
  
  def dict(self):
    return {
      "name": self.name,
      "link": self.link
    }

class Bet():
  def __init__(self,bookmaker:Bookmaker,bet_name:str,odd:float):
    self.bookmaker = bookmaker
    # if the bet name is in LIST_OF_NAMES_TAKEN_AS_DRAW it will be considered a draw
    if bet_name.lower() in LIST_OF_NAMES_TAKEN_AS_DRAW:
      self.bet_name = "X"
    else:
      self.bet_name = bet_name.strip().lower().capitalize()
    
    self.odd = float(odd)
    self.bet_id = f"{bookmaker.name[:2]}{bet_name[:2]}{bet_name[-2:]}".lower()
    
    
  def __str__(self):
    return f"{self.bet_name}\t\t({self.odd})\t\tin {self.bookmaker.name}"
  
  def dict(self):
    return {
      "bet_id": self.bet_id,
      "bet_name": self.bet_name,
      "odd": self.odd,
      "bookmaker": self.bookmaker.__dict__
    }

class Event():
  def __init__(self, bets:list[Bet]):
    #make sure all the bets are from the same bookmaker
    assert any([bet.bookmaker == bets[0].bookmaker for bet in bets])
    self.bookmaker = bets[0].bookmaker
    self.bets = bets
    # the event name will be the options that are not called "Draw", ordered alphabetically separated by " vs "
    
    self.event_name = " vs ".join(sorted([bet.bet_name for bet in self.bets if bet.bet_name.lower() not in LIST_OF_NAMES_TAKEN_AS_DRAW]))
    self.event_id = f"{self.bookmaker.name[:2]}-{self.bets[0].bet_id[2:]}-{self.bets[-1].bet_id[2:]}".lower()
    
  def __str__(self):
    return f"Event in {self.bookmaker.name}: {' '.join([str(bet) for bet in self.bets])}"
  
  def dict(self):
    return {
      "event_id": self.event_id,
      "event_name": self.event_name,
      "bets": [bet.dict() for bet in self.bets],
      "bookmaker": self.bookmaker.dict(),
      
    }
    
class EventsSet():
  def __init__(self, events:list[Event]):
    if len(events) < 2: raise ValueError("An event set must have at least 2 events")
    
    self.events = events # at least 2 events
    
    self.bets = simplify_list( [ event.bets for event in self.events])
    
    # group bets by similarity in the name using levenshtein distance
    grouped_bets = [[b] for b in self.events[0].bets]
    
    
    
    bets_to_group = simplify_list( [ event.bets for event in self.events[1:]])
    for bet in bets_to_group:
      
      # for each bet, look for the similar named bet in the grouped_bets
      ideal = {
        "index_group": None,
        "distance": float("inf")
      }
      for i,group in enumerate(grouped_bets):
        distance = min([Levenshtein(football_name_normalize(bet.bet_name),football_name_normalize(b.bet_name)).distance() for b in group])
        if distance < ideal["distance"]:
          ideal["distance"] = distance
          ideal["index_group"] = i
      
      # put on the ideal group
      grouped_bets[ideal["index_group"]].append(bet)
    
    
    
    
    
    # for each option, get the option with the highest odd
    self.best_bets = [
      max(group, key=lambda x: x.odd)
      for group in grouped_bets
    ]
    
    
    
    # calculate if it's a sure bet
    implicit_posibilities = [ 1/bet.odd for bet in self.best_bets ]
    sum_of_implicit_posibilities = sum(implicit_posibilities)
    self.is_sure_bet = sum_of_implicit_posibilities < 1
    self.profit = (1/sum_of_implicit_posibilities - 1)*100
    
    
    # 
    
  def __str__(self):
    bet_strings = "\n".join([str(bet) for bet in self.best_bets])
    return (
f"""({round(self.profit,2)}%) EventsSet for the event: {self.events[0].event_name}
Sure bet: {self.is_sure_bet}
Best bets:
{bet_strings}
"""    )
    
  
  # run a test

if __name__ == "__main__":
  # create 3 bm
  wplay = Bookmaker("Wplay","https://apuestas.wplay.co/es#upcoming-tab-FOOT")
  betplay = Bookmaker("Betplay","https://www.betplay.com.co/")
  codere = Bookmaker("Codere","https://www.codere.com.co/")
  bookmakers = [wplay,betplay,codere]
  
  # print(*bookmakers,sep="\n")
  event_a = Event([
    Bet(wplay,"tolima",1.5),
    Bet(wplay,"x",3.5),
    Bet(wplay,"pereira",3)
  ])
  event_b = Event([
    Bet(betplay,"pereira",6.25),
    Bet(betplay,"x",2),
    Bet(betplay,"tolima",1),
  ])
  
  
  event_set = EventsSet([event_a,event_b])
  print(event_set)
  