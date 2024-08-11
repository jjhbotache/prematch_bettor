from .constants.constants import LIST_OF_NAMES_TAKEN_AS_DRAW
import Levenshtein
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
    if bet_name.lower() in LIST_OF_NAMES_TAKEN_AS_DRAW: self.bet_name = "Draw"
    else: self.bet_name = bet_name.strip().lower().capitalize()
    
    self.odd = float(odd)
    self.bet_id = f"{bookmaker.name[:2]}{bet_name[:2]}{bet_name[-2:]}".lower()
    
    
  def __str__(self):
    return f"{self.bet_name}({self.odd}) in {self.bookmaker.name}"
  
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
    self.event_id = f"{self.event_name[:2]}{self.event_name[-2:]}"
    
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
    self.events = events # at least 2 events
    
    # if two events have the same name, bookmaker and odds, raise an error
    for event in self.events:
      for other_event in self.events:
        if event != other_event:
          assert event.event_name != other_event.event_name or event.bookmaker != other_event.bookmaker or event.bets != other_event.bets
    
    # for each option, get the option with the highest odd
    self.best_bets = []
    for bet in self.events[0].bets:
      # for each bet, look for the same bet in each event
      same_bet = []
      for event in self.events:
        same_bet.append(
          list(filter(
            lambda b: Levenshtein.distance(b.bet_name.lower(), bet.bet_name.lower()) < 10,
            event.bets
          ))
        )
      
      self.best_bets.append(
        max(same_bet,key=lambda bets: bets[0].odd)[0]
      )
      
    
    # calculate if it's a sure bet
    implicit_posibilities = [ 1/bet.odd for bet in self.best_bets ]
    sum_of_implicit_posibilities = sum(implicit_posibilities)
    self.is_sure_bet = sum_of_implicit_posibilities < 1
    self.profit = 1 - sum_of_implicit_posibilities
    
    
    # 
    
  def __str__(self):
    return (f"""({round(self.profit,2)}%) EventsSet for the event: {self.events[0].event_name}
    Sure bet: {self.is_sure_bet}
    Best bets:
    {"\n".join([str(bet) for bet in self.best_bets])}
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
    Bet(wplay,"local fs",1.5),
    Bet(wplay,"x",2.5),
    Bet(wplay,"deportivo visitante",9.5)
  ])
  event_b = Event([
    Bet(betplay,"Visitante",3.6),
    Bet(betplay,"x",5.7),
    Bet(betplay,"Local",4.9),
  ])
  
  print(event_a)
  print(event_b)
  
  event_set = EventsSet([event_a,event_b])
  print(event_set)
  