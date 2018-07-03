from Game import *
import SolverOptimized as solver
import time
'''
Author: Devin B, dpb246

Calls all the functions to play the game
'''
#Number of games to play
number_of_games = 3

#Init game class
game = Binary()
#Number of times it solves it
success = 0
#store time taken to solve puzzle, not time taken to click/wait for website
times = list()
for i in range(number_of_games):
    #Start new game
    game.new_episode()
    print("Game:", i)
    #Get starting board from screen data
    board = game.get_board()
    #Solve the board
    start_time = time.time()
    solved_board = solver.Main(board) #Call the solver function
    stop_time = (time.time() - start_time)
    times.append(stop_time)
    print("--- %s seconds ---" % stop_time)
    print(solved_board)
    #Output solved board into website and check if it was correct
    if game.try_finish(solved_board) == True:
        success += 1
    #Wait for website to reset
    time.sleep(3)
print("Average of:", "--- %s seconds ---" % (sum(times)/len(times)))
print("Solved %.4f percent of trys" % (success/number_of_games), )
