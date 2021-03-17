import math
import re


class Parser:

    def __init__(self):
        self.operations_dict = {
            # operator: (priority, function)
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '*': (2, lambda x, y: x * y),
            '%': (2, lambda x, y: x % y),
            '/': (2, lambda x, y: x / y),
            '//': (2, lambda x, y: x // y),
            '**': (3, lambda x, y: x ** y),

        }

    def parse(self, input_expr):
        tokenized = self._tokenize(input_expr)
        postfix = self._convert_to_postfix(tokenized)
        result = self._evaluate(postfix)

        return result

    def _evaluate(self, postfix_expr):
        """
        Gets postfix notation expression and evaluates it.
        """
        stack = []
        for char in postfix_expr:
            if char.lstrip('-').isdigit() or '.' in char:
                stack.append(char)

            if char in self.operations_dict:
                try:
                    y = float(stack.pop())
                    x = float(stack.pop())

                except ValueError:
                    raise SyntaxError("Invalid operand types")
                except IndexError:
                    raise SyntaxError("Invalid operand number")

                stack.append(self.operations_dict[char][1](x, y))

        if len(stack) != 1:
            raise SyntaxError('Invalid input')

        return stack.pop()

    def _convert_to_postfix(self, input_expr):
        """
        Transforming expression in infix notation to postfix 
        notation. I.e., (2/2+1)*3 => 2 2 / 1 + 3 *
        """
        stack = []
        postfix_expr = []
        for char in input_expr:
            if char.lstrip('-').isdigit() or '.' in char:
                postfix_expr.append(char)

            elif char == '(':
                stack.append(char)

            elif char == ')':
                while stack and stack[-1] != '(':
                    postfix_expr.append(stack.pop())
                # popping '('
                stack.pop()

            elif char in self.operations_dict:
                if not stack or stack[-1] == '(':
                    stack.append(char)

                else:
                    while stack and stack[-1] != '(':
                        if (stack[-1] in self.operations_dict and
                                self.operations_dict[char][0] > self.operations_dict[stack[-1]][0]):
                            break

                        postfix_expr.append(stack.pop())
                    stack.append(char)

        while stack:
            postfix_expr.append(stack.pop())

        return postfix_expr

    def _tokenize(self, input_string):
        """
        Tokenizer, which recognises:
        - ints and floats
        - brackets: ()
        - operators: +, -, *, /, %
        """
        input_string = re.sub(r'pi', str(math.pi), input_string)
        input_string = re.sub(r'e', str(math.e), input_string)
        tokens = []
        tokenizer = re.compile(r'\s*([()+*/%-]|([0-9]+([.][0-9]*)?|[.][0-9]+))')
        current_pos = 0
        while current_pos < len(input_string):
            match = tokenizer.match(input_string, current_pos)
            if match is None:
                raise SyntaxError('Wrong syntax.')

            tokens.append(match.group(1))
            current_pos = match.end()

        self._validate_brackets(tokens)
        tokens = self._modify_operators(tokens)
        tokens = self._find_neg_nums(tokens)

        return tokens

    def _modify_operators(self, tokens):
        """
        Checks if token list contains '*','*' and '/','/', and if so,
        joins them. I.e., ['2','*','*','2'] => ['2','**','2']
        """
        prev_token = ''
        final_token_list = []
        for token in tokens:
            if token in '*/':
                if len(prev_token) < 3:
                    prev_token += token
                else:
                    raise SyntaxError('Wrong operator usage.')

            elif prev_token:
                final_token_list.append(prev_token)
                prev_token = ''
                final_token_list.append(token)

            else:
                final_token_list.append(token)

        return final_token_list

    def _find_neg_nums(self, tokens):
        """
        Checks if '-' is at the beginning of the expression and followed by a number or
        if it is after a bracket '(' before a number. If so, appends '-' to the number.
        """
        prev_token = ''
        final_token_list = []
        for token in tokens:
            # ['-', '5', '+', '5']
            if token == '-' and not prev_token:
                prev_token = token

            elif token == '(':
                if prev_token:
                    final_token_list.append(prev_token)

                prev_token = token
            # ['5', '-', '(', '-', '5', ')']
            elif token == '-' and prev_token == '(':
                final_token_list.append(prev_token)
                prev_token = token

            elif prev_token == '-':
                prev_token += token

            else:
                if prev_token:
                    final_token_list.append(prev_token)

                prev_token = token

        if prev_token:
            final_token_list.append(prev_token)

        return final_token_list

    def _validate_brackets(self, tokens):
        """
        Validates input for equal number of brackets and their order.
        """
        brackets_stack = []
        for token in tokens:
            if token == '(':
                brackets_stack.append(token)

            elif token == ')':
                try:
                    brackets_stack.pop()
                except IndexError:
                    raise SyntaxError('Wrong brackets number.')

        if brackets_stack:
            raise SyntaxError('Wrong brackets number.')


def main():
    p = Parser()
    while True:
        try:
            input_expr = input('Enter your expression (ctrl+c to exit): ')
            print(p.parse(input_expr))
        except SyntaxError:
            print("Invalid input. Try again: ")
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
