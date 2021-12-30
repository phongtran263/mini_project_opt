from random_generate import gen
import time

def input(filename):
  with open(filename) as f:
    [N, M] = [int(x) for x in f.readline().split()]
    info_classes = [[int(x) for x in f.readline().split()] + [i] for i in range(N)]
    rooms = [int(x) for x in f.readline().split()]
  return info_classes, rooms

def Greedy(filename):
  info_classes, rooms = input(filename)
  # Sort base on room's capacity (increasing) 
  rooms_sort = sorted([(rooms[i], i) for i in range(len(rooms))], key = lambda x : x[0])

  G = {}
  for info_class in info_classes:
    teacher = info_class[1]
    G[teacher] = G.get(teacher, [])
    G[teacher].append(info_class)

  # Sort teacher base on the number of shift he/she have to teach (decreasing)
  teachers = sorted(list(G.keys()), key = lambda x: -sum([info_class[0] for info_class in G[x]]))

  state_teacher = [[True for _ in range(len(set(teachers)) + 1)] for __ in range(60)]
  state_room = [[True for _ in range(len(rooms))] for __ in range(60)]
  timetable = {}
  for teacher in teachers:
    info_classes_sort = sorted(G[teacher], key = lambda x: -x[2])
    for info_class in info_classes_sort:
      timetable[info_class[-1]] = []
      for _ in range(info_class[0]): # If we loop this way, we will sure that each class has enough shift.
        x = Select(info_class, state_room, state_teacher, rooms_sort)
        if x == None:
          if not Try(info_class, info_classes, state_room, state_teacher, rooms_sort, timetable):
            return "FAILURE"
        else:
          ChangeState(x, info_class[1], state_room, state_teacher, False)
          timetable[info_class[-1]].append(x)
  return timetable

def Select(info_class, state_room, state_teacher, rooms):
  for shift in range(12):
    for day in range(5):
      p = day * 12 + shift
      for capacity, index_room in rooms:
        if Feasible(info_class, state_room, state_teacher, capacity, p, index_room):
          return p, index_room
  return None

def Try(info_class, info_classes, state_room, state_teacher, rooms, timetable):
  for classArranged in timetable:
    for period, index_room in timetable[classArranged]:

      infoClassArrangeed = info_classes[classArranged]
      teacherClassArrangeed = infoClassArrangeed[1]
      ChangeState((period, index_room), teacherClassArrangeed, state_room, state_teacher, True)
      chooseForNewClass = Select(info_class, state_room, state_teacher, rooms)

      if chooseForNewClass != None:
        ChangeState(chooseForNewClass, info_class[1], state_room, state_teacher, False)
      else:
        ChangeState((period, index_room), teacherClassArrangeed, state_room, state_teacher, False)
        continue

      chooseForOldClass = Select(infoClassArrangeed, state_room, state_teacher, rooms)
      if chooseForOldClass != None:
        timetable[classArranged].remove((period, index_room))
        timetable[classArranged].append(chooseForOldClass)
        timetable[info_class[-1]].append(chooseForNewClass)
        ChangeState(chooseForOldClass, teacherClassArrangeed, state_room, state_teacher, False)
        return True
      else:
        ChangeState(chooseForNewClass, info_class[1], state_room, state_teacher, True)
        ChangeState((period, index_room), teacherClassArrangeed, state_room, state_teacher, False)

  return False

def ChangeState(x, teacher, state_room, state_teacher, state):
  p, index_room = x
  state_room[p][index_room] = state
  state_teacher[p][teacher] = state

def Feasible(info_class, state_room, state_teacher, capacity, p, index_room):
  # At a moment, a teacher teaches at most one class
  if not state_teacher[p][info_class[1]]:
    return False
  # At a moment, a room is used by at most one class
  if not state_room[p][index_room]:
    return False
  # The room's capacity is bigger than the number of student in class
  if info_class[2] > capacity:
    return False
  return True

def PrintSolution(timetable):
  if timetable == "FAILURE":
    print("FAILURE")
    return
  classes = sorted(list(timetable.keys()))
  convert = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  shift = lambda x: 12 if x % 12 == 0 else x % 12
  for i in classes:
    table_sort = sorted(timetable[i])
    for p, r in table_sort:
      print(f'Class {i + 1} has lessons at period {shift(p+1)} on {convert[p//12]} at room {r + 1}')
    print()

if __name__ == "__main__":
  filename = "random_data.txt"
  gen(filename, 15, 2, hard=True)
  start = time.time()
  timetable = Greedy(filename)
  end = time.time()
  PrintSolution(timetable)
  print("Time:", end - start)