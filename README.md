# Compyler
FLC

## Diagramas 
![Diagramaaaa](h7diagrams.png)

## EBNF
Program = { "sub", "main", "(",")", (statement, "/n" | lambda ), "end", "sub"};<br>
Statement = (lambda | "Identifier, "=", Expression | "Print", Expression | "While", RelExpression, Statements, "Wend") | "If", RelExpression, "Then", Statements, (lambda | ("else", Statement)) | "dim", Identifier, "as", Type;<br>
RelExpression = Expression, (lambda | (“>” | “<” | “=” ), Expression);<br>
Type = "Integer" | "Boolean"; <br>
Expression = Term, { (“+” | “-”), Term };<br>
Term =  Factor, { (“*” | “/”), Factor };<br>
Factor = (“+” | “-”), Factor | INT | “(”, Expression, “)” | Identifier | ;<br>
