# Smart Systems

Folder dedicated to the group assignment developed in the Smart System course (winter semester 2022-2023).

The goal was to create a board game, where two teams of 5 elements would try to eliminate each other. Soldiers are eliminated when blocked on the four possible directions of movement (up, down, left, right), either by enemies, teammates or the board limits.

Strategies were created in order to collect intel and find enemies, coordinate attacks and avoiding blockages. Movements were defined based on a score grid system, created based on the available collective information of the board (vision of each soldier is a 7x7 square centered on its position).

Agents communication was made using the Spade library. 3 types of agents created: moderator, commander (1 for each team) and players.
