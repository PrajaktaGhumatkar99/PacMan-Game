# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        currFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        from util import manhattanDistance
        
#         print("\nnewPos = ", newPos)
#         print("\nnewFood = ", newFood)
#         print("\nnewScaredTimes = ", newScaredTimes)
#         print("\nCurrent = ",len(currFood.asList()))
#         print("\nSuccessor = ",len(newFood.asList()))
        food = newFood.asList()
        foodDistances = []
        ghostDistances = []
        score = 0 
        score += successorGameState.getScore()
        # dist of successor from every food
        for i in food:
            foodDistances.append(manhattanDistance(newPos,i))
        
        # Calculate distance from every ghost #
        for g in successorGameState.getGhostPositions():
            ghostDistances.append(manhattanDistance(g,newPos))

#         print("\n\nFood Distances = ", foodDistances)
#         print("\nGhost Distances = ", ghostDistances)
        
#         foodAvailable = newFood.asList(True)
#         score -= 
        
        if len(newFood.asList()) < len(currFood.asList()):
            score += len(currFood.asList()) - len(newFood.asList())
            
        for i in foodDistances:
            if i <= 5:
                score += 1
            elif i <= 10:
                score += 0.4
            else:
                score += 0.2
        
        #add score if pacman eats the power pallet
        if newPos in currentGameState.getCapsules():
            score += 1.5
            #print("Ate capsule")
                
        # penalty based on ghost and pacman positions
        for i in ghostDistances:
            if i <= 5:
                score = 1 - score

        return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        #max agent : pacman => agent is 0
        def maxValue(gameState, depth):
            nextDepth = depth+1
            
#             print("gammestate = ", gameState)
#             print("\ndepth = ", depth)
            #if terminal state is reached return utility()
            if(gameState.isWin() or gameState.isLose() or nextDepth == self.depth):
                return self.evaluationFunction(gameState)
                
            v = -999999
            actions = gameState.getLegalActions(0)   #0 -> pacman
                
            for a in actions:
                s=gameState.generateSuccessor(0,a)
                v=max(v,minValue(s,nextDepth,1))
                
            return v
            
        #min agents : ghosts => agent index is passed as arguement
        def minValue(gameState, depth, agidx):
            #print("\n------------------------------------------------------")
            
            #if terminal state is reached return utility()
            if(gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
                
            v = 999999
            actions = gameState.getLegalActions(agidx)
                
            for a in actions:
                s=gameState.generateSuccessor(agidx,a)
                #v assigned based on agent index (1/2)
                if agidx == (gameState.getNumAgents()-1):    #agidx = 2
                    v = min (v,maxValue(s,depth))
                    #print("AGIDX = ",agidx)
                else:                                        #agidx = 1
                    v = min(v,minValue(s,depth,agidx+1))
                    #print("agidx = ",agidx)
                
            return v
            
        #actions of pacman so idx is 0
        actions = gameState.getLegalActions(0)
            
        #initialize score with neg(infinity)
        score = -999999
            
        for a in actions:
            s = gameState.generateSuccessor(0,a)
            temp = minValue(s,0,1)
            if temp > score:
                result = a     #update for better/optimal action
                score = temp
            
        return result

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #max agent : pacman => agent is 0
        def maxValue(gameState, depth, alpha, beta):
            nextDepth = depth+1
            
            #if terminal state is reached return utility()
            if(gameState.isWin() or gameState.isLose() or nextDepth == self.depth):
                return self.evaluationFunction(gameState)
                
            v = -999999
            alphaPrime = alpha   #because we update alpha in this(maxValue) func 
            actions = gameState.getLegalActions(0)
                
#             print("\n------------------------------------------------------")
            for a in actions:
                s = gameState.generateSuccessor(0,a)
                v = max(v,minValue(s, nextDepth, 1, alphaPrime, beta))
                #update alpha if required
                if v > beta:
                    return v
                alphaPrime = max(alphaPrime,v)
#                 print("ABP max : ", a, alphaPrime, beta)
                
            return v
            
        #min agents : ghosts => agent index is passed as arguement
        def minValue(gameState, depth, agidx, alpha, beta):
            
            #if terminal state is reached return utility()
            if(gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
                
            v = 999999
            betaPrime = beta     ##because we update beta in this(minValue) func 
            actions = gameState.getLegalActions(agidx)
            
#             print("\n------------------------------------------------------")         
            for a in actions:
                s=gameState.generateSuccessor(agidx,a)
                #v assigned based on agent index (1/2)
                if agidx == (gameState.getNumAgents()-1):     #agidx = 2
                    v = min (v,maxValue(s, depth, alpha, betaPrime))
                    #update beta if required
                    if v < alpha:
                        return v
                    betaPrime = min(betaPrime,v)
                else:                                          #agidx = 1
                    v = min(v,minValue(s,depth,agidx+1,alpha, betaPrime))
                    if v < alpha:
                        return v
                    betaPrime = min(betaPrime,v)
#                 print("ABP min : ", a, alpha, betaPrime)
            return v
            
        #actions of pacman so idx is 0
        actions = gameState.getLegalActions(0)
            
        #initialize score with neg(infinity)
        score = -999999
        alpha = -999999
        beta = 999999
        
        for a in actions:
#             print("\n-------------New Layer----------")
            s = gameState.generateSuccessor(0,a)
            temp = minValue(s,0,1,alpha, beta)
#             print("temp= ", temp)
            if temp > score:
                result = a
                score = temp
#                 print("score updated= ", score)
            #update alpha IF required (since we call minValue to calculate temp)
            if temp > beta:
                return result
            alpha = max(alpha,temp)
            
        return result

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #max agent : pacman => agent is 0
        def maxValue(gameState, depth):
            nextDepth = depth+1
            
            #if terminal state is reached return utility()
            if(gameState.isWin() or gameState.isLose() or nextDepth == self.depth):
                return self.evaluationFunction(gameState)
                
            v = -999999
            actions = gameState.getLegalActions(0)
                
            for a in actions:
                s=gameState.generateSuccessor(0,a)
                v=max(v,expValue(s,nextDepth,1))
                
            return v
        
        #to calculate expected value score => for the ghosts (agent index req)
        def expValue(gameState, depth, agidx):
            #terminal state
            if(gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            
            #print("\n------------------------------------------------------")
            actions = gameState.getLegalActions(agidx)
            total_e = 0 #initialize total score
            
            for a in actions:
#                 print("\n------------------------------------------------------")
                s=gameState.generateSuccessor(agidx,a)
#                 print("action = ", a)
                if agidx == (gameState.getNumAgents()-1):
                    e = maxValue(s,depth)
#                     print("max e = ",e)
                else:
                    e = expValue(s,depth,agidx+1)
#                     print("exp e = ",e)
                total_e += e    #update total score value
#                 print("updated total_e = ", total_e)
            if(len(actions) == 0):     #terminate function
                    return 0
            #since probbaility is not given consider it as 1 and take average of terminal nodes
#             print("len of actions = ", len(actions))
            size1 = float(len(actions))
            return total_e/size1          #calculate value for node as average
            
        
        #actions of pacman so idx is 0
        actions = gameState.getLegalActions(0)
            
        #initialize score with neg(infinity)
        score = -999999
            
        for a in actions:
            s = gameState.generateSuccessor(0,a)
            temp = expValue(s,0,1)
            if temp > score:
                result = a
                score = temp
            
        return result
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    
    1. Calculating relative score => score = score + current.getScore()
    2. Calculate food distances from pacman => score = score - no. of food left
    3. Add reciprocal of sum food distances to score
    4. If pacman eats a power pellet, add 2(double the value for normal food) to score
    5. If ghost is scared, and closer to pacman, add the distance to the score. If the pacman is farther away from ghost when its scared, subtract reciprocal of distance.
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    score = 0
    score += currentGameState.getScore()
    noOfFood = len(newFood.asList(True))
    food = newFood.asList()
    foodDistances = []
    # dist of pacman from every food
    for i in food:
        foodDistances.append(manhattanDistance(newPos,i))
    
    score -= noOfFood
    
    if sum(foodDistances)>0:
        score += 1/sum(foodDistances)
        
    if newPos in currentGameState.getCapsules():
            score += 2
#             print("Ate capsule")
    
    ghostList = []
    for g in newGhostStates:
        ghostList.append(g.getPosition())
    
    ghostDistances = []
    for g in ghostList:
        ghostDistances.append(manhattanDistance(newPos,g))
    
#     print("\nGhost dist = ", ghostDistances[0])
    
    if sum(newScaredTimes) > 0:
        if ghostDistances[0] < 5:
            score += ghostDistances[0]
        else:
            score -= 1/ghostDistances[0]
    
    return score
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
