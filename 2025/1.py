#!/usr/bin/env python3

with open("1.input") as file:
    data = [(item[0], int(item[1:])) for item in [x.strip() for x in file.readlines()]]

    size = 100
    
    pos = 50
    count = 0

    for dir, n in data:
        if dir == 'L':
            pos = ((pos - n) + size) % size
        elif dir == 'R':
            pos = (pos + n) % size
        
        if pos == 0:
            count += 1
        
    print(count)

    count = 0
    pos = 50

    for dir, n in data:
        count += n // size
        n = n % size

        pre = pos

        if n > 0:
            if dir == 'L':
                pos = ((pos - n) + size) % size

                if pos > pre and pre != 0 or pos == 0:
                    count += 1

            elif dir == 'R':
                pos = (pos + n) % size
        
                if pos < pre and pre != 0 or pos == 0:
                    count += 1

    print(count)
