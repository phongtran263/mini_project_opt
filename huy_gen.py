import random as rd
def gen(filename,N,M, hard = True):
  with open(filename,'w') as f:
  #T:num of teachers
    f.write(f'{N} {M}\n')
    number_teacher = rd.randint(2, N//4)
    teacher = [_ for _ in range(1, 1 + number_teacher)]
    num_in_room = [] # The capacity of this room
    room_largest = 0
    teacher_class = {}
    info_class = [[0,0,float("inf")] for _ in range(N)]
    state_room = [[True]*M for _ in range(60)]
    state_teacher = [[True]*(1+number_teacher) for _ in range(60)]
    for _ in range(M):
      num_in_room.append(rd.randint(30,60))
      # if num_in_room[-1] > num_in_room[room_largest]:
      #   room_largest = len(num_in_room) - 1
      if num_in_room[-1] > num_in_room[room_largest]:
        room_largest = len(num_in_room) - 1

    for _ in range(M):
      if _ != room_largest and num_in_room[room_largest] == num_in_room[_]:
        num_in_room[_] -= 10

    dict_class_teacher = {}
    for _ in range(N):
      if len(teacher) != 0:
        index_teacher = teacher.pop()
        teacher_class[index_teacher] = [_]
        # info_class[_][1] = index_teacher
        # dict_class_teacher[_] = index_teacher
      else:
        index_teacher = rd.randint(1, len(teacher_class))
        teacher_class[index_teacher].append(_)
      info_class[_][1] = index_teacher
      dict_class_teacher[_] = index_teacher

    ############## CHOOSE CLASS IN SMALL ROOM ##############
    class_large_room = rd.sample([i for i in range(N)], N//3)
    large_room = []

    for _ in range(60):
      if rd.choice([True, False]):
        continue
      choose = rd.choice(class_large_room)
      large_room.append(choose)
      state_room[_][room_largest] = False
      state_teacher[_][dict_class_teacher[choose]] = False
      info_class[choose][2] = num_in_room[room_largest] - rd.randint(0,5)
      info_class[choose][0] += 1

    no_lesson = [_ for _ in range(N) if info_class[_][0] == 0]

    for i in range(60):
      teacher_c = [_ for _ in range(1, 1 + number_teacher)]
      room_c = [_ for _ in range(M)]
      while True:
        loop = True
        while True:
          if len(teacher_c) == 0:
            loop = False
            break
          c_choice = rd.choice(teacher_c)
          teacher_c.remove(c_choice)
          if state_teacher[i][c_choice]:
            state_teacher[i][c_choice] = False
            teacher_satisfy = c_choice
            break
        if not loop:
          break

        while True:
          if len(room_c) == 0:
            loop = False
            break
          c_choice = rd.choice(room_c)
          room_c.remove(c_choice)
          if state_room[i][c_choice]:
            state_room[i][c_choice] = False
            room_satisfy = c_choice
            break
        if not loop:
          break
        choice1 = list(set.intersection(set(teacher_class[teacher_satisfy]), set(no_lesson)))
        if len(choice1) == 0:
          choose_from = list(set(teacher_class[teacher_satisfy]) - set(large_room))
          if len(choose_from) == 0:
            class_teach = rd.choice(teacher_class[teacher_satisfy])
          else:
            class_teach = rd.choice(choose_from)
        else:
          class_teach = rd.choice(choice1)
          no_lesson.remove(class_teach)
        info_class[class_teach][0] += 1
        if num_in_room[room_satisfy] < info_class[class_teach][2]:
          info_class[class_teach][2] = num_in_room[room_satisfy] - rd.randint(1,5)
    if not hard:
      list_info = [_[:] for _ in info_class]
      list_info.sort(reverse=True, key=lambda x: x[0])
      for i in range(len(list_info)//3 + 1):
        list_info[i][0] = list_info[i][0] // 2 + 1
      info_class = list_info
    for t, g, s in info_class:
      f.write(f'{t} {g} {s}\n')
    for _ in num_in_room:
      f.write(f'{_} ')

if __name__ == "__main__":
  gen("test.txt", 15, 4)




