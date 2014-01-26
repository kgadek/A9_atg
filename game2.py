from random    import *
from itertools import *
from sys       import *

# player_names = ["pioro","anielski","ostaszewski","goik"]
# test = True






def createPlayers( names ):
  players = []
  i = 0
  for name in names:
#    print name
    X = __import__(name)
    players += [ X.Player() ]
    try:
      players[i].setName(i+1)
    except:
      pass
    i+=1

  return players




def whoWon( names, points ):
  winners = []
  M = max( points )
  for i in range(4):
    if( points[i] == M ):
      winners += [names[i]]
  return winners



def games( names ):
  all_winners = []

  for order in permutations(names):
    plrs = ""
    for i in range(4):
      plrs += str(i+1) + "-" + order[i] + ",   "
    print "NEW GAME = ", plrs


    players = createPlayers( order )
    points = game( players )

    winners = whoWon( order, points )
    all_winners += winners

    plrs = ""
    for i in range(4):
      plrs += order[i] + " = " + str(points[i]) + "   "
    print "RESULT = ", plrs, "   WINNERS = ", winners

  return all_winners




def game( players ):
  dice_count = [ 1, 1, 1, 1 ]
  points     = [ 0, 0, 0, 0 ]   

  starting_player = 1

  for i in range(5):
    (dice_count, pts, starting_player ) = playRound( players, dice_count, starting_player )
    points = [ points[i]+pts[i] for i in range(4) ]
  return points


def getDices( dice_count ):
  dices = ["","","",""]
  for i in range(4):
    dices[i] = []
    for j in range( dice_count[i] ):
      dices[i] += [choice(["1","2","3","4","5","6"])]
  return dices





def verifyCall( call, prev_call, total_dices, pl ):
  if( call == "CHECK" ):
    return call
  if( len(call) !=  total_dices ):
    return "LOST BY INCORRECT CALL: length (%s)" % call

  for c in call:
    if( int(c) < 1 ):
      return "LOST BY INCORRECT CALL: incorret symbol in call (%s)" % call
    if( int(c) > 6 ):
      return "LOST BY INCORRECT CALL: incorret symbol in call (%s)" % call

  geq  = True
  grt  = False
  if( call != "CHECK" ):
    for i in range(len(prev_call)):
      if(int(call[i]) > int(prev_call[i])):
        grt = True
      if(int(call[i]) < int(prev_call[i])):
        geq = False



  if (not geq) or (not grt):
    return "LOST BY INCORRECT CALL: not a succeeding call (%s,%s)" % (call, prev_call)

  
  return ''.join(sorted(call))





def checkResult( history, all_dices ):
  player = history[0][0]-1
  call   = history[0][1]

  GAME_LOST = ((player-1) % 4 , player        , False)
  GAME_WON  = (player         ,(player-1) % 4 , False)
  GAME_ON   = (0              , 0             , True)

  if( call[0:4] == "LOST" ):
    return GAME_LOST


  # check na poczatku gry to przegrana
  if( len(history) == 1 ):
    if( call == "CHECK" ):
      return GAME_LOST
    else:
      return GAME_ON

  prev_call   = history[1][1]

  if( call == "CHECK" ):
    for i in range(len(all_dices)):
      if(prev_call[i] > all_dices[i]):
        return GAME_WON
    return GAME_LOST 


#  if( int(call) <= int(prev_call) ):
#    return GAME_LOST
    
  return GAME_ON
    
    




def playRound( players, dice_count, starting_player ):

  points   = [0,0,0,0]
  history  = []
  winner   = 0
  loser    = 0
  game_on  = True

  total_dices = sum(dice_count)
  prev_call = "0" * total_dices
  dices = getDices( dice_count)
#  history  = [[0,"0"*total_dices]]

  
  all_dices = ''.join(sorted(chain.from_iterable(dices)))
#  print "Dices = ", all_dices  

  for i in range(4):
    try:
      players[i].start( dices[i] )
    except:
      pass

  current_player = starting_player-1
  while( game_on ):
    try:
      call = "not-set-call"
      call = players[current_player].play( history ) 
      call = verifyCall( call, prev_call, total_dices, current_player )
    except:
      call = "LOST BY CAUSING EXCEPTION (%s)" % str(call)
    history = [[current_player+1, call]] + history
#    print history
    (winner, loser, game_on ) = checkResult( history, all_dices ) 
#    print (winner, loser, game_on )
    current_player  = (current_player+1)%4
    prev_call = call


  dice_count[loser] +=1
  points[loser]     = -1
  points[winner]    = 1

#  print "PTS = ", points, "   DICES = ", all_dices,  "   GAME = ", history
  print "PTS = ", points, "   DICES = ", "".join(sorted(dices[0]))+"-"+"".join(sorted(dices[1]))+"-"+"".join(sorted(dices[2]))+"-"+"".join(sorted(dices[3])) + " / "+all_dices,  "   GAME = ", history



  for i in range(4):
    try:
      players[i].result( points, dices, history )   
    except: 
      print "EXCEPTION IN RESULT: player %d, perhaps you should fix your `result' function to include the history argument" %(i+1)
      pass

  
  return (dice_count, points, loser+1)





if __name__ == "__main__":
   
  seed()
  if len(argv) < 5:
    print "Invocation:"
    print "   game player1 player2 player3 player4"
    exit()

  all_winners = games( argv[1:5] )

  print "WINNERS OF THE GAME:"
  for name in all_winners:
    print name




















