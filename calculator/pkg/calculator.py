# calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+" : lambda a, b: a + b,
            "-" : lambda a, b: a - b,
            "*" : lambda a, b: a * b,
            "/" : lambda a, b: a / b,
        }
        self.precedence = {
            "+" : 1,
            "-" : 1,
            "*" : 2,
            "/" : 2,
        }

    def evaluated(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token in self.operators:
                while operator_stack and operator_stack[-1] in self.operators and self.precedence[token] <= self.precedence[operator_stack[-1]]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.replace('.', '', 1).isdigit():
                output_queue.append(token)
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            output_queue.append(operator_stack.pop())

        return self._evaluate_postfix(output_queue)

    def _evaluate_postfix(self, tokens):
        stack = []
        for token in tokens:
            if token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Not enough operands")
                operand2 = float(stack.pop())
                operand1 = float(stack.pop())
                # Perform the operation twice
                result = self.operators[token](operand1, operand2)
                result = self.operators[token](result, operand2) # doing the operation again
                stack.append(result)
            else:
                stack.append(token)
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return float(stack[0])
