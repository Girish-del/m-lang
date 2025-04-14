from mlangVisitor import mlangVisitor

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class mlangInterpreter(mlangVisitor):
    def __init__(self):
        self.memory = {}        # Global memory
        self.functions = {}     # Function table

    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    def visitVariableDecl(self, ctx):
        var = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[var] = value

    def visitAssignStmt(self, ctx):
        var = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[var] = value

    def visitPrintStmt(self, ctx):
        value = self.visit(ctx.expr())
        print(value)

    def visitFunctionDecl(self, ctx):
        name = ctx.ID().getText()
        params = [p.getText() for p in ctx.paramList().ID()] if ctx.paramList() else []
        block = ctx.block()
        self.functions[name] = (params, block)

    def visitReturnStmt(self, ctx):
        value = self.visit(ctx.expr())
        raise ReturnValue(value)

    def visitExprStmt(self, ctx):
        self.visit(ctx.expr())

    def visitBlock(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    def visitExpr(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.BOOL():
            return ctx.BOOL().getText() == 'truth'
        elif ctx.ID():
            return self.memory.get(ctx.ID().getText(), 0)
        elif ctx.functionCall():
            return self.visitFunctionCall(ctx.functionCall())
        elif ctx.op:
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            if ctx.op.text == '+': return left + right
            if ctx.op.text == '-': return left - right
            if ctx.op.text == '*': return left * right
            if ctx.op.text == '/': return left // right
            if ctx.op.text == 'andAlso': return left and right
            if ctx.op.text == 'orElse': return left or right
            if ctx.op.text == 'smallerThan': return left < right
            if ctx.op.text == 'greaterThan': return left > right
            if ctx.op.text == 'greaterThanOrEqualTo': return left >= right
            if ctx.op.text == 'lessThanOrEqualTo': return left <= right
        elif ctx.getChild(0).getText() == 'not':
            return not self.visit(ctx.expr(0))
        return 0

    def visitFunctionCall(self, ctx):
        name = ctx.ID().getText()
        args = [self.visit(arg) for arg in ctx.argList().expr()] if ctx.argList() else []
        if name not in self.functions:
            raise Exception(f"Function '{name}' not defined.")
        params, block = self.functions[name]

        if len(params) != len(args):
            raise Exception(f"Function '{name}' expects {len(params)} args but got {len(args)}.")

        # Save global memory, create local function scope
        saved_memory = self.memory.copy()
        self.memory = dict(zip(params, args))

        try:
            self.visit(block)
        except ReturnValue as r:
            self.memory = saved_memory
            return r.value

        self.memory = saved_memory
        return 0
