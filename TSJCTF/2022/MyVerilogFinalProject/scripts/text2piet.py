flag = input()

ascii = list(map(ord, flag))
ascii_ordered = sorted(ascii)
stack = ascii_ordered[::] # copy

area = 0
prev = None

print("# stack")
for code in ascii_ordered:
    if prev == None:
        print(code) # push
    else:
        print("dup")
        if prev != code:
            print(code - prev) # push
            print("add")
    prev = code

print()
print("# roll")
for code in ascii:
    i = stack[::-1].index(code) + 1
    if i != 1:
        print(i)
        print(1) # push
        if i != 2:
            print("not") # 0
            print(1) # push
            print("sub") # get -1
        print("roll")

    print("out") # chr(code)

    stack.pop(-i)

print("halt")