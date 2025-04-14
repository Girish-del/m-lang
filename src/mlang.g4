grammar mlang;

program: statement* EOF;

statement
    : variableDecl
    | assignStmt
    | printStmt
    | functionDecl
    | returnStmt
    | exprStmt
    ;

variableDecl: 'cast' ID 'is' expr ';';
assignStmt: ID 'is' expr ';';
printStmt: 'say' expr ';';

functionDecl: 'scene' ID ('with' paramList)? 'action' block 'cut';
paramList: ID (',' ID)*;
returnStmt: 'wrap' expr ';';

exprStmt: expr ';';

block: '{' statement* '}';

expr
    : expr op=('*'|'/') expr
    | expr op=('+'|'-') expr
    | expr op=('andAlso'|'orElse') expr
    | expr op=('smallerThan'|'greaterThan'|'greaterThanOrEqualTo'|'lessThanOrEqualTo') expr
    | 'not' expr
    | functionCall
    | BOOL
    | INT
    | ID
    ;

functionCall: 'call' ID ('with' argList)?;
argList: expr (',' expr)*;

BOOL: 'truth' | 'lie';
ID: [a-zA-Z_][a-zA-Z0-9_]*;
INT: [0-9]+;
WS: [ \t\r\n]+ -> skip;
COMMENT: 'note:' ~[\r\n]* -> skip;
