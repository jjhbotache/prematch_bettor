import pickle
import unittest
from python.classes import *
from python.helper_functions import *


class TestEventsSet(unittest.TestCase):
  wplay = Bookmaker("Wplay","https://apuestas.wplay.co/es#upcoming-tab-FOOT")
  betplay = Bookmaker("Betplay","https://www.betplay.com.co/")
  codere = Bookmaker("Codere","https://www.codere.com.co/")
  
  def test_load_events_from_json(self):
        # Define a sample JSON file path
        json_file_path = "sample.json"

        # Define the expected output
        expected_events = [
            Event(
                bets=[
                    Bet(bookmaker=Bookmaker(name="Bookmaker 1", link="http://bookmaker1.com"), bet_name="Bet 1", odd=1.5),
                    Bet(bookmaker=Bookmaker(name="Bookmaker 2", link="http://bookmaker2.com"), bet_name="Bet 2", odd=2.0)
                ]
            ),
            Event(
                bets=[
                    Bet(bookmaker=Bookmaker(name="Bookmaker 3", link="http://bookmaker3.com"), bet_name="Bet 3", odd=1.8),
                    Bet(bookmaker=Bookmaker(name="Bookmaker 4", link="http://bookmaker4.com"), bet_name="Bet 4", odd=2.2)
                ]
            )
        ]

        # Call the function
        actual_events = load_events_from_json(json_file_path)
        # save events in a binary file and print them
        with open('expected_events.bin', 'rb') as file:
          expected_events= pickle.load(file)
          for i in range(len(expected_events)):
            self.assertEqual(actual_events[i].event_id, expected_events[i].event_id)
        
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

  def test_create_events_groups(self):
        events = [
            *load_events_from_json("sample_betplay_events.json"),
            *load_events_from_json("sample_codere_events.json"),
            *load_events_from_json("sample_wplay_events.json"),
        ]
        
        result = create_events_groups(events)
        current_amount_of_groups = len(result)
        for group in result[:5]:
          print("*"*100)
          for event in group:
              print(f"{str(event.bookmaker.name + ")").ljust(10)}{event.event_name}")
              
        self.assertEqual(current_amount_of_groups, 836) # 836 groups are the amount of groups expected
    
  def test_events_sets(self):
        events = [
            *load_events_from_json("sample_betplay_events.json"),
            *load_events_from_json("sample_codere_events.json"),
            *load_events_from_json("sample_wplay_events.json"),
        ]
        
        groups = [g for g in create_events_groups(events) if len(g) > 1]
        event_sets = [EventsSet(group) for group in groups]
        event_sets.sort(key=lambda x: x.profit, reverse=True)
        for event_set in event_sets[:5]:
          print("*"*100)
          print(event_set)
        
        
    
if __name__ == '__main__':
  unittest.main()