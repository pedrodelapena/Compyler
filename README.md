# Compyler
FLC

## Diagramas 
![Diagramaaaa](diagramsz.png)

## EBNF
Program = { "sub", "main", "(",")", (statement, "/n" | lambda ), "end", "sub"};<br>
Statement = (lambda | "Identifier, "=", RelExpression | "Print", RelExpression | "While", RelExpression, Statements, "Wend") | "If", RelExpression, "Then", Statements, (lambda | ("else", Statement)) "end", "if" | "dim", Identifier, "as", Type;<br>
RelExpression = Expression, (lambda | (“>” | “<” | “=” ), Expression);<br>
Expression = Term, { (“+” | “-”), Term };<br>
Term =  Factor, { (“*” | “/” | "and"), Factor };<br>
Factor = (“+” | “-”), Factor | INT | “(”, RelExpression, “)” | "Identifier" | "Input" ;<br>
Type = "Integer" | "Boolean"; <br>
