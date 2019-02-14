def calc(stg):
    stg = stg.replace(" ", "") 
    c = "" #placeholder
    total = 0 #after 
    ops = 1 #can be eiter 1 or -1
    firstNeg = False #flag

    if stg[0] == "-": #considering there won't be more than one "-" | while
        isneg = True 
        stg = stg[1:]

    for i in range(len(stg)):
        j = stg[i]
        if j.isdigit(): 
            c += j
            if firstNeg:
                ops = -1
                firstNeg = False
        else:
            if j == "+":
                total += int(c) * ops
                ops = 1
                c = ""
            elif j == "-":
                total += int(c) * ops
                ops = -1
                c = "" 
    
    total += int(c) * ops
    print(total)

x = input("Digita ai meu bacana ")
calc(x)
