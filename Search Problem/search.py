# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    from util import Stack

    explored = []        #nodes explored
    Frontier = Stack()   #LIFO Queue
    
    initialNode = problem.getStartState()
    
    #if initial node is goal node: return
    if problem.isGoalState(initialNode):
        return []
    
    Frontier.push((initialNode, []))
    #print("\nI used the depth first search algorithm.\n")
    
    #while frontier is non-empty: run loop
    while not Frontier.isEmpty():
        curr, actionSet = Frontier.pop()  #pop last enqued item
        #print("\nCurrent node : ", curr)
        
        if curr not in explored:
            explored.append(curr)       #and add to explored set if its not already present
        #print("\nExplored set : ", explored)
        
        if problem.isGoalState(curr):   #if current node is the goal, return the set of actions.
            #print("\n***Current node is the final node so end function***")
            return actionSet
            
        for Next, action, cost in problem.getSuccessors(curr):
            if Next not in explored:
                nextAction = actionSet + [action]
                Frontier.push((Next, nextAction))
        #print("\nFrontier : ", Frontier)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    from util import Queue
    
    explored = []        #nodes explored
    Frontier = Queue()   #FIFO Queue
    
    initialNode = problem.getStartState()
    
    #if initial node is goal node: return
    if problem.isGoalState(initialNode):
        print("\nyes its goal state\n")
        return []
    
    Frontier.push((initialNode, []))
    #Frontier.push((Frontier, initialNode))
    #while frontier is non-empty: run loop
    while not Frontier.isEmpty():
        curr, actionSet = Frontier.pop()  #pop last enqued item
        #print("\nCurrent node : ", curr)
        
        if curr not in explored:
            explored.append(curr)       #and add to explored set if its not already present
        #print("\nExplored set : ", explored)
            if problem.isGoalState(curr):   #if current node is the goal, return the set of actions.
                #print("\n***Current node is the final node so end function***")
                return actionSet
            for Next, action, cost in problem.getSuccessors(curr):
                if Next not in explored:
                    if Next not in (next_state[0] for next_state in Frontier.list):
                        nextAction = actionSet + [action]
                        Frontier.push((Next, nextAction))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    
    explored = []        #nodes explored
    Frontier = PriorityQueue()   #Priority Queue
    initialNode = problem.getStartState()
    
    #if initial node is goal node: return
    if problem.isGoalState(initialNode):
        return []
    
    Frontier.push((initialNode, [],0),0)
    curr = initialNode
   
    while not Frontier.isEmpty():
        
        curr, actionSet, cost = Frontier.pop()  #pop last enqued item
        
        if curr not in explored:
            explored.append(curr)       #and add to explored set if its not already present
        
            if problem.isGoalState(curr):   #if current node is the goal, return the set of actions.
                return actionSet
            flag = 0
            for Next, action, newcost in problem.getSuccessors(curr):
                nextAction = actionSet + [action]
                pathCost = cost + newcost
                if Next not in explored:
                    for i in range(len(Frontier.heap)):
                        if Next == tuple(Frontier.heap)[i][2][0]:
                            flag=1    #frontier contains Next
                            if pathCost<tuple(Frontier.heap)[i][2][2]:
                                Frontier.update((Next, nextAction, pathCost),pathCost)
                    if flag == 0:     #frontier does not contain Next
                        Frontier.push((Next,nextAction, pathCost),pathCost)                  
                
                
                
                
                #a = tuple(Frontier.heap)
                #print("\n next = ", Next)
#                 print("a[1] = ", tuple(Frontier.heap)[0][2][0])
                
                  
    util.raiseNotDefined()
    
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

                    
    from util import PriorityQueue
    
    explored = []        #nodes explored
    Frontier = PriorityQueue()   #Priority Queue
    initialNode = problem.getStartState()
    
    #if initial node is goal node: return
    if problem.isGoalState(initialNode):
        return []
    h1=heuristic(initialNode,problem)
    Frontier.push((initialNode, [],0),0+h1)
    curr = initialNode
    while not Frontier.isEmpty():
        curr, actionSet, cost = Frontier.pop()  #pop last enqued item
        if curr not in explored:
            explored.append(curr)       #and add to explored set if its not already present
            if problem.isGoalState(curr):   #if current node is the goal, return the set of actions.
                return actionSet
            flag = 0
            for Next, action, newcost in problem.getSuccessors(curr):
                nextAction = actionSet + [action]
                h=heuristic(Next,problem)
                pathCost = cost + newcost 
                if Next not in explored:
                    for i in range(len(Frontier.heap)):
                        if Next == tuple(Frontier.heap)[i][2][0]:
                            flag=1    #frontier contains Next
                            if pathCost<tuple(Frontier.heap)[i][2][2]:
                                Frontier.update((Next, nextAction, pathCost),pathCost+h)
                    if flag == 0:     #frontier does not contain Next
                        Frontier.push((Next,nextAction, pathCost),pathCost+h)                  

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
