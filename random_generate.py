from math import inf
from random import randint
import random

def gen(filename, N, M, hard = True):
  with open(filename,'w') as f:
    smallest = 40
    largest = 60
    
    # Initialize the number of teacher
    number_teacher = randint(2, N//4)

    # Initialize the room capacity
    room_capacity = [randint(smallest, largest) for _ in range(M)]

    # Initialize the state of room and teacher. From the beginning, there
    # are no timetable so all of them is assigned True.
    state_room = [[True for _ in range(M)] for __ in range(60)]
    state_teacher = [[True for _ in range(number_teacher + 1)] for __ in range(60)]
    info_class = [[0,-1,1e10] for _ in range(N)]

    # Initialize the teacher of each class
    CBG = {}
    teacher = [0 for _ in range(number_teacher)]
    classes = [_ for _ in range(N)]
    while len(classes) != 0:
      i = teacher.index(min(teacher))
      choose = random.choice(classes)
      classes.remove(choose)
      info_class[choose][1] = i + 1
      CBG[choose] = i + 1 
      teacher[i] += 1

    # Initialize the number of student in each class
    smallest_class = float("inf")
    for _ in range(N):
      number = randint(smallest - 10, max(room_capacity))
      info_class[_][2] = number
      if number < smallest_class:
        smallest_class = number

    # To make sure that there are no room is left unused.
    if smallest_class > min(room_capacity):
      classes = random.sample([_ for _ in range(N)], N//2)
      while len(classes) != 0:
        temp = classes.pop()
        info_class[temp][2] = randint(smallest - 10, min(room_capacity))

    # Create the number of period in each class which is feasible to solve. 
    # The number of period in one class do not too different with another one. 
    cases = {}
    for c in range(N):
      cases[c] = [(p,r) for p in range(60) for r in range(M)]
    period_each_class = [1 for _ in range(N)]
    count = 0
    while count < len(cases):
      c = period_each_class.index(min(period_each_class))
      case = cases[c]
      if len(case) == 0:
        period_each_class[c] = float("inf")
        count += 1
        continue
      p, r = random.choice(case)
      case.remove((p, r))
      if state_room[p][r] and state_teacher[p][CBG[c]] and info_class[c][2] <= room_capacity[r]:
        state_room[p][r] = False
        state_teacher[p][CBG[c]] = False
        info_class[c][0] += 1
        period_each_class[c] += 1

    # If set the mode hard = False, this mean the number of period  
    # we have randomize above is 4 times to solution it write to file txt.
    if not hard:
      for i in range(len(info_class)):
        info_class[i][0] = info_class[i][0] // 4 + 1
    
    # Write input created to file .txt 
    f.write(f'{N} {M}\n')
    for t, g, s in info_class:
      f.write(f'{t} {g} {s}\n')
    for _ in room_capacity:
      f.write(f'{_} ')

if __name__ == "__main__":
  gen("random_data.txt", 15, 2)
