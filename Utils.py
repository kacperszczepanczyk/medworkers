worlds = ['legacy', 'spectrum', 'destiny', 'pendulum']
professions = ['warriors', 'scouts', 'clerics', 'sorcerers', 'none', 'all']


class Player:

    def __init__(self, name, profession, level):
        self.name = name
        self.profession = profession
        self.level = level

    def __gt__(self, other):
        return self.level > other

    def __lt__(self, other):
        return self.level < other

    def as_dict(self):
        return {'name': self.name, 'profession': self.profession, 'level': self.level}


class DetailedPlayer(Player):

    def __init__(self, name, profession, level, mlevel, sex, world, status, accstatus, residence, guild, house, skills):
        self.name = name
        self.profession = profession
        self.level = level
        self.mlevel = mlevel
        self.sex = sex
        self.world = world
        self.status = status
        self.accstatus = accstatus
        self.residence = residence
        self.guild = guild
        self.house = house
        self.skills = skills
