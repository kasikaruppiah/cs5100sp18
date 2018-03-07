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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [
            self.evaluationFunction(gameState, action) for action in legalMoves
        ]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(
            bestIndices)  # Pick randomly among the best

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
        newGhostStates = successorGameState.getGhostStates()

        "*** YOUR CODE HERE ***"
        actualGhosts = filter(lambda x: not x.scaredTimer, newGhostStates)
        closestActualGhostDist = min(
            map(lambda x: manhattanDistance(newPos, x.getPosition()),
                actualGhosts), 0)
        actualGhostScore = -500.0 / closestActualGhostDist if closestActualGhostDist else -500

        sacredGhosts = filter(lambda x: x.scaredTimer, newGhostStates)
        closestSacredGhostDist = min(
            map(lambda x: manhattanDistance(newPos, x.getPosition()),
                sacredGhosts), 0)
        sacredGhostScore = 200.0 * 2.0 / closestSacredGhostDist if closestSacredGhostDist else 0

        closestFoodDist = min(
            map(lambda x: manhattanDistance(newPos, x), newFood), 0)
        foodScore = 10.0 / closestFoodDist if closestFoodDist else 0
        numFood = successorGameState.getNumFood()
        remainingFood = 1.0 / numFood if numFood else 1

        actionScore = -2 if action == Directions.STOP else 0

        gameScore = successorGameState.getScore() - currentGameState.getScore()

        return actualGhostScore + sacredGhostScore + foodScore + remainingFood + gameScore + actionScore


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        PACMAN = 0
        legalMoves = gameState.getLegalActions(PACMAN)
        successorStates = [
            gameState.generateSuccessor(PACMAN, action)
            for action in legalMoves
        ]

        scores = [self.minVal(state, 0, 1) for state in successorStates]
        bestScore = max(scores)
        bestIndices = [
            index for index, value in enumerate(scores) if value == bestScore
        ]

        return legalMoves[random.choice(bestIndices)]

    def maxVal(self, gameState, currentDepth):
        if self.depth == currentDepth or gameState.isWin() or gameState.isLose(
        ):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(0)
        successorStates = [
            gameState.generateSuccessor(0, action) for action in legalMoves
        ]
        scores = [
            self.minVal(state, currentDepth, 1) for state in successorStates
        ]

        return max(scores)

    def minVal(self, gameState, currentDepth, chosenIndex):
        if self.depth == currentDepth or gameState.isWin() or gameState.isLose(
        ):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(chosenIndex)
        successorStates = [
            gameState.generateSuccessor(chosenIndex, action)
            for action in legalMoves
        ]

        if (chosenIndex < gameState.getNumAgents() - 1):
            scores = [
                self.minVal(state, currentDepth, chosenIndex + 1)
                for state in successorStates
            ]
        else:
            scores = [
                self.maxVal(state, currentDepth + 1)
                for state in successorStates
            ]

        return min(scores)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float('inf')
        beta = float('inf')
        PACMAN = 0
        legalMoves = gameState.getLegalActions(PACMAN)

        bestScore = -float('inf')
        bestAction = legalMoves[0]
        for action in legalMoves:
            nextState = gameState.generateSuccessor(PACMAN, action)
            score = self.minVal(nextState, 0, 1, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            if score > beta:
                return bestAction
            alpha = max(alpha, score)

        return bestAction

    def maxVal(self, gameState, currentDepth, alpha, beta):
        if self.depth == currentDepth or gameState.isWin() or gameState.isLose(
        ):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(0)
        bestScore = -float('inf')
        for action in legalMoves:
            nextState = gameState.generateSuccessor(0, action)
            bestScore = max(bestScore,
                            self.minVal(nextState, currentDepth, 1, alpha,
                                        beta))
            if bestScore > beta:
                return bestScore
            alpha = max(alpha, bestScore)

        return bestScore

    def minVal(self, gameState, currentDepth, chosenIndex, alpha, beta):
        if self.depth == currentDepth or gameState.isWin() or gameState.isLose(
        ):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(chosenIndex)
        bestScore = float('inf')
        for action in legalMoves:
            nextState = gameState.generateSuccessor(chosenIndex, action)
            numAgents = gameState.getNumAgents() - 1
            if (chosenIndex < numAgents):
                bestScore = min(bestScore,
                                self.minVal(nextState, currentDepth,
                                            chosenIndex + 1, alpha, beta))
            else:
                bestScore = min(bestScore,
                                self.maxVal(nextState, currentDepth + 1, alpha,
                                            beta))
            if bestScore < alpha:
                return bestScore
            beta = min(beta, bestScore)

        return bestScore


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
        PACMAN = 0
        legalMoves = gameState.getLegalActions(PACMAN)
        successorStates = [
            gameState.generateSuccessor(PACMAN, action)
            for action in legalMoves
        ]

        scores = [self.expVal(state, 0, 1) for state in successorStates]
        bestScore = max(scores)
        bestIndices = [
            index for index, value in enumerate(scores) if value == bestScore
        ]

        return legalMoves[random.choice(bestIndices)]

    def maxVal(self, gameState, currentDepth):
        if self.depth == currentDepth or gameState.isWin() or gameState.isLose(
        ):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(0)
        successorStates = [
            gameState.generateSuccessor(0, action) for action in legalMoves
        ]
        scores = [
            self.expVal(state, currentDepth, 1) for state in successorStates
        ]

        return max(scores)

    def expVal(self, gameState, currentDepth, chosenIndex):
        if self.depth == currentDepth or gameState.isWin() or gameState.isLose(
        ):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(chosenIndex)
        successorStates = [
            gameState.generateSuccessor(chosenIndex, action)
            for action in legalMoves
        ]

        if (chosenIndex < gameState.getNumAgents() - 1):
            scores = [
                self.expVal(state, currentDepth, chosenIndex + 1)
                for state in successorStates
            ]
        else:
            scores = [
                self.maxVal(state, currentDepth + 1)
                for state in successorStates
            ]

        return sum(scores) / len(scores)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: get currentGameState score and update it if the newGameState
      results on a food or ghost
    """
    "*** YOUR CODE HERE ***"
    currPos = currentGameState.getPacmanPosition()
    legalMoves = currentGameState.getLegalActions()
    currFoods = currentGameState.getFood()

    score = currentGameState.getScore()
    for action in legalMoves:
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()

        if newPos in currFoods:
            score += 10

        ghostStates = successorGameState.getGhostStates()
        actualGhosts = map(lambda x: x.getPosition(),
                           filter(lambda x: not x.scaredTimer, ghostStates))
        if newPos in actualGhosts:
            score -= 500
        sacredGhosts = map(lambda x: x.getPosition(),
                           filter(lambda x: x.scaredTimer, ghostStates))
        if newPos in sacredGhosts:
            score += 200

    return score


# Abbreviation
better = betterEvaluationFunction
