from Parser import Parser
from Memcache import Memcache
from multiprocessing import Process
from iron_cache import *
from random import randint
import json
import time

cache = IronCache()
memcache = Memcache()
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


def thread_manager(interval):
    p1 = Process(target=fetch_online_players, args=(10,), name='fetch_online_players')
    p1.start()
    p2 = Process(target=fetch_highscores, args=(2*60*60,), name='fetch_highscores')
    p2.start()
    while True:
        if not p1.is_alive():
            p1.terminate()
            p1 = Process(target=fetch_online_players, args=(10,), name='fetch_online_players')
            p1.start()
        if not p2.is_alive():
            p2.terminate()
            p2 = Process(target=fetch_highscores, args=(2*60*60,), name='fetch_highscores')
            p2.start()
        print(str(p1) + ' ' + str(p1.is_alive()))
        print(str(p2) + ' ' + str(p2.is_alive()))
        time.sleep(interval)


if __name__ == '__main__':
    thread_manager(10)


