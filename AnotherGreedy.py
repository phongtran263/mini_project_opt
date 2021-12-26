from random_generate import gen
import time

def input(filename):
  with open(filename) as f:
    [N, M] = [int(x) for x in f.readline().split()]
    info_classes = [[int(x) for x in f.readline().split()] for _ in range(N)]
    rooms = [int(x) for x in f.readline().split()]
  return info_classes, rooms

def Greedy(filename):
  info_classes, rooms = input(filename)
  teacher = [g for t, g, s in info_classes]
  state_teacher = [[True for _ in range(len(set(teacher)) + 1)] for __ in range(60)]
  state_room = [[True for _ in range(len(rooms))] for __ in range(60)]
  timetable = {}
  for i in range(len(info_classes)):
    info_class = info_classes[i]
    timetable[i] = []
    for _ in range(info_class[0]):
      x = Select(info_class, state_room, state_teacher, rooms)
      if x == None:
        return "FAILURE"
      timetable[i].append(x)
  return timetable

def Feasible(info_class, state_room, state_teacher, rooms, p, r):
  # At a moment, a teacher teaches at most one class
  if not state_teacher[p][info_class[1]]:
    return False
  # At a moment, a room is used by at most one class
  if not state_room[p][r]:
    return False
  # The room's capacity is bigger than the number of student in class
  if info_class[2] > rooms[r]:
    return False
  return True

def Select(info_class, state_room, state_teacher, rooms):
  for p in range(60):
    for r in range(len(rooms)):
      if Feasible(info_class, state_room, state_teacher, rooms, p, r):
        state_room[p][r] = False
        state_teacher[p][info_class[1]] = False
        return p, r
  return None

def PrintSolution(timetable):
  if timetable == "FAILURE":
    print("FAILURE")
    return
  classes = sorted(list(timetable.keys()))
  convert = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  shift = lambda x: 12 if x % 12 == 0 else x % 12
  for i in classes:
    for p, r in timetable[i]:
      print(f'Class {i+1} has lessons at period {shift(p+1)} on {convert[p//12]} at room {r}')
    print()

if __name__ == "__main__":
  filename = "random_data.txt"
  gen(filename, 15, 2, hard=True)
  start = time.time()
  timetable = Greedy(filename)
  end = time.time()
  PrintSolution(timetable)
  print("Time:", end - start)