"""
PostfixChecker.py - Kiem tra bieu thuc hau to voi hien thi tung buoc
Su dung PDA de nhan dien bieu thuc hau to (postfix)
"""

from PDA import PDA


class PostfixChecker:
    def __init__(self):
        self.pda = PDA()

    def check_postfix(self, expr):
        """
        Kiem tra bieu thuc hau to va hien thi tung buoc:
        1. Parse/tokenize
        2. Mo phong PDA nhan dien hau to
        """
        print(f"\n{'=' * 70}")
        print(f"KIEM TRA BIEU THUC HAU TO (POSTFIX)")
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

        # Buoc 2: Mo phong PDA
        print(f"{'-' * 70}")
        print("BUOC 2: MO PHONG PDA NHAN DIEN")
        print(f"{'-' * 70}")
        result = self._simulate_pda(expr)
        print()

        # Ket qua cuoi cung
        print(f"{'-' * 70}")
        print("KET QUA CUOI CUNG")
        print(f"{'-' * 70}")
        if result:
            print(f"[OK] CHAP NHAN: Bieu thuc hau to '{expr}' hop le")
        else:
            print(f"[NO] TU CHOI: Bieu thuc hau to '{expr}' khong hop le")
        print(f"{'=' * 70}\n")
        return result

    def _simulate_pda(self, postfix_expr):
        """
        Mo phong PDA voi hien thi chi tiet tung buoc:
        - Operands: PUSH len stack
        - Binary operators: POP 2, PUSH 1 result
        - Unary operators/functions: POP 1, PUSH 1 result
        - Cuoi: stack phai chi co 1 phan tu (result)
        """
        tokens = self.pda._tokenize(postfix_expr)
        stack = []
        operators = set(['+', '-', '*', '/', '^', '**'])
        functions = set(['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'abs'])
        unary_ops = set(['u-'])

        print(f"PDA STACK SIMULATION:")
        print(f"{'BUOC':<8} {'TOKEN':<10} {'LOAI':<15} {'HANH DONG':<25} {'STACK':<35} {'TRANG THAI':<15}")
        print(f"{'-' * 108}")

        step = 0
        for tok in tokens:
            if tok == ' ' or tok == '':
                continue

            step += 1
            tok_type = ""
            action = ""
            status = "OK"

            if tok in operators:
                # Binary operator
                tok_type = "Toan tu nhi phan"
                if len(stack) < 2:
                    print(f"{step:<8} {tok:<10} {tok_type:<15} {'LOI: thieu toan hang':<25} {str(stack):<35} {'LOI':<15}")
                    print(f"\n[ERROR] Toan tu '{tok}' can 2 toan hang nhung stack chi co {len(stack)} phan tu")
                    return False
                operand2 = stack.pop()
                operand1 = stack.pop()
                action = f"POP({operand1}, {operand2}) -> PUSH(R)"
                stack.append('R')
                status = "OK"

            elif tok in unary_ops:
                # Unary operator
                tok_type = "Toan tu don"
                if len(stack) < 1:
                    print(f"{step:<8} {tok:<10} {tok_type:<15} {'LOI: thieu toan hang':<25} {str(stack):<35} {'LOI':<15}")
                    print(f"\n[ERROR] Toan tu don '{tok}' can 1 toan hang nhung stack trong")
                    return False
                operand = stack.pop()
                action = f"POP({operand}) -> PUSH(R)"
                stack.append('R')
                status = "OK"

            elif tok in functions:
                # Function
                tok_type = "Ham"
                if len(stack) < 1:
                    print(f"{step:<8} {tok:<10} {tok_type:<15} {'LOI: thieu toan hang':<25} {str(stack):<35} {'LOI':<15}")
                    print(f"\n[ERROR] Ham '{tok}' can 1 toan hang nhung stack trong")
                    return False
                operand = stack.pop()
                action = f"POP({operand}) -> PUSH(R)"
                stack.append('R')
                status = "OK"

            else:
                # Operand (number or variable)
                tok_type = "Toan hang"
                action = f"PUSH({tok})"
                stack.append(f"{tok}")
                status = "OK"

            print(f"{step:<8} {tok:<10} {tok_type:<15} {action:<25} {str(stack):<35} {status:<15}")

        print(f"{'-' * 108}")

        # Kiem tra stack cuoi cung
        print(f"\nKiem tra trang thai cuoi cung:")
        print(f"  - Stack: {stack}")
        print(f"  - So phan tu: {len(stack)}")

        if len(stack) == 1:
            print(f"[OK] Stack co dung 1 phan tu (ket qua) -> CHAP NHAN")
            return True
        else:
            print(f"[NO] Stack co {len(stack)} phan tu (phai la 1) -> TU CHOI")
            return False


def main():
    checker = PostfixChecker()

    print("\n" + "=" * 70)
    print("CONG CU KIEM TRA BIEU THUC HAU TO (POSTFIX CHECKER)")
    print("=" * 70)
    print("Nhap bieu thuc hau to de kiem tra tinh hop le")
    print("Ho tro: +, -, *, /, ^ (luy thua), ham (sin, cos, tan, log, ln, sqrt, abs)")
    print("Cac toan hang phai duoc tach bang khoang trang")
    print("Vi du: a b + c *, 3 4 + 2 *, x sin, -3 4 +")
    print("Nhap 'exit' de thoat")
    print("=" * 70 + "\n")

    while True:
        expr = input("Nhap bieu thuc hau to: ").strip()

        if expr.lower() == 'exit':
            print("Thoat chuong trinh.")
            break

        if not expr:
            print("Bieu thuc trong. Vui long nhap lai.\n")
            continue

        checker.check_postfix(expr)


if __name__ == '__main__':
    main()
