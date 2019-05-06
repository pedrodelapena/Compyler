sub main()
dim a as integer
dim b as integer
dim c as boolean
dim d as integer
c = False
a = 1
b = 2
d = 0
print a+b
WHILE d < 5
    IF c THEN
        print c 
        c = False
        d=d+1
    ELSE
        IF c = False THEN
            print c
            c = True
            d=d+1
        END IF
    END IF
WEND
print a+b+d
end sub