# Compyler
FLC

## Diagramas 
![Diagramaaaa](h7diagrams.png)

## EBNF
Statements = { Statement, "/n" };<br>
Statement = (lambda | "Identifier, "=", Expression | "Print", Expression | "While", RelExpression, Statements, "Wend") | "If", RelExpression, "Then", Statements, (lambda | ("else", Statement));<br>
RelExpression = Expression, (“>” | “<” | “=”), Expression;<br>
Expression = Term, { (“+” | “-”), Term };<br>
Term =  Factor, { (“*” | “/”), Factor };<br>
Factor = (“+” | “-”), Factor | INT | “(”, Expression, “)” | Identifier;<br>
