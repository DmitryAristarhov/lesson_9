# -*- coding: utf-8 -*-
import card_game_fool as fool

game=fool.Game()
print(game.hello())  # Приветствие - отобразит текст "Добро пожаловать в игру".
print(game.command_commands())  # Список команд.
print('Козырь: ', end='')
print(game.command_trump(), end='')  # Козырь - отобразит последнюю карту колоды задающую козырную масть.
print('Рука: ', end='')
print(game.command_hand())  # Рука - отобразит ваши карты.

while True:  # Основной цикл.
    cmd = input('> ')

    if cmd == 'Выход':
        break

    if cmd == '':
        continue

    string = game.command(cmd)
    split = string.find('GameOver:')

    if split != -1:  # Если игра окончена.

        print(string[:split])
        result = string[split:]

        if result == 'GameOver:None':
            print('Ничья. Не плохо сыграно!')

        if result == 'GameOver:Gamer':
            print('Поздравляю! Вы выиграли.')

        if result == 'GameOver:Dummy':
            print('Вы выиграли проиграли. Вы дурак!')

        break

    print(string)

print('Спасибо за игру. Приходите ещё!\n')
