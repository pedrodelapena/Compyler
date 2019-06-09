Function Soma(x as integer, y as integer) as integer
	a = x + y 
	print a
	Soma = a
End Function

Sub main()
	Dim a as integer
	Dim b as integer
	a = 3
	b = Soma(a, 4)
	print a
	print b
end sub