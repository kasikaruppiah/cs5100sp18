Question 1: Reflex Agent
	compute the following scores and return the sum of all the scores as output
	
	Game Score = Successor Game State Score - Current Game State Score
	Actual Ghost Score = -500 / Manhattan Distance between Pacman and Closest Actual Ghost
	Sacred Ghost Score = 200 / Manhattan Distance between Pacman and Sacred Ghost
	Food Score = 10 / Manhattan Distance betwen Pacman and Closest Food
	Remaining Food = 1 / Number of Food
	Action Score = -2 if action is Direction.STOP

Question 5: Evaluation Function
	compute the Current Game State Score
	get all the legal moves from the current state
	for each legal move calculate if the new state is in food(+10), actual ghost(-500) or sacred ghost(+200) and update the scores accordingly

Time Spent: 15 hrs