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
  # Sort depend on room's capacity (increasing) 
  rooms_sort = sorted([(rooms[i], i) for i in range(len(rooms))], key = lambda x : x[0])

  # Sort depend on the number of student (decreasing)
  info_classes_sort = sorted(info_classes, key = lambda x: -x[2])
  teacher = [g for t, g, s, _ in info_classes]
  state_teacher = [[True for _ in range(len(set(teacher)) + 1)] for __ in range(60)]
  state_room = [[True for _ in range(len(rooms))] for __ in range(60)]
  timetable = {}
  for info_class in info_classes_sort:
    timetable[info_class[-1]] = []
    for _ in range(info_class[0]): # If we loop this way, we will sure that each class has enough shift.
      x = Select(info_class, state_room, state_teacher, rooms_sort)
      if x == None:
        return "FAILURE"
      timetable[info_class[-1]].append(x)
  return timetable

def Select(info_class, state_room, state_teacher, rooms):
  for p in range(60):
    for capacity, index_room in rooms:
      if Feasible(info_class, state_room, state_teacher, capacity, p, index_room):
        state_room[p][index_room] = False
        state_teacher[p][info_class[1]] = False
        return p, index_room
  return None

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
    for p, r in timetable[i]:
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