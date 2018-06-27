from Fetcher import Fetcher
from ProcessManager import ProcessManager


fetcher = Fetcher()

proc_attrs = {
             'online': {'func': fetcher.fetch_online_players, 'arg': 10},
             'highscores': {'func': fetcher.fetch_highscores, 'arg': 2*60*60}
            }

if __name__ == '__main__':
    pm = ProcessManager()
    pm.run(proc_attrs, 10)


