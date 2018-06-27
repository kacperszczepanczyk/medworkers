from Memcache import Memcache
from Parser import Parser
import Utils as utils
import json
import time
from random import randint


class Fetcher:
    memcache = Memcache()
    parser_online = Parser()
    parser_highscores = Parser()

    def cache_online_players(self, world):
        op = self.parser_online.get_online_players(str(world))
        v = json.dumps(op)
        # cache.put(cache="online_players", key=world, value=v)
        self.memcache.cache.set(world, v)
        print('Cached online players for ' + str(world))

    def cache_highscores(self, world, profession):
        hs = self.parser_highscores.get_highscores(world, profession)
        v = json.dumps(hs)
        # cache.put(cache="highscores", key=world + '_' + profession, value=v)
        self.memcache.cache.set('highscores_' + world + '_' + profession, v)
        print('Cached higscores for  ' + str(world) + '_' + profession)

    def fetch_online_players(self, interval):
        while True:
            for world in utils.worlds:
                self.cache_online_players(world)
            time.sleep(interval)

    def fetch_highscores(self, interval):
        worlds_arr = utils.worlds
        professions_arr = utils.professions
        if randint(0, 1) == 1:
            worlds_arr = utils.worlds[::-1]
            professions_arr = utils.professions[::-1]

        while True:
            for world in worlds_arr:
                for profession in professions_arr:
                    time.sleep(2)
                    self.cache_highscores(world, profession)
            time.sleep(interval)
