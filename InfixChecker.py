"""
InfixChecker.py - Kiem tra bieu thuc trung to voi hien thi tung buoc
Chuyen tu trung to (infix) sang hau to (postfix) va kiem tra tinh hop le
"""

from PDA import PDA


class InfixChecker:
    def __init__(self):
        self.pda = PDA()
        self.steps = []

    def check_infix(self, expr):
        """
        Kiem tra bieu thuc trung to va hien thi tung buoc:
        1. Parse/tokenize
        2. Chuyen sang hau to (shunting-yard)
        3. Kiem tra hau to bang PDA
        """
        print(f"\n{'=' * 70}")
        print(f"KIEM TRA BIEU THUC TRUNG TO (INFIX)")
        print(f"{'=' * 70}")
        print(f"Bieu thuc nhap vao: {expr}")
        print()

        # Buoc 1: Tokenize
        print(f"{'-' * 70}")
        print("BUOC 1: PHAN TICH TOKENS")
        print(f"{'-' * 70}")
        tokens = self.pda._tokenize(expr)
        print(f"Tokens: {tokens}")
        print()

        # Buoc 2: Chuyen sang hau to bang shunting-yard
        print(f"{'-' * 70}")
        print("BUOC 2: CHUYEN SANG HAU TO (SHUNTING-YARD)")
        print(f"{'-' * 70}")
        try:
            postfix = self.pda.infix_to_postfix(expr)
            print(f"Hau to: {postfix}")
            print(f"[OK] Chuyen doi thanh cong")
            print()

            # Buoc 3: Kiem tra hau to bang PDA
            print(f"{'-' * 70}")
            print("BUOC 3: KIEM TRA HAU TO BANG PDA")
            print(f"{'-' * 70}")
            self._show_postfix_recognition(postfix)
            print()

            # Ket qua cuoi cung
            print(f"{'-' * 70}")
            print("KET QUA CUOI CUNG")
            print(f"{'-' * 70}")
            result = self.pda.recognize_infix(expr)
            if result:
                print(f"[OK] CHAP NHAN: Bieu thuc trung to '{expr}' hop le")
            else:
                print(f"[NO] TU CHOI: Bieu thuc trung to '{expr}' khong hop le")
            print(f"{'=' * 70}\n")
            return result

        except ValueError as e:
            print(f"[ERROR] {e}")
            print(f"{'=' * 70}\n")
            return False

    def _show_postfix_recognition(self, postfix_expr):
        """Hien thi qua trinh nhan dien hau to bang PDA"""
        tokens = self.pda._tokenize(postfix_expr)
        stack = []
        operators = set(['+', '-', '*', '/', '^', '**'])
        functions = set(['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'abs'])
        unary_ops = set(['u-'])

        print(f"{'BUOC':<8} {'TOKEN':<10} {'HANH DONG':<20} {'STACK':<30} {'TRANG THAI':<15}")
        print(f"{'-' * 83}")

        step = 0
        for tok in tokens:
            if tok == ' ' or tok == '':
                continue

            step += 1
            action = ""
            status = ""

            if tok in operators:
                if len(stack) < 2:
                    print(f"{step:<8} {tok:<10} {'POP 2, PUSH 1':<20} {str(stack):<30} {'LOI':<15}")
                    print(f"[ERROR] Khong du toan hang cho toan tu '{tok}'")
                    return False
                stack.pop()
                stack.pop()
                stack.append('R')
                action = "POP 2, PUSH 1"
                status = "OK"
            elif tok in unary_ops or tok in functions:
                if len(stack) < 1:
                    print(f"{step:<8} {tok:<10} {'POP 1, PUSH 1':<20} {str(stack):<30} {'LOI':<15}")
                    print(f"[ERROR] Khong du toan hang cho ham/toan tu don '{tok}'")
                    return False
                stack.pop()
                stack.append('R')
                action = "POP 1, PUSH 1"
                status = "OK"
            else:
                # Operand
                stack.append('O')
                action = "PUSH OPERAND"
                status = "OK"

            print(f"{step:<8} {tok:<10} {action:<20} {str(stack):<30} {status:<15}")

        print(f"{'-' * 83}")

        # Kiem tra trang thai cuoi
        if len(stack) == 1:
            print(f"[OK] Stack cuoi cung co 1 phan tu: CHAP NHAN")
            return True
        else:
            print(f"[NO] Stack cuoi cung co {len(stack)} phan tu: TU CHOI")
            return False


def main():
    checker = InfixChecker()

    print("\n" + "=" * 70)
    print("CONG CU KIEM TRA BIEU THUC TRUNG TO (INFIX CHECKER)")
    print("=" * 70)
    print("Nhap bieu thuc trung to de kiem tra tinh hop le")
    print("Ho tro: +, -, *, /, ^ (luy thua), ham (sin, cos, tan, log, ln, sqrt, abs)")
    print("Vi du: (a+b)*c, -3+4, sin(x)/2, (x+y)^2")
    print("Nhap 'exit' de thoat")
    print("=" * 70 + "\n")

    while True:
        expr = input("Nhap bieu thuc trung to: ").strip()

        if expr.lower() == 'exit':
            print("Thoat chuong trinh.")
            break

        if not expr:
            print("Bieu thuc trong. Vui long nhap lai.\n")
            continue

        checker.check_infix(expr)


if __name__ == '__main__':
    main()

