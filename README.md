# PushDown Automata — Infix & Postfix Tools

Tài liệu này hướng dẫn cách cài đặt môi trường, chạy chương trình và kết quả test hiện tại.

## Yêu cầu
- Python 3.10+ (project được phát triển và chạy với Python 3.14 trong môi trường ảo `.venv`).

## Cài đặt môi trường (Windows PowerShell)
1. Tạo môi trường ảo:

```powershell
cd D:\PushDown-Automata-Implementation-master
python -m venv .venv
```

2. Kích hoạt môi trường (PowerShell):

```powershell
. .venv\Scripts\Activate.ps1
# Nếu không dùng PowerShell, dùng: .venv\Scripts\activate (bash/cmd tương ứng)
```

3. Cài pytest (nếu cần để chạy test):

```powershell
pip install -U pip
pip install pytest
```

## Cách chạy chương trình

- Kiểm tra biểu thức trung tố (convert -> kiểm tra):

```powershell
python PDA.py --infix "(a + b) * c"
```

- Kiểm tra biểu thức hậu tố:

```powershell
python PDA.py --postfix "a b + c *"
```

- Chỉ chuyển đổi trung tố -> hậu tố (infix -> postfix):

```powershell
python PDA.py --convert --infix "(a+b)^2"
```

- Chạy chế độ legacy (dùng file mô tả PDA):

```powershell
python PDA.py --legacy --file automaton.txt --input "abba"
```

- Chạy trình kiểm tra tương tác trung tố / hậu tố:

```powershell
python InfixChecker.py
python PostfixChecker.py
```

(các script sẽ yêu cầu nhập biểu thức và in ra các bước tokenization, chuyển đổi và mô phỏng PDA từng bước)

## Test

Chạy toàn bộ bộ test bằng pytest:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

Kết quả test hiện tại (máy phát triển):

```
13 passed in 0.03s
```

## Mô tả tệp chính
- `PDA.py`: lõi xử lý — tokenizer, chuyển trung tố->hậu tố (shunting-yard), bộ mô phỏng PDA cho hậu tố, wrapper nhận dạng trung tố, và CLI.
- `InfixChecker.py`: trình kiểm tra trung tố tương tác, in chi tiết các bước.
- `PostfixChecker.py`: trình kiểm tra hậu tố tương tác, in chi tiết các bước.
- `FileHandler.py`: bộ hàm đọc/parse mô tả PDA (dành cho chế độ legacy).
- `tests/test_pda.py`: bộ unit tests dùng pytest.

## Ghi chú
- Nếu bạn muốn tôi đẩy các thay đổi này lên GitHub, hãy cho biết và tôi sẽ commit + push cho bạn.

## Ví dụ kiểm tra biểu thức trung tố (mẫu đầu ra)

Dưới đây là ví dụ đầu ra của `InfixChecker.py` khi kiểm tra biểu thức trung tố:

```
Nhap bieu thuc trung to de kiem tra tinh hop le
Ho tro: +, -, *, /, ^ (luy thua), ham (sin, cos, tan, log, ln, sqrt, abs)
Vi du: (a+b)*c, -3+4, sin(x)/2, (x+y)^2
Nhap 'exit' de thoat
======================================================================

Nhap bieu thuc trung to: ( a + b ) + c + (d +g) ^21

======================================================================
KIEM TRA BIEU THUC TRUNG TO (INFIX)
======================================================================
Bieu thuc nhap vao: ( a + b ) + c + (d +g) ^21

----------------------------------------------------------------------
BUOC 1: PHAN TICH TOKENS
----------------------------------------------------------------------
Tokens: ['(', 'a', '+', 'b', ')', '+', 'c', '+', '(', 'd', '+', 'g', ')', '^', '21']

----------------------------------------------------------------------
BUOC 2: CHUYEN SANG HAU TO (SHUNTING-YARD)
----------------------------------------------------------------------
Hau to: a b + c + d g + 21 ^ +
[OK] Chuyen doi thanh cong

----------------------------------------------------------------------
BUOC 3: KIEM TRA HAU TO BANG PDA
----------------------------------------------------------------------
BUOC     TOKEN      HANH DONG            STACK                          TRANG THAI
-----------------------------------------------------------------------------------
1        a          PUSH OPERAND         ['O']                          OK
2        b          PUSH OPERAND         ['O', 'O']                     OK
3        +          POP 2, PUSH 1        ['R']                          OK
4        c          PUSH OPERAND         ['R', 'O']                     OK
5        +          POP 2, PUSH 1        ['R']                          OK
6        d          PUSH OPERAND         ['R', 'O']                     OK
7        g          PUSH OPERAND         ['R', 'O', 'O']                OK
8        +          POP 2, PUSH 1        ['R', 'R']                     OK
9        21         PUSH OPERAND         ['R', 'R', 'O']                OK
10       ^          POP 2, PUSH 1        ['R', 'R']                     OK
11       +          POP 2, PUSH 1        ['R']                          OK
-----------------------------------------------------------------------------------
[OK] Stack cuoi cung co 1 phan tu: CHAP NHAN

----------------------------------------------------------------------
KET QUA CUOI CUNG
----------------------------------------------------------------------
[OK] CHAP NHAN: Bieu thuc trung to '( a + b ) + c + (d +g) ^21' hop le
======================================================================
```

Bạn có muốn tôi chèn thêm ví dụ đầu ra cho `PostfixChecker.py` không? (ví dụ tương tự sẽ được thêm vào nếu bạn đồng ý.)

## Ví dụ kiểm tra biểu thức hậu tố (mẫu đầu ra)

Dưới đây là ví dụ đầu ra của `PostfixChecker.py` khi kiểm tra biểu thức hậu tố tương đương với ví dụ trên (hậu tố: `a b + c + d g + 21 ^ +`):

```
KIEM TRA BIEU THUC HAU TO (POSTFIX)
======================================================================
Bieu thuc nhap vao (hậu tố): a b + c + d g + 21 ^ +

----------------------------------------------------------------------
BUOC 1: PHAN TICH TOKENS
----------------------------------------------------------------------
Tokens: ['a', 'b', '+', 'c', '+', 'd', 'g', '+', '21', '^', '+']

----------------------------------------------------------------------
BUOC 2: KIEM TRA HAU TO BANG PDA
----------------------------------------------------------------------
BUOC     TOKEN      HANH DONG            STACK                          TRANG THAI
-----------------------------------------------------------------------------------
1        a          PUSH OPERAND         ['O']                          OK
2        b          PUSH OPERAND         ['O', 'O']                     OK
3        +          POP 2, PUSH 1        ['R']                          OK
4        c          PUSH OPERAND         ['R', 'O']                     OK
5        +          POP 2, PUSH 1        ['R']                          OK
6        d          PUSH OPERAND         ['R', 'O']                     OK
7        g          PUSH OPERAND         ['R', 'O', 'O']                OK
8        +          POP 2, PUSH 1        ['R', 'R']                     OK
9        21         PUSH OPERAND         ['R', 'R', 'O']                OK
10       ^          POP 2, PUSH 1        ['R', 'R']                     OK
11       +          POP 2, PUSH 1        ['R']                          OK
-----------------------------------------------------------------------------------
[OK] Stack cuoi cung co 1 phan tu: CHAP NHAN

----------------------------------------------------------------------
KET QUA CUOI CUNG
----------------------------------------------------------------------
[OK] CHAP NHAN: Bieu thuc hau to 'a b + c + d g + 21 ^ +' hop le
======================================================================
```
