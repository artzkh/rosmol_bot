from vkbottle import BaseStateGroup


class States(BaseStateGroup):
    TRAINING = 0
    ACTIVE = 1
    DIED = 2
    SPAM = 3
    ROULETTE = 4
