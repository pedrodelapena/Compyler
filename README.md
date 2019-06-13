# Compyler
FLC

## Diagramas 
![Diagramaaaa](diagramfin.png)

## EBNF
Program = { FuncDec | SubDec }; <br>
<br>
FuncDec = { "Function", Identifier, "(", (Identifier, "as", Type | lambda ), ")", "as", Type, "\n", (Statement, "\n" | lambda ) "end", "function"};<br>
<br>
SubDec = { "Sub", Identifier, "(", (Identifier, "as", Type | lambda ), ")", "\n", (Statement, "\n" | lambda ) "end", "sub"};<br>
Statement = (lambda | Identifier, "=", RelExpression | "Print", RelExpression | "While", RelExpression, Statements, "Wend") | "If", RelExpression, "Then", Statements, (lambda | ("else", Statement)) "end", "if" | "dim", Identifier, "as", Type | "Call", Identifier, "(", (lambda  | RelExpression,  | ",");<br>
<br>
RelExpression = Expression, (lambda | (“>” | “<” | “=” ), Expression);<br>
<br>
Expression = Term, { ( lambda | “+” | “-”), Term };<br>
<br>
Term =  Factor, { (“*” | “/” | "and"), Factor };<br>
<br>
Factor = (“+” | “-”), Factor | INT | “(”, (RelExpression  | ","  | lambda), “)” | "Identifier" | "Input" ;<br>
<br>
Type = "Integer" | "Boolean"; <br>
