import threading

from python.scrape import *











if __name__ == '__main__':

    threads = [
        threading.Thread(target=scrape_wplay),
        threading.Thread(target=scrape_betplay),
        threading.Thread(target=scrape_codere)
    ]
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
        
    print("All threads finished")
        
