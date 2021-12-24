import random as rd
def Gen(filename,N,M):
    #T:num of teachers
    l = []
    f = open(filename,'w')
    f.write(f'{N} {M}\n')
    for i in range(N):
        t = rd.randint(2,4)
        g = rd.randint(1,4)
        s = rd.randint(20,40)
        l.append(s)
        f.write(f'{t} {g} {s}\n')
    for i in range(M-1):
        c = rd.randint(20,40)
        f.write(f'{c} ')
    c = max(l) + rd.randint(1,10)
    f.write(f'{c}')
if __name__ == '__main__':
    Gen('data_15.txt',40,5)
    

    
    