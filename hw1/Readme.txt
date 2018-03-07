Question 6: Corner Problem: Heuristic

  maximum manhattan distance between current position and unvisited corners
  Cost: 106
  Time: 0.1 seconds
  Nodes Expanded: 1136

  Other attempts:
  1:
    add manhattan distance between current position and all unvisited corners
    Cost: 106
    Time: 0.0 seconds
    Nodes Expanded: 502
    FAIL: Inadmissible heuristic
  2:
    minimum manhattan distance between current position and unvisited corners
    Cost: 106
    Time: 0.8 seconds
    Nodes Expanded: 2838
    FAIL: heuristic non-zero at goal
    FAIL: Heuristic resulted in expansion of 2838 nodes

Question 7: Eating All the Dots

  maximum maze distance between current position and available food
  Cost: 60
  Time: 28.5 seconds
  Nodes Expanded: 4137

  Other attempts:
  1.
    maximum manhattan distance between current position and available food
    Cost: 60
    Time: 16.1 seconds
    Nodes Expanded: 9551
    FAIL: test_cases/q7/food_heuristic_grade_tricky.test

Time Spent: 10 Hrs
