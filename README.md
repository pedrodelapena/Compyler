# Compyler
FLC

## Diagramas 
![Diagramaaaa](diagramas.png)

## EBNF
Statements = { Statement, "/n" };
Statement = (lambda | "Identifier, "=", Expression | "Print", Expression | "While", RelExpression, Statements, "Wend") | "If", RelExpression, "Then", Statements, (lambda | ("else", Statement));
RelExpression = Expression, (“>” | “<” | “=”), Expression;
Expression = Term, { (“+” | “-”), Term };
Term =  Factor, { (“*” | “/”), Factor };
Factor = (“+” | “-”), Factor | INT | “(”, Expression, “)” | Identifier;
