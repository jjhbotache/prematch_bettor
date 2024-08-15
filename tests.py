import pickle
import unittest
from python.classes import *
from python.helper_functions import *


class TestEventsSet(unittest.TestCase):
  wplay = Bookmaker("Wplay","https://apuestas.wplay.co/es#upcoming-tab-FOOT")
  betplay = Bookmaker("Betplay","https://www.betplay.com.co/")
  codere = Bookmaker("Codere","https://www.codere.com.co/")
  
  def test_well_formed_event(self):
    event = Event([
      Bet(TestEventsSet.wplay,"tolima (f)",10),
      Bet(TestEventsSet.wplay,"x",5),
      Bet(TestEventsSet.wplay,"pereira (f)",2.5),
    ])
    self.assertEqual(event.event_id,"wp-pera-toma")
    
  def test_sure_bet(self):
    
    event_a = Event([
      Bet(TestEventsSet.wplay,"tolima",10),
      Bet(TestEventsSet.wplay,"x",5),
      Bet(TestEventsSet.wplay,"pereira",2.5),
    ])
    event_b = Event([
      Bet(TestEventsSet.betplay,"pereira",5),
      Bet(TestEventsSet.betplay,"x",.2),
      Bet(TestEventsSet.betplay,"tolima",.1),
    ])
    
    event_set = EventsSet([event_a,event_b])
    
    self.assertTrue(event_set.is_sure_bet)
  
  def test_not_sure_bet(self):
    
    event_a = Event([
      Bet(TestEventsSet.wplay,"tolima",1),
      Bet(TestEventsSet.wplay,"x",.1),
      Bet(TestEventsSet.wplay,"pereira",2.5),
    ])
    event_b = Event([
      Bet(TestEventsSet.betplay,"pereira",1),
      Bet(TestEventsSet.betplay,"x",.2),
      Bet(TestEventsSet.betplay,"tolima",.1),
    ])
    event_c = Event([
      Bet(TestEventsSet.codere,"pereira",1),
      Bet(TestEventsSet.codere,"x",2),
      Bet(TestEventsSet.codere,"tolima",1),
    ])
    
    event_set = EventsSet([event_a,event_b,event_c])
    
    self.assertFalse(event_set.is_sure_bet)

  def test_remove_accents(self):
        self.assertEqual(remove_accents('café'), 'cafe')
        self.assertEqual(remove_accents('niño'), 'nino')
        self.assertEqual(remove_accents('jalapeño'), 'jalapeno')
        self.assertEqual(remove_accents('façade'), 'facade')

  def test_simplify_list(self):
      self.assertEqual(simplify_list([1, [2, 3], [4, [5, 6]]]), [1, 2, 3, 4, 5, 6])
      self.assertEqual(simplify_list([[['a']], ['b', ['c']]]), ['a', 'b', 'c'])
      self.assertEqual(simplify_list([[], [1, [2, []]]]), [1, 2])

  def test_football_name_normalize(self):
      self.assertEqual(football_name_normalize('FC Barcelona'), 'Barcelona')
      self.assertEqual(football_name_normalize('Real Madrid CF'), 'Realmadrid')
      self.assertEqual(football_name_normalize('Atlético de Madrid'), 'Atleticomadrid')
      self.assertEqual(football_name_normalize('Manchester United'), 'Manchester')

  def test_events_sets(self):
        events = [
            *load_events_from_json("sample_betplay_events.json"),
            *load_events_from_json("sample_codere_events.json"),
            *load_events_from_json("sample_wplay_events.json"),
        ]
        
        groups = [g for g in create_events_groups(events) if len(g) > 1]
        event_sets = [EventsSet(group) for group in groups]
        event_sets.sort(key=lambda x: x.profit, reverse=True)
        for event_set in event_sets[:2]:
          print("*"*100)
          print(event_set)
        
  def test_event_exits_function(self):
        events = [
            *load_events_from_json("sample_betplay_events.json"),
            *load_events_from_json("sample_codere_events.json"),
            *load_events_from_json("sample_wplay_events.json"),
        ]
        event1 = Event([
          Bet(
            bookmaker=Bookmaker(
              name="betplay",
              link="https://betplay.com.co/apuestas#sports-hub/football"
            ),
            bet_name="Cambridge united",
            odd=2.02
          ),
          Bet(
            bookmaker=Bookmaker(
              name="betplay",
              link="https://betplay.com.co/apuestas#sports-hub/football"
            ),
            bet_name="X",
            odd=3.45
          ),
          Bet(
            bookmaker=Bookmaker(
              name="betplay",
              link="https://betplay.com.co/apuestas#sports-hub/football"
            ),
            bet_name="Crawley town",
            odd=3.6
          )
        ])
        event2 = Event([
          Bet(
            bookmaker=Bookmaker(
              name="betplay",
              link="https://betplay.com.co/apuestas#sports-hub/football"
            ),
            bet_name="Cambridge united false",
            odd=2.02
          ),
          Bet(
            bookmaker=Bookmaker(
              name="betplay",
              link="https://betplay.com.co/apuestas#sports-hub/football"
            ),
            bet_name="X",
            odd=3.45
          ),
          Bet(
            bookmaker=Bookmaker(
              name="betplay",
              link="https://betplay.com.co/apuestas#sports-hub/football"
            ),
            bet_name="unexistent Crawley town",
            odd=3.6
          )
        ])
        
        self.assertTrue(event_already_exists(events_list=events, event=event1))
        self.assertFalse(event_already_exists(events_list=events, event=event2))
        
  
    
if __name__ == '__main__':
  unittest.main()