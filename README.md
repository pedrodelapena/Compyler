# Compyler
FLC

## Diagramas 
![Diagramaaaa](diagrams.png)

## EBNF
Program = { FuncDec | SubDec }; <br>
FuncDec = { "Function", Identifier, "(", (Identifier, "as", Type | lambda ), ")", "as", Type, "\n", (Statement, "\n" | lambda ) "end", "function"};<br>
SubDec = { "Sub", Identifier, "(", (Identifier, "as", Type | lambda ), ")", "\n", (Statement, "\n" | lambda ) "end", "sub"};<br>
Statement = (lambda | Identifier, "=", RelExpression | "Print", RelExpression | "While", RelExpression, Statements, "Wend") | "If", RelExpression, "Then", Statements, (lambda | ("else", Statement)) "end", "if" | "dim", Identifier, "as", Type | "Call", Identifier, "(", (lambda  | RelExpression,  | ",");<br>
RelExpression = Expression, (lambda | (“>” | “<” | “=” ), Expression);<br>
Expression = Term, { ( lambda | “+” | “-”), Term };<br>
Term =  Factor, { (“*” | “/” | "and"), Factor };<br>
Factor = (“+” | “-”), Factor | INT | “(”, (RelExpression  | ","  | lambda), “)” | "Identifier" | "Input" ;<br>
Type = "Integer" | "Boolean"; <br>
