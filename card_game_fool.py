# -*- coding: utf-8 -*-
from random import shuffle


####################
class Suit:  # Масть

    __names = 'пики', 'трефы', 'бубны', 'червы'

    def __init__(self, n):
        assert isinstance(n, int)
        assert 0 <= n < Suit.len()
        self.__value = n

    def value(self):
        return self.__value

    def __str__(self):
        return str(Suit.__names[self.__value])

    def __repr__(self):
        return str(Suit.__names[self.__value])

    def just(self):  # Пробелы справа до максимально длинного названия масти
        return str(Suit.__names[self.__value]).ljust(max(len(name) for name in Suit.__names))

    def __hash__(self):
        return self.__value

    def __eq__(self, other):  # x == y
        assert isinstance(other, Suit)
        return self.__value == other.value()

    def __ne__(self, other):  # x != y
        assert isinstance(other, Suit)
        return self.__value != other.value()

    @staticmethod
    def len():
        return len(Suit.__names)

    @staticmethod
    def sequence():
        return (Suit(n) for n in range(Suit.len()))

    @staticmethod
    def name(string):
        assert isinstance(string, str)
        return Suit(Suit.__names.index(string)) if string in Suit.__names else None


######################################
class Dignity:  # Номинал, достоинство

    __names = '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз'

    def __init__(self, n):
        assert isinstance(n, int)
        assert 0 <= n < Dignity.len()
        self.__value = n

    def value(self):
        return self.__value

    def __str__(self):
        return str(Dignity.__names[self.__value])

    def __repr__(self):
        return str(Dignity.__names[self.__value])

    def just(self):  # Пробелы слева до максимально длинного названия
        return str(Dignity.__names[self.__value]).rjust(max(len(name) for name in Dignity.__names))

    def __hash__(self):
        return self.__value

    def __lt__(self, other):  # x < y
        assert isinstance(other, Dignity)
        return self.__value < other.value()

    def __le__(self, other):  # x ≤ y
        assert isinstance(other, Dignity)
        return self.__value <= other.value()

    def __eq__(self, other):  # x == y
        assert isinstance(other, Dignity)
        return self.__value == other.value()

    def __ne__(self, other):  # x != y
        assert isinstance(other, Dignity)
        return self.__value != other.value()

    def __gt__(self, other):  # x > y
        assert isinstance(other, Dignity)
        return self.__value > other.value()

    def __ge__(self, other):  # x ≥ y
        assert isinstance(other, Dignity)
        return self.__value >= other.value()

    @staticmethod
    def len():
        return len(Dignity.__names)

    @staticmethod
    def sequence():
        return (Dignity(n) for n in range(Dignity.len()))

    @staticmethod
    def name(string):
        assert isinstance(string, str)
        return Dignity(Dignity.__names.index(string)) if string in Dignity.__names else None


####################
class Card:  # Карта

    def __init__(self, dignity, suit):
        assert isinstance(dignity, Dignity) and isinstance(suit, Suit)
        self.__value = dignity, suit

    def value(self):
        return self.__value

    def dignity(self):
        return self.__value[0]

    def suit(self):
        return self.__value[1]

    def cover(self, card, trump_suit=None):
        assert isinstance(card, Card)
        assert trump_suit is None or isinstance(trump_suit, Suit)
        self_dignity, self_suit = self.value()
        card_dignity, card_suit = card.value()

        if self_suit == card_suit:  # Если масти одинаковые
            return self_dignity > card_dignity  # Если старше достоинство
        else:  # Масти разные
            return trump_suit is not None and self_suit == trump_suit  # Если козырь

    def __str__(self):
        dignity, suit = self.__value
        return '{}-{}'.format(dignity, suit)

    def __repr__(self):
        dignity, suit = self.__value
        return '{}-{}'.format(dignity, suit)

    def just(self):
        dignity, suit = self.__value
        return '{}-{}'.format(dignity.just(), suit.just())

    def __eq__(self, other):  # x == y
        assert isinstance(other, Card)
        return self.value() == other.value()

    def __hash__(self):
        dignity, suit = self.__value
        return dignity.value() * Suit.len() + suit.value()

    @staticmethod
    def name(string):
        assert isinstance(string, str)
        names = string.split('-')
        if len(names) == 2:
            name_dignity, name_suit = names
            dignity = Dignity.name(name_dignity)
            suit = Suit.name(name_suit)
            if dignity and suit:  # Если оба не None
                return Card(dignity, suit)
        # return None  # Во всех остальных случаях


#####################
class Deck:  # Колода

    def __init__(self):
        self.__deck = [Card(dignity, suit) for dignity in Dignity.sequence() for suit in Suit.sequence()]
        shuffle(self.__deck)
        self.__trump_card = self.__deck[0]

    def trump_suit(self):  # Козырная масть
        return self.__trump_card.suit()

    def trump_card(self):  # В принципе достаточно только масти. Но по правилам карту должно быть видно)
        return self.__trump_card

    def len(self):
        return len(self.__deck)

    def get_cards(self, n=1):
        assert isinstance(n, int)
        assert n > 0
        n = min(n, self.len())
        return [self.__deck.pop() for _ in range(n)]


###########################################################################
class Table:  # Стол на который кидают карты. Следит за соблюдением правил)

    def __init__(self, trump_card):
        assert isinstance(trump_card, Card)
        self.trump_card = trump_card
        self.cards = []

    def trump_suit(self):  # Козырная масть
        return self.trump_card.suit()

    def trump_card(self):  # В принципе достаточно только масти. Но по правилам карту должно быть видно)
        return self.trump_card

    def len(self):
        return len(self.cards)

    def is_attack(self):
        return len(self.cards) % 2 == 0  # Если атака. Четный ход.

    def check(self, card):
        assert isinstance(card, Card)
        count_cards = len(self.cards)

        if count_cards == 0:  # Если список пуст. Первый ход любая карта.
            return True

        if count_cards % 2:  # Если нужно отбиватся. Нечетный ход.
            return card.cover(self.cards[-1], self.trump_card.suit())  # Если можно побить последнюю карту.
        else:  # Если нужно ходить. Четный ход.
            return card.dignity() in {card.dignity() for card in self.cards}  # Только уже присутствующего достоинства.

    def go(self, card):
        assert isinstance(card, Card)
        check = self.check(card)
        if check:
            self.cards.append(card)
        return check

    def get_all_card(self):
        temp = self.cards
        self.cards = []
        return temp

    def clear(self):
        self.cards = []

    def __str__(self):
        return ' '.join(str(card) for card in self.cards)

    def __repr__(self):
        return ' '.join(str(card) for card in self.cards)

    def just(self):
        go = len(self.cards) % 2  # Четность хода. Определяет атакуют сейчас или отбиваются
        s0, s1 = self.cards[0::2], self.cards[1::2]  # Четная и нечетная последовательности
        dummy = s0 if go else s1   # Последовательность Болвана всегда первая
        gamer = s1 if go else s0  # Последовательность игрока вторая. Так удобнее смотреть)
        string = ''
        string += '|'
        string += '|'.join(card.just() for card in dummy)
        string += '|\n|'
        string += '|'.join(card.just() for card in gamer)
        string += '|'
        return string


#############################
class Hand:  # Рука с картами

    def __init__(self):
        self.cards = []

    def exist(self, card):
        assert isinstance(card, Card)
        return card in self.cards

    def get_card(self, card):
        assert isinstance(card, Card)
        return self.cards.pop(self.cards.index(card)) if card in self.cards else None

    def len(self):
        return len(self.cards)

    def add_cards(self, cards):
        assert isinstance(cards, (list, tuple))
        for card in cards:
            assert isinstance(card, Card)
        self.cards.extend(cards)

    def __str__(self):
        return ' '.join(str(card) for card in self.cards)

    def just(self):
        return '[' + ', '.join(str(card) for card in self.cards) + ']'

    def __repr__(self):
        return ' '.join(str(card) for card in self.cards)

    def __contains__(self, card):
        assert isinstance(card, Card)
        return card in self.cards


