from random_generate import gen
import time

class Constraint(object):

    def __init__(self, info_classes, rooms) -> None:
        number_of_teacher = len(set([g for t, g, s in info_classes]))
        self.info_classes = info_classes
        self.rooms = rooms
        self.state_teacher = [[True for _ in range(number_of_teacher + 1)] for __ in range(60)]
        self.state_room = [[True for _ in range(len(rooms))] for __ in range(60)]


    def Feasible(self, index_class, index_room, period) -> bool:

        # At a moment, a teacher teaches at most one class
        teacher = self.info_classes[index_class][1]
        if not self.state_teacher[period][teacher]:
            return False

        # At a moment, a room is used by at most one class
        if not self.state_room[period][index_room]:
            return False

        # The room's capacity is bigger than the number of student in class
        capacity = self.rooms[index_room]
        numberOfStudents = self.info_classes[index_class][2]
        if numberOfStudents > capacity:
            return False

        return True

    def Set_State(self, index_class, index_room, period, state) -> None:
        teacher = self.info_classes[index_class][1]
        self.state_room[period][index_room] = state
        self.state_teacher[period][teacher] = state

class BackTrackingAlgorithm(object):

    def __init__(self, filename, time_limit = 100):
        self.time_limit = time_limit
        self.info_classes, self.rooms = self.input(filename)
        self.AllowTry = [True for _ in range(len(self.info_classes) + 1)]
        self.constraint = Constraint(self.info_classes, self.rooms)
        self.timetable = {i:[] for i in range(len(self.info_classes))}
        self.start = time.time()
        self.Solve()

    def input(self, filename):
        with open(filename) as f:
            [N, M] = [int(x) for x in f.readline().split()]
            info_classes = [[int(x) for x in f.readline().split()] for _ in range(N)]
            rooms = [int(x) for x in f.readline().split()]
        return info_classes, rooms


    def Solve(self):

        # Sort base on room's capacity (increasing) 
        index_rooms_sorted      = sorted([i for i in range(len(self.rooms))], key = lambda x : self.rooms[x])
        
        # Sort class base on the number of students (decreasing)
        index_classes_sorted    = sorted([i for i in range(len(self.info_classes))], key = lambda x: -self.info_classes[x][2])
        
        self.BackTrack(index_classes_sorted, index_rooms_sorted)

    def Select(self, index_class, index_rooms_sorted):
        for shift in range(12):
            for day in range(5):
                period = day * 12 + shift
                for index_room in index_rooms_sorted:
                    if self.constraint.Feasible(index_class, index_room, period):
                        return period, index_room
        return None

    def Try(self, index_class, index_rooms_sorted):
        for index_class_arranged in self.timetable:
            if index_class_arranged != index_class:
                for i in range(len(self.timetable[index_class_arranged])):
                    period, index_room = self.timetable[index_class_arranged][i]
                    self.constraint.Set_State(index_class_arranged, index_room, period, True)

                    if self.constraint.Feasible(index_class, index_room, period):
                        self.constraint.Set_State(index_class, index_room, period, False)
                    else:
                        self.constraint.Set_State(index_class_arranged, index_room, period, False)
                        continue

                    chooseForOldClass = self.Select(index_class_arranged, index_rooms_sorted)
                    if chooseForOldClass != None:
                        self.timetable[index_class_arranged][i] = chooseForOldClass
                        new_period, new_index_room = chooseForOldClass
                        self.constraint.Set_State(index_class_arranged, new_index_room, new_period, False)
                        self.constraint.Set_State(index_class, index_room, period, True)
                        return True
                    else:
                        self.constraint.Set_State(index_class, index_room, period, True)
                        self.constraint.Set_State(index_class_arranged, index_room, period, False)

        return False

    def ShowSolution(self):
        timetable = self.timetable
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


    def BackTrack(self, index_classes_sorted, index_rooms_sorted, last_index_period = -1, i = 0):
        if i >= len(self.info_classes):
            return True
        
        index_class = index_classes_sorted[i]
        info_class = self.info_classes[index_class]

        for shift in range(12):
            for day in range(5):
                period = day * 12 + shift
                index_period = shift * 5 + day
                if index_period > last_index_period:
                    for index_room in index_rooms_sorted:
                        if self.constraint.Feasible(index_class, index_room, period):

                            self.constraint.Set_State(index_class, index_room, period, False)
                            self.timetable[index_class].append((period, index_room))
                            info_class[0] -= 1

                            if info_class[0] == 0:
                                arrange_next = self.BackTrack(index_classes_sorted, index_rooms_sorted, -1 ,i + 1)
                            else:
                                arrange_next = self.BackTrack(index_classes_sorted, index_rooms_sorted, index_period, i)

                            if arrange_next == True:
                                return True
                            elif arrange_next == "TIME EXCEED LIMIT":
                                self.timetable = "FAILURE"
                                return "TIME EXCEED LIMIT"

                            self.AllowTry[i + 1] = True
                            p_pop, ir_pop = self.timetable[index_class].pop()
                            self.constraint.Set_State(index_class, ir_pop, p_pop, True)
                            info_class[0] += 1
        
        if time.time() - self.start > self.time_limit:
            return "TIME EXCEED LIMIT"

        if self.Try(index_class, index_rooms_sorted) and self.AllowTry[i]:
            self.AllowTry[i] = False
            return self.BackTrack(index_classes_sorted, index_rooms_sorted, i)
        
        return False

if __name__ == "__main__":
    filename = "random_data.txt"
    gen(filename, 15, 2, hard=True)
    start = time.time()
    timetable = BackTrackingAlgorithm(filename, time_limit=100)
    end = time.time()
    timetable.ShowSolution()
    # PrintSolution(timetable)
    print("Time:", end - start)