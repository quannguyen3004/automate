from FileHandler import FileHandler
import argparse
import sys


class PDA:
    """Pushdown-related utilities focused on infix/postfix expressions.

    Features:
    - `infix_to_postfix(expr)` : convert infix expression to postfix (shunting-yard)
    - `recognize_postfix(expr)` : simulate a simple PDA that accepts well-formed postfix arithmetic expressions
    - `recognize_infix(expr)` : convert infix to postfix then recognize
    - `compute_legacy(inputString, parsedLines)` : preserved basic legacy behavior for automata files
    """

    def __init__(self):
        pass

    def _tokenize(self, expr):
        tokens = []
        i = 0
        n = len(expr)
        # define two-char operators we want to recognize
        two_char_ops = {'**', '==', '!=', '<=', '>=', '&&', '||'}
        operator_chars = set('+-*/^%=<>!&|')
        while i < n:
            c = expr[i]
            if c.isspace():
                i += 1
                continue

            # number (possibly with decimal point)
            if c.isdigit() or (c == '.' and i+1 < n and expr[i+1].isdigit()):
                j = i
                has_dot = False
                while j < n and (expr[j].isdigit() or (expr[j] == '.' and not has_dot)):
                    if expr[j] == '.':
                        has_dot = True
                    j += 1
                tokens.append(expr[i:j])
                i = j
                continue

            # negative number as part of token: if '-' and next is digit and previous token is operator or '(' or start
            if c == '-' and i+1 < n and (expr[i+1].isdigit() or expr[i+1] == '.'):
                prev = tokens[-1] if tokens else None
                if prev is None or prev in ('+', '-', '*', '/', '^', '%', '(', ',', '**') or prev in operator_chars:
                    # parse negative number
                    j = i+1
                    has_dot = False
                    while j < n and (expr[j].isdigit() or (expr[j] == '.' and not has_dot)):
                        if expr[j] == '.':
                            has_dot = True
                        j += 1
                    tokens.append(expr[i:j])
                    i = j
                    continue

            # identifier (function or variable)
            if c.isalpha():
                j = i
                while j < n and expr[j].isalpha():
                    j += 1
                tokens.append(expr[i:j])
                i = j
                continue

            # two-char operator
            if i+1 < n and expr[i:i+2] in two_char_ops:
                tokens.append(expr[i:i+2])
                i += 2
                continue

            # single-char operator or parenthesis
            if c in operator_chars or c in '(),':
                tokens.append(c)
                i += 1
                continue

            # unknown char: treat as single token
            tokens.append(c)
            i += 1

        return tokens

    def infix_to_postfix(self, expr):
        """Convert infix expression to postfix using the shunting-yard algorithm.

        Supports multi-character operands (letters/digits/period), operators + - * / ^ and parentheses.
        Returns a space-separated postfix string.
        """
        output = []
        stack = []
        prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 4, '**': 4, 'u-': 5}
        right_assoc = {'^', '**', 'u-'}

        tokens = self._tokenize(expr)
        prev_token = None
        functions = set(['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'abs'])

        for tok in tokens:
            # functions should be recognized before generic alphanumeric operands
            if tok in functions:
                stack.append(tok)
                prev_token = 'func'
                continue

            # operand: number or variable (may contain digits or letters)
            if (tok.replace('.', '', 1).lstrip('-').isdigit()) or tok.isalnum():
                output.append(tok)
                prev_token = 'operand'
                continue

            if tok == '(':
                stack.append(tok)
                prev_token = '('
                continue

            if tok == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                else:
                    raise ValueError('Mismatched parentheses')
                # if function on top, pop it to output
                if stack and stack[-1] in functions:
                    output.append(stack.pop())
                prev_token = 'operand'
                continue

            # detect unary minus
            if tok == '-' and (prev_token is None or prev_token in ('operator', '(')):
                tok = 'u-'

            # operator
            while stack and stack[-1] != '(' and (
                (prec.get(stack[-1], 0) > prec.get(tok, 0)) or
                (prec.get(stack[-1], 0) == prec.get(tok, 0) and tok not in right_assoc)
            ):
                output.append(stack.pop())
            stack.append(tok)
            prev_token = 'operator'

        while stack:
            top = stack.pop()
            if top in ('(', ')'):
                raise ValueError('Mismatched parentheses')
            output.append(top)

        return ' '.join(output)

    def recognize_postfix(self, expr):
        """Simulate a PDA that recognizes well-formed postfix expressions.

        Rules: operands push a marker; operators require two markers to pop, and then push one marker (the result).
        At the end the stack should contain exactly one marker.
        Returns True if accepted, False otherwise.
        """
        tokens = self._tokenize(expr)
        stack = []
        # define binary operators and unary/function operators
        bin_ops = set(['+', '-', '*', '/', '^', '**'])
        unary_ops = set(['u-'])
        functions = set(['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'abs'])

        for tok in tokens:
            if tok == ' ' or tok == '':
                continue
            if tok in bin_ops:
                if len(stack) < 2:
                    return False
                stack.pop()
                stack.pop()
                stack.append('R')
            elif tok in unary_ops or tok in functions:
                if len(stack) < 1:
                    return False
                stack.pop()
                stack.append('R')
            else:
                # operand (variable, number)
                stack.append('O')

        return len(stack) == 1

    def recognize_infix(self, expr):
        try:
            postfix = self.infix_to_postfix(expr)
        except ValueError:
            return False
        return self.recognize_postfix(postfix)

    def compute_legacy(self, inputString, parsedLines):
        """Preserve a clearer version of the original compute using parsed automata description.

        Note: This implements the original, limited production model in the repo. Kept for compatibility.
        """
        # simple wrapper that attempts to simulate legacy behavior
        inputString = inputString + 'e'
        stack = []
        initStackSymbol = parsedLines['initial_stack']
        stack.append(initStackSymbol)
        finalStates = parsedLines['final_states']
        currentState = parsedLines['initial_state']
        productions = parsedLines['productions']

        print('State\tInput\tStack\tMove')
        print('{}\t {}\t {}\t ({}, {})'.format(currentState, '_', initStackSymbol, initStackSymbol, stack))

        for char in inputString:
            currentStackSymbol = stack[-1] if stack else None
            moved = False
            for production in productions:
                if ((production[0] == currentState) and (production[1] == char) and (production[2] == currentStackSymbol)):
                    currentState = production[3]
                    action = production[4]
                    if action == 'e':
                        if len(stack) > 1:
                            stack.pop()
                    else:
                        # push symbols from action (if action contains symbols like 'AA' push individually)
                        for s in action:
                            stack.append(s)
                    moved = True
                    break
            prevStackSymbol = currentStackSymbol
            currentStackSymbol = stack[-1] if stack else None
            print('{}\t {}\t {}\t ({}, {})'.format(currentState, char, prevStackSymbol, currentStackSymbol, stack))

        if currentState in finalStates:
            print('String accepted by PDA.')
            return True
        else:
            print('String rejected by PDA.')
            return False


def main(argv=None):
    pda = PDA()
    fh = FileHandler()

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='PDA utilities: convert/check infix/postfix or run legacy automata file')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--convert', action='store_true', help='Convert infix to postfix and print result')
    group.add_argument('--postfix', type=str, help='Check given postfix expression')
    group.add_argument('--infix', type=str, help='Check given infix expression (convert then check)')
    group.add_argument('--legacy', action='store_true', help='Run legacy automata file compute')

    parser.add_argument('--file', type=str, help='Path to automata file (for --legacy)')
    parser.add_argument('--input', type=str, help='Input string for automata (for --legacy)')

    args = parser.parse_args(argv)

    if args.convert:
        expr = args.infix
        if not expr:
            print('Error: --convert requires --infix "EXPR"')
            return 2
        try:
            postfix = pda.infix_to_postfix(expr)
            print('Postfix:', postfix)
            return 0
        except ValueError as e:
            print('Error converting infix to postfix:', e)
            return 1

    if args.postfix is not None:
        expr = args.postfix
        ok = pda.recognize_postfix(expr)
        if ok:
            print('CHẤP NHẬN: Biểu thức hậu tố hợp lệ.')
            return 0
        else:
            print('TỪ CHỐI: Biểu thức hậu tố không hợp lệ.')
            return 1

    if args.infix is not None:
        expr = args.infix
        try:
            postfix = pda.infix_to_postfix(expr)
            print('Converted postfix:', postfix)
        except ValueError as e:
            print('Error: mismatched parentheses or invalid infix:', e)
            return 1
        ok = pda.recognize_postfix(postfix)
        if ok:
            print('CHẤP NHẬN: Biểu thức trung tố hợp lệ (qua chuyển sang hậu tố).')
            return 0
        else:
            print('TỪ CHỐI: Biểu thức trung tố không hợp lệ (qua chuyển sang hậu tố).')
            return 1

    if args.legacy:
        if not args.file:
            print('Error: --legacy requires --file PATH and --input STRING')
            return 2
        lines = fh.readFile(args.file)
        parsedLines = fh.parseFile(lines)
        inputString = args.input or input('Enter input String: ')
        pda.compute_legacy(inputString, parsedLines)
        return 0

    return 0


if __name__ == '__main__':
    main()