######################################################
class Game:  # Партия в игре. Да собственно, вся игра)

    def __init__(self):
        self.hand_gamer = Hand()  # Рука игрока.
        self.hand_dummy = Hand()  # Рука "Болвана".
        self.deck = Deck()  # Карточная колода.
        self.table = Table(self.deck.trump_card())  # Стол для игры с объявленным козырем.
        self.distribution_cards()  # Раздача карт (до 6-ти).
        self.commands = {}  # Собираем все команды в словарь.
        self.commands.update({'Карты': self.command_dignity})
        self.commands.update({'Масти': self.command_suit})
        self.commands.update({'Команды': self.command_commands})
        self.commands.update({'Игра': self.command_description})
        self.commands.update({'Козырь': self.command_trump})
        self.commands.update({'Рука': self.command_hand})
        self.commands.update({'cheat': self.command_cheat})  # Недокументированная команда. Подсмотреть карты)
        self.commands.update({'Болван': self.command_dummy})
        self.commands.update({'Колода': self.command_deck})
        self.commands.update({'Программа': self.command_about})
        self.commands.update({'Стол': self.command_table})
        self.commands.update({'Инфо': self.command_info})
        self.commands.update({'Пас': self.command_pass})
        self.commands.update({'Взял': self.command_get})

    @staticmethod
    def hello():  # Приветствие - выдаст текст "Добро пожаловать в игру".
        string = ''
        string += 'Добро пожаловать в игру "Подкидной Дурак"!\n'
        string += 'Против вас играет простейший алгоритм "Болван"\n'
        string += 'Колода уже перетасована. Карты розданы. Козырь объявлен.\n'
        string += 'Вам предоставляется право первого хода.\n'
        return string

    @staticmethod
    def command_commands():  # Команды - выдаст справку о командах
        string = ''
        string += 'Доступны следующие команды:\n'
        string += 'Выход - выход из игры.\n'
        string += 'Программа - выдаст информацию об этой программе и её разработчиках.\n'
        string += 'Игра - выдаст краткие правила игры.\n'
        string += 'Карты - перечислит все возможные достоинства карт.\n'
        string += 'Масти - перечислит все возможные масти.\n'
        string += 'Козырь - отобразит последнюю карту колоды задающую козырную масть.\n'
        string += 'Колода - сообщит количество карт в колоде.\n'
        string += 'Болван - сообщит количество карт у противника.\n'
        string += 'Стол - отобразит карты лежащие на столе.\n'
        string += 'Рука - отобразит ваши карты.\n'
        string += 'Название карты (Карта-масть) - сообщаете игре свой ход.\n'
        string += 'Пас - сообщаете игре что больше не будете подкидывать карты.\n'
        string += 'Взял - сообщаете игре что больше не будете отбиваться.\n'
        string += 'Инфо - отобразит всю текущюю информацию об игре: Козырь, Колода, Болван, Стол, Рука.\n'
        string += 'Команды - отобразит только что выданную информацию.\n'
        return string

    @staticmethod
    def command_dignity():  # Достоинства - перечислит все возможные достоинства карт.
        return ', '.join(str(dignity) for dignity in Dignity.sequence()) + '.\n'

    @staticmethod
    def command_suit():  # Масти - перечислит все возможные масти.
        return ', '.join(str(suit) for suit in Suit.sequence()) + '.\n'

    @staticmethod
    def command_description():  # Игра - выдаст краткие правила игры.
        string = ''
        string += 'В начале игры на руках противников по 6 карт.\n'
        string += 'Противники по очереди выкладывают карты на стол,\n'
        string += 'сообщая свои ходы в формате: Карта-масть\n'
        string += 'Например: "Дама-пики" или "7-бубны".\n'
        string += 'Начинать атаку можно с любой имеющейся в руке карты.\n'
        string += 'Продолжить атаку можно картой любого достоинства из тех что уже лежат на столе.\n'
        string += 'В случае невозможности или не желания продолжить атаку следует ввести команду "Пас".\n'
        string += 'Тогда право атаки переходит к другому игроку.\n'
        string += 'Отбаваться можно, кроя атакующую карту, картой той же масти, но большего достоинства.\n'
        string += 'Карты бывают следующих достоинств в порядке возрастания старшинства:\n'
        string += Game.command_dignity()
        string += 'Например: "10-червы" бьет "9-червы" или "Туз-трефы" бьет "Валет-трефы".\n'
        string += 'Карту не козырной масти можно побить любой картой козырной масти.\n'
        string += 'Например, если козырь бубны, то: "8-бубны" бьет "Король-пики".\n'
        string += 'Таким образом, козырный "Туз" может побить любую карту и не может быть побит.\n'
        string += 'В игре приняты следующие масти:\n'
        string += Game.command_suit()
        string += 'Порядок мастей не предусмотрен.\n'
        string += 'Козырная масть случайным образом выбирается в начале каждой игры.\n'
        string += 'Карта задавшая козырную масть в игре, становится последней картой колоды.\n'
        string += 'В случае невозможности или не желания отбаваться дальше следует ввести команду "Взял".\n'
        string += 'Тогда все карты со стола переходят в руку неотбившегося игрока.\n'
        string += 'Право атаки остается у атакующего игрока.\n'
        string += 'Кон закачивается после команды "Пас" атакующего игрока, или команды "Взял" отбивающегося.\n'
        string += 'Перед началом следующего хода, игроки добирают в руку карты из колоды,\n'
        string += 'по одной карте, до 6 карт на руке, начиная с атаковавшего игрока.\n'
        string += '(при необходимости, и если на тот момент в колоде остались карты)\n'
        string += 'Игра заканчивается, когда в колоде не остается карт, и рука хотя бы одного из игроков пуста.\n'
        string += 'Цель: остатся без карт в конце игры. Игрок оставшийся с картами в руке, объявляется "Дураком".\n'
        return string

    def command_trump(self):  # Козырь - выдаст последнюю карту колоды задающую козырную масть.
        return str(self.table.trump_card) + '\n'

    def command_hand(self):  # Рука - Выдаст ваши карты.
        return self.hand_gamer.just() + '\n'

    def command_cheat(self):  # cheat - отобразит карты "Болвана". Недокументированная команда)
        return self.hand_dummy.just() + '\n'

    def command_dummy(self):  # Болван - сообщит количество карт у противника.
        return 'Карт у Болвана: ' + str(self.hand_dummy.len()) + '\n'

    def command_deck(self):  # Колода - сообщит количество карт в колоде.
        return 'Карт в колоде: ' + str(self.deck.len()) + '\n'

    @staticmethod
    def command_about():  # Программа - выдаст информацию об этой программе и её разработчиках.
        string = ''
        string += 'Программа разработана Дмитрием Аристарховым, по заданию Дмитрия Ермилова,\n'
        string += 'в рамках курса "Python - разработчик", "Университета искусственного интеллекта".\n'
        string += 'https://neural-university.ru/python-developer\n'
        string += 'P.S. Отдельное спасибо Елене Аристарховой, за разъяснение правил игры и тестирование.\n'
        string += '08.01.2020г.\n'
        return string

    def command_table(self):  # Стол - отобразит карты лежащие на столе.
        return self.table.just() + '\n'

    def command_info(self):  # Инфо - отобразит всю текущюю информацию об игре.
        string = ''
        string += 'Козырь: '+ self.command_trump()  # Козырь - отобразит последнюю карту колоды.
        string += self.command_deck()  # Колода - сообщит количество карт в колоде.
        string += self.command_dummy()  # Болван - сообщит количество карт.
        string += self.command_table()  # Стол - отобразит карты лежащие на столе.
        string += self.command_hand()  # Рука - отобразит ваши карты.
        return string

    def distribution_cards(self, first_gamer=True):  # Раздача карт.
        assert isinstance(first_gamer, bool)
        h1 = self.hand_gamer if first_gamer else self.hand_dummy
        h2 = self.hand_dummy if first_gamer else self.hand_gamer
        last_len = 0
        while last_len != self.deck.len():  # Если карты уже не берут.
            last_len = self.deck.len()
            if h1.len() < 6:
                h1.add_cards(self.deck.get_cards())  # Не страшно раздавать, если что, из пустой колоды)
            if h2.len() < 6:
                h2.add_cards(self.deck.get_cards())

    def command(self, string):  # Интерпритатор команд.
        assert isinstance(string, str)
        if string.find('-') == -1:  # Нет деффиса - значит не карта)
            if string in self.commands:
                return self.commands[string]()
            else:
                return 'Неизвестная команда.\n'

        else:
            card = Card.name(string)

            if card is None:
                return 'Неизвестная карта.\n'

            if not self.hand_gamer.exist(card):
                return 'У вас нет такой карты.\n'

            if not self.table.check(card):
                return 'Так ходить нельзя.\n'

            self.table.go(self.hand_gamer.get_card(card))
            return self.next_go(gamer=True, card=card)

    def command_pass(self):  # Пас - сообщаете игре что больше не будете подкидывать карты.
        if not self.table.is_attack():  # Если нужно отбиватся. Нечетный ход.
            return 'Нельзя пасовать когда отбиваешься.\n'
        if self.table.len() == 0:  # Перый ход.
            return 'Нельзя пасовать первым ходом.\n'

        return self.next_go(gamer=True, card=None)

    def command_get(self):  # Взял - сообщаете игре что больше не будете отбиваться.
        if self.table.is_attack():  # Если нужно подкидывать. Четный ход.
            return 'Нельзя взять когда атакуешь.\n'

        return self.next_go(gamer=True, card=None)

    def dummy(self):  # Искусственный интеллект) Ходит первой попавшейся из минимальных по достоинству.
        suitable_cards = {card for card in self.hand_dummy.cards if self.table.check(card)}  # Годные карты.
        trump_suitable_cards = {card for card in suitable_cards if card.suit() == self.table.trump_suit()}  # Козыри.
        suitable_cards -= trump_suitable_cards  # Не козыри.

        card = None
        if suitable_cards:
            card = min(suitable_cards, key=lambda card: card.dignity())
        elif trump_suitable_cards:
            card = min(trump_suitable_cards, key=lambda card: card.dignity())

        if card is not None:
            self.table.go(self.hand_dummy.get_card(card))
        return self.next_go(gamer=False, card=card)

    def next_go(self, *, gamer, card):  # Подготовка к следующему ходу.
        assert isinstance(gamer, bool)
        assert isinstance(card, Card) or card is None

        attack = self.table.is_attack() if card is None else not self.table.is_attack()
        distribution = False  # Нужна ли пересдача.
        ticket = False  # Право внеочередного хода.
        if card is not None:  # Если ход картой.
            if not attack:  # Если защита (При атаке противник должен отбиватся и это следующий ход).
                if self.hand_gamer.len() == 0 or self.hand_dummy.len() == 0:  # Если у кого нибудь закончились карты.
                    distribution = True  # Пересдача карт нужна.
                    ticket = True  # Молодец, отбился. Теперь ходи первый.
        else:  # Если ход не картой: Пас или Взял.
            if not attack:  # Если защита(Взял).
                if gamer:  # Если взял игрок.
                    self.hand_gamer.add_cards(self.table.get_all_card())  # Все карты со стола ему в руку.
                else:  # Если взял Болван.
                    self.hand_dummy.add_cards(self.table.get_all_card())  # Все карты со стола ему в руку.
            else:
                self.table.clear()  # Очистить стол.
            distribution = True  # Пересдача карт нужна.

        the_end = False  # Закончена ли игра.
        if distribution:  # Если установлен флаг.
            if self.deck.len() == 0:  # Если закончились карты в колоде.
                if not attack:  # При защите
                    the_end = self.hand_gamer.len() == 0 or self.hand_dummy.len() == 0  # У кого-то кончились карты.
            else:  # Карты в колоде не закончились.
                self.distribution_cards(gamer if not ticket else not gamer)  # Начинаем с того кто сейчас ходил.

        string = ''  # Вернём эту строку
        if not gamer:  # Ходил Болван. Вернуть этот ход.
            if card is not None:  # Если ход картой.
                string += str(card) + '\n'
            else:  # Если ход не картой: Пас или Взял.
                if attack:  # Если атака(Пас).
                    string += 'Пас\n'
                else:  # Если защита(Взял).
                    string += 'Взял\n'

        if the_end:  # Игра закончена!
            if self.hand_gamer.len() == 0 and self.hand_dummy.len() == 0:  # Ничья.
                string += 'GameOver:None'
                return string
            if self.hand_gamer.len() == 0:  # Поздравляю с победой над Болваном!
                string += 'GameOver:Gamer'
                return string
            if self.hand_dummy.len() == 0:  # Это фиаско, братан.
                string += 'GameOver:Dummy'
                return string
            assert False  # Не знаю как ты здесь оказался.

        if distribution:  # Если была раздача, вернуть руку для удобства.
            string += self.command_hand()

        if (gamer and not ticket) or (not gamer and ticket):  # Вернуть новый ход Болвана.
            string += self.dummy()

        return string
