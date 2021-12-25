from random import randint
import random

def gen(filename, N, M, hard = True):
  with open(filename,'w') as f:
    f.write(f'{N} {M}\n')
    number_teacher = randint(2, N//4)
    
    #Initialize the room capacity
    room_capacity = [randint(30,60) for _ in range(M)]
    state_room = [[True for _ in range(M)] for __ in range(60)]
    state_teacher = [[True for _ in range(number_teacher + 1)] for __ in range(60)]
    info_class = [[0,-1,1e10] for _ in range(N)]

    # Initialize the teacher of each class
    CBG = {}
    teacher = [_ for _ in range(1, 1 + number_teacher)]
    for _ in range(N):
      if len(teacher) != 0: # To make sure that each teacher teach at least one class
        index_teacher = random.choice(teacher)
        teacher.remove(index_teacher)
      else:
        index_teacher = randint(1, number_teacher)
      info_class[_][1] = index_teacher
      CBG[_] = index_teacher

    # Initialize the number of student in each class
    cases = [(p, c, r) for p in range(60) for c in range(N) for r in range(M)]
    count = 0
    while count < N:
      p, c, r = random.choice(cases)
      cases.remove((p, c, r))
      if state_room[p][r] and state_teacher[p][CBG[c]] and info_class[c][0] == 0:
        state_room[p][r] = False
        state_teacher[p][CBG[c]] = False
        count += 1
        info_class[c][2] = room_capacity[r] - randint(0,10)
        info_class[c][0] += 1

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
      
    for t, g, s in info_class:
      f.write(f'{t} {g} {s}\n')
    for _ in room_capacity:
      f.write(f'{_} ')

if __name__ == "__main__":
  gen("test.txt", 15, 2)
  print(1e10)