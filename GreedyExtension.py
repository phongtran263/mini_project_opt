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

class Greedy(object):

    def __init__(self, filename):
        self.info_classes, self.rooms = self.input(filename)
        self.constraint = Constraint(self.info_classes, self.rooms)
        self.timetable = {}
        self.Solve()

    def input(self, filename):
        with open(filename) as f:
            [N, M] = [int(x) for x in f.readline().split()]
            info_classes = [[int(x) for x in f.readline().split()] for _ in range(N)]
            rooms = [int(x) for x in f.readline().split()]
        return info_classes, rooms


    def Solve(self):

        # Sort base on room's capacity (increasing) 
        index_rooms_sorted = sorted([i for i in range(len(self.rooms))], key = lambda x : self.rooms[x])
        
        # Sort teacher base on the number of shift he/she have to teach (decreasing)
        G = {}
        for i in range(len(self.info_classes)):
            teacher = self.info_classes[i][1]
            G[teacher] = G.get(teacher, [])
            G[teacher].append(i)

        teachers = sorted(list(G.keys()), key = lambda x: -sum([self.info_classes[i][0] for i in G[x]]))

        for teacher in teachers:
            index_classes_sorted = sorted(G[teacher], key = lambda x: -self.info_classes[x][2])
            for index_class in index_classes_sorted:
                self.timetable[index_class] = []
                for _ in range(self.info_classes[index_class][0]): # If we loop this way, we will sure that each class has enough shift.
                    select = self.Select(index_class, index_rooms_sorted)
                    if select == None:
                        if not self.Try(index_class, index_rooms_sorted):
                            self.timetable = "FAILURE"
                            return 
                    else:
                        period, index_room = select
                        self.constraint.Set_State(index_class, index_room, period, False)
                        self.timetable[index_class].append(select)


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
            for period, index_room in self.timetable[index_class_arranged]:

                self.constraint.Set_State(index_class_arranged, index_room, period, True)

                if self.constraint.Feasible(index_class, index_room, period):
                    self.constraint.Set_State(index_class, index_room, period, False)
                else:
                    self.constraint.Set_State(index_class_arranged, index_room, period, False)
                    continue

                chooseForOldClass = self.Select(index_class_arranged, index_rooms_sorted)
                if chooseForOldClass != None:
                    self.timetable[index_class_arranged].remove((period, index_room))
                    self.timetable[index_class_arranged].append(chooseForOldClass)
                    self.timetable[index_class].append((period, index_room))
                    new_period, new_index_room = chooseForOldClass
                    self.constraint.Set_State(index_class_arranged, new_index_room, new_period, False)
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
        count = [[0]*5 for _ in range(len(classes))]
        for i in classes:
            table_sort = sorted(timetable[i])
            for p, r in table_sort:
                count[i][p//12] += 1
                print(f'Class {i + 1} has lessons at period {shift(p+1)} on {convert[p//12]} at room {r + 1}')
            print()
        
        f = 0
        for i in count:
            f += (max(i) - min(i))
        print("F* =", f)

if __name__ == "__main__":
    filename = "random_data.txt"
    gen(filename, 15, 2, hard=True)
    start = time.time()
    solution = Greedy(filename)
    end = time.time()
    solution.ShowSolution()
    print("Time:", end - start)