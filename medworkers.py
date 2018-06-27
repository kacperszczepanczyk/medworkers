from Parser import Parser
from Fetcher import Fetcher
from ProcessManager import ProcessManager
from Memcache import Memcache
from multiprocessing import Process
from iron_cache import *
from random import randint
import json
import time

cache = IronCache()
memcache = Memcache()
fetcher = Fetcher()
parser_online = Parser()
parser_highscores = Parser()
worlds = ['legacy', 'spectrum', 'destiny', 'pendulum']
professions = ['warriors', 'scouts', 'clerics', 'sorcerers', 'none', 'all']


def cache_online_players(world):
    op = parser_online.get_online_players(str(world))
    v = json.dumps(op)
    #cache.put(cache="online_players", key=world, value=v)
    memcache.cache.set(world, v)
    print('Cached online players for ' + str(world))


def cache_highscores(world, profession):
    hs = parser_highscores.get_highscores(world, profession)
    v = json.dumps(hs)
    #cache.put(cache="highscores", key=world + '_' + profession, value=v)
    memcache.cache.set('highscores_' + world + '_' + profession, v)
    print('Cached higscores for  ' + str(world) + '_' + profession)


def fetch_online_players(interval):
    while True:
        for world in worlds:
            cache_online_players(world)
        time.sleep(interval)


def fetch_highscores(interval):
    if randint(0, 1) == 1:
        worlds_arr = worlds[::-1]
        professions_arr = professions[::-1]
    else:
        worlds_arr = worlds
        professions_arr = professions

    while True:
        for world in worlds_arr:
            for profession in professions_arr:
                time.sleep(2)
                cache_highscores(world, profession)
        time.sleep(interval)


proc_attrs = {
             'online': {'func': fetcher.fetch_online_players, 'arg': 10},
             'highscores': {'func': fetcher.fetch_highscores, 'arg': 2*60*60}
            }


if __name__ == '__main__':
    pm = ProcessManager()
    pm.run(proc_attrs, 10)


