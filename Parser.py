from bs4 import BeautifulSoup
import aiohttp
import asyncio


class Parser:

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_source_data_async(self, url):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, url)
            return html

    def get_source_data(self, url):
        parser_loop = asyncio.get_event_loop()
        data = parser_loop.run_until_complete(self.get_source_data_async(url))
        return data

    def get_player_logo(self, soup):
        div = soup.find('div', class_='med-news-image')
        style = div.find_all('div')[0]['style']
        logo_path = style.replace("background-image: url('", "").replace("');", "").replace(' ', '')
        return "https://medivia.online" + logo_path

    def get_player_activities(self, soup):
        div = soup.find_all('div', class_='med-width-100')
        titles = div[1].find_all('div', class_='title')
        del titles[0]

        _dict = dict()
        lists = soup.find_all('div', class_='med-width-100 med-p-10 med-show-more')
        for title, _list in zip(titles, lists):
            times = _list.find_all('div', class_='med-width-25')
            activities = _list.find_all('div', class_='med-width-75')
            msg = ''
            for time, activity in zip(times, activities):
                msg = msg + '• ' + time.get_text() + ' ' + activity.get_text() + '\n'

            if title.get_text() == "Task list":
                _dict['tasks_done'] = len(activities)
            else:
                _dict[title.get_text()] = msg

        return _dict

    def get_player_info(self, name):
        url = 'https://medivia.online/community/character/' + name.replace(' ', '%20')
        print("Getting detailed info for " + url)

        data = self.get_source_data(url)
        soup = BeautifulSoup(data, "html.parser")
        activities = self.get_player_activities(soup)
        stats = soup.find_all('div', class_='med-width-100 med-mt-10')
        info = {'last login': '-', 'status': '-', 'guild': '-', 'house': '-', 'comment': '-', 'tasks_done': 0,
                'Latest deaths': 'This player has not died in the last 4 weeks.',
                'Latest kills': 'This player has not killed anyone in the last 4 weeks.'}
        for stat in stats:
            if stat.get_text().startswith('comment:'):
                info['comment'] = stat.get_text()[8:]
            else:
                key, value = stat.get_text().split(':')
                info[key.strip()] = value.strip()

        info['logo'] = self.get_player_logo(soup)
        if 'Death list' in activities:
            info['Latest deaths'] = activities['Death list']
        if 'Kill list' in activities:
            info['Latest kills'] = activities['Kill list']
        if 'tasks_done' in activities:
            info['tasks_done'] = activities['tasks_done']

        return info

    def get_online_players(self, world):
        url = 'http://medivia.online/community/online/' + str(world)

        data = self.get_source_data(url)

        soup = BeautifulSoup(data, "html.parser")
        names = soup.find_all('div', class_='med-width-35')
        vocs = soup.find_all('div', class_='med-width-15')
        levels = soup.find_all('div', class_='med-width-25 med-text-right med-pr-40')

        players = list()
        for name, voc, level in zip(names, vocs, levels):
            player = {'name': name.get_text(), 'profession': voc.get_text(), 'level': level.get_text()}
            players.append(player)

        if players and len(players) >= 1:
            del players[0]

        return players

    def get_highscores(self, world, profession):
        highscores = {}
        skills = ['maglevel', 'fist', 'club', 'sword', 'axe', 'distance', 'shielding', 'fishing', 'mining']
        for skill in skills:
            url = 'https://medivia.online/highscores/' + world + '/' + profession + '/' + skill
            data = self.get_source_data(url)
            soup = BeautifulSoup(data, "html.parser")
            names = soup.find_all('div', class_='med-width-66')
            skill_values = soup.find_all('div', class_='med-width-35 med-text-right med-pr-40')
            highscores[skill] = {}
            for name, skill_value in zip(names, skill_values):
                highscores[skill][name.get_text()] = skill_value.get_text()

        return highscores






















