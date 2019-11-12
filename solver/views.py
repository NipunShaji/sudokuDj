import sys

from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    return render(request, 'solver/home.html')

# sudoku solving algorithm and functions
puzzle = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]
         ]

flags = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]
       ]


def getrow(x):
    if x<9 or x>89:
        print("Non accepted value in getrow : {}".format(x))
        sys.exit()
    rowlist = []
    row = x//9
    for i in range(1,10):
        rowlist.append(puzzle[row][i])
    return rowlist


def getcol(y):
    if y<9 or y>89:
        print("Non accepted value in getcol : {}".format(y))
        sys.exit()
    col = []
    colspot = (y%9)+1
    for i in puzzle:
        col.append(i[colspot])
    return col


def getgroup(x):

    if x<9 or x>89:
        print("Non accepted value in getgroup : {}".format(x))
        sys.exit()

    group = []
    row = x//9
    if row<4:
        row = 1
    elif row<7:
        row = 4
    elif row < 10:
        row = 7

    col = x%9+1
    if col<4:
        col = 1
    elif col<7:
        col = 4
    elif col<10:
        col = 7

    for i in range(row,row+3):
        for j in range(col,col+3):
            group.append(puzzle[i][j])

    return group


def value(x,z=-1):
    if x<9 or x>89:
        print("Non accepted value in value : {}".format(x))
        sys.exit()
    row = x//9
    col = x%9 + 1
    if z == -1:
        return puzzle[row][col]
    else:
        puzzle[row][col] = z
        return True


def flag(x,z=-1):
    if x<9 or x>89:
        print("Non accepted value in flag : {}".format(x))
        sys.exit()
    row = x//9
    col = x%9 + 1
    if z != -1:
        flags[row][col] = 1
        return True
    return flags[row][col]

def getbestvalue(x,i):
    best = False
    row = getrow(x)
    col = getcol(x)
    grp = getgroup(x)
    for m in range(i+1,10):
        if m not in row and m not in col and m not in grp:
            return m
    return best


def initialize(data):
    j = 9
    for i in data:
        value(j,i)
        if i > 0:
            flag(j,1)
        j+=1
    return True

def startsolving():
    i = 9
    while i < 90:
        if not flag(i):
            best = getbestvalue(i,value(i))
            if best:
                value(i,best)
            else:
                while True:
                    i -= 1
                    if not flag(i):
                        best = getbestvalue(i,value(i))
                        if best:
                            value(i,best)
                            break
                        else:
                            value(i,0)
        i += 1
    return True




def solve(request):
    context = {}
    if request.method == 'GET':
        dataall = request.GET.getlist('data')
        data = dataall[0].split(',')
        for i in range(len(data)):
            data[i] = int(data[i])
            print(data[i])
        print(type(data[1]))
        if initialize(data):
            print(flags)
            startsolving()
            print('solving')
            print(puzzle)
            output = []
            for i in range(9,90):
                output.append(value(i))
            context['status'] = 'Success...'
            context['data'] = output
        else:
            context['status'] = 'Error!!!'
        return JsonResponse(context)
    else:
        return JsonResponse({'status':'Error!!!'})
