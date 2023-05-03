import time
import pygame
from spade import quit_spade
from Agents.moderator import ModeratorAgent
from Agents.commander import CommanderAgent
from Agents.soldier import SoldierAgent
from Classes.coordinates import Coordinates
from Classes.infocommander import InfoCommander
from Classes.infosoldado import InfoSoldado
from constants import *


def display(win):
    run = True
    clock = pygame.time.Clock()

    while run:
        try:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            moderator.board.draw(win)
            pygame.display.update()
        except KeyboardInterrupt:
            run = False

    pygame.quit()


def createModerator():
    global moderator
    if moderator is None:
        mod = ModeratorAgent("moderator@" + SERVER, PASSWORD, X_MAX, Y_MAX)
        moderator = mod
        return mod
    return moderator


def createTeam(team_str: str, number_soldiers: int):
    global commanders
    global soldiers
    if team_str not in commanders.keys():
        comman = CommanderAgent("commander_{}@".format(team_str) + SERVER, PASSWORD, X_MAX, Y_MAX)
        comman.info = InfoCommander(comman.jid, team_str)
        commanders[team_str] = comman
        team_list = []
        team_dic = {}
        for num in range(1, number_soldiers + 1):
            sol = SoldierAgent("soldier_{}_{}@".format(team_str, str(num)) + SERVER, PASSWORD)
            sol.info = InfoSoldado(sol.jid, team_str, Coordinates(-1, -1))
            team_list.append(sol)
            team_dic[str(sol.jid)] = sol
        comman.soldiers_alive = team_dic
        soldiers.append(team_list)
        return comman
    else:
        print("Team {} already exists".format(team_str))
        return commanders.get(team_str)


moderator = None
commanders = {}
soldiers = []

if __name__ == '__main__':
    moderator = createModerator()
    counter = 0
    for team_name in TEAM_NAMES:
        time.sleep(0.1)
        if type(N_SOLDIERS) is int:
            commander = createTeam(team_name, N_SOLDIERS)
        else:
            commander = createTeam(team_name, N_SOLDIERS[counter])
            counter += 1

    print("------------------------------------------------------------------------------------------------------------")
    res_moderator = moderator.start()
    res_moderator.result()
    for team in commanders.keys():
        com = commanders[team]
        com_res = com.start()
        com_res.result()
    for key in range(len(soldiers)):
        for soldier_agent in soldiers[key]:
            soldier_agent.start()

    print("------------------------------------------------------------------------------------------------------------")
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moderator View")

    # Handle interruption of all agents
    while moderator.is_alive() and display(window):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # stop all soldier Agents
            for key in range(len(soldiers)):
                for soldier_agent in soldiers[key]:
                    if soldier_agent.is_alive():
                        soldier_agent.stop()

            # stop all commander Agents
            for key in commanders.keys():
                if commanders[key].is_alive():
                    commanders[key].stop()

            # stop manager agent
            if moderator.is_alive():
                moderator.stop()
            break
    print('Agents finished')

    # finish all the agents and behaviors running in your process
    quit_spade()
