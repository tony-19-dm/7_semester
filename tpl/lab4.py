import sys

transitions_rpn = {
    ('q0', 'n', 'Z'): ('q0', 'none', 'n'),
    ('q0', 'n', '+'): ('q0', 'none', 'n'),
    ('q0', 'n', '-'): ('q0', 'none', 'n'),
    ('q0', 'n', '*'): ('q0', 'none', 'n'),
    ('q0', 'n', '/'): ('q0', 'none', 'n'),
    ('q0', 'n', '('): ('q0', 'none', 'n'),

    ('q0', '(', 'Z'): ('q0', 'push:(', ''),
    ('q0', '(', '+'): ('q0', 'push:(', ''),
    ('q0', '(', '-'): ('q0', 'push:(', ''),
    ('q0', '(', '*'): ('q0', 'push:(', ''),
    ('q0', '(', '/'): ('q0', 'push:(', ''),
    ('q0', '(', '('): ('q0', 'push:(', ''),

    ('q0', ')', '('): ('q0', 'pop', ''),
    ('q0', ')', '+'): ('q_(', 'pop', '+'),
    ('q0', ')', '-'): ('q_(', 'pop', '-'),
    ('q0', ')', '*'): ('q_(', 'pop', '*'),
    ('q0', ')', '/'): ('q_(', 'pop', '/'),

    ('q_(', '', '('): ('q0', 'pop', ''),
    ('q_(', '', '+'): ('q_(', 'pop', '+'),
    ('q_(', '', '-'): ('q_(', 'pop', '-'),
    ('q_(', '', '*'): ('q_(', 'pop', '*'),
    ('q_(', '', '/'): ('q_(', 'pop', '/'),

    ('q0', '+', 'Z'): ('q0', 'push:+', ''),
    ('q0', '+', '('): ('q0', 'push:+', ''),

    ('q0', '+', '+'): ('q_+', 'pop', '+'),
    ('q0', '+', '-'): ('q_+', 'pop', '-'),
    ('q0', '+', '*'): ('q_+', 'pop', '*'),
    ('q0', '+', '/'): ('q_+', 'pop', '/'),

    ('q_+', '', 'Z'): ('q0', 'push:+', ''),
    ('q_+', '', '('): ('q0', 'push:+', ''),
    ('q_+', '', '+'): ('q_+', 'pop', '+'),
    ('q_+', '', '-'): ('q_+', 'pop', '-'),
    ('q_+', '', '*'): ('q_+', 'pop', '*'),
    ('q_+', '', '/'): ('q_+', 'pop', '/'),

    ('q0', '-', 'Z'): ('q0', 'push:-', ''),
    ('q0', '-', '('): ('q0', 'push:-', ''),

    ('q0', '-', '+'): ('q_-', 'pop', '+'),
    ('q0', '-', '-'): ('q_-', 'pop', '-'),
    ('q0', '-', '*'): ('q_-', 'pop', '*'),
    ('q0', '-', '/'): ('q_-', 'pop', '/'),

    ('q_-', '', 'Z'): ('q0', 'push:-', ''),
    ('q_-', '', '('): ('q0', 'push:-', ''),
    ('q_-', '', '+'): ('q_-', 'pop', '+'),
    ('q_-', '', '-'): ('q_-', 'pop', '-'),
    ('q_-', '', '*'): ('q_-', 'pop', '*'),
    ('q_-', '', '/'): ('q_-', 'pop', '/'),

    ('q0', '*', 'Z'): ('q0', 'push:*', ''),
    ('q0', '*', '('): ('q0', 'push:*', ''),
    ('q0', '*', '+'): ('q0', 'push:*', ''),
    ('q0', '*', '-'): ('q0', 'push:*', ''),

    ('q0', '*', '*'): ('q_*', 'pop', '*'),
    ('q0', '*', '/'): ('q_*', 'pop', '/'),

    ('q_*', '', 'Z'): ('q0', 'push:*', ''),
    ('q_*', '', '('): ('q0', 'push:*', ''),
    ('q_*', '', '+'): ('q0', 'push:*', ''),
    ('q_*', '', '-'): ('q0', 'push:*', ''),
    ('q_*', '', '*'): ('q_*', 'pop', '*'),
    ('q_*', '', '/'): ('q_*', 'pop', '/'),

    ('q0', '/', 'Z'): ('q0', 'push:/', ''),
    ('q0', '/', '('): ('q0', 'push:/', ''),
    ('q0', '/', '+'): ('q0', 'push:/', ''),
    ('q0', '/', '-'): ('q0', 'push:/', ''),

    ('q0', '/', '*'): ('q_/', 'pop', '*'),
    ('q0', '/', '/'): ('q_/', 'pop', '/'),

    ('q_/', '', 'Z'): ('q0', 'push:/', ''),
    ('q_/', '', '('): ('q0', 'push:/', ''),
    ('q_/', '', '+'): ('q0', 'push:/', ''),
    ('q_/', '', '-'): ('q0', 'push:/', ''),
    ('q_/', '', '*'): ('q_/', 'pop', '*'),
    ('q_/', '', '/'): ('q_/', 'pop', '/'),

    ('q0', '', 'Z'): ('qf', 'pop', ''),
    ('q0', '', '+'): ('q_pop_all', 'pop', '+'),
    ('q0', '', '-'): ('q_pop_all', 'pop', '-'),
    ('q0', '', '*'): ('q_pop_all', 'pop', '*'),
    ('q0', '', '/'): ('q_pop_all', 'pop', '/'),

    ('q_pop_all', '', 'Z'): ('qf', 'pop', ''),
    ('q_pop_all', '', '+'): ('q_pop_all', 'pop', '+'),
    ('q_pop_all', '', '-'): ('q_pop_all', 'pop', '-'),
    ('q_pop_all', '', '*'): ('q_pop_all', 'pop', '*'),
    ('q_pop_all', '', '/'): ('q_pop_all', 'pop', '/'),
}

# transitions_lang = {
#     ('q0', 'a', 'Z'): ('q1', 'none', ''),
#     ('q1', 'a', 'Z'): ('q2', 'none', ''),
#     ('q2', 'a', 'Z'): ('q3', 'none', ''),
#     ('q3', 'a', 'Z'): ('q2', 'none', ''),
#     ('q2', 'b', 'Z'): ('q4', 'push:b', ''),
#     ('q4', 'b', 'b'): ('q6', 'pop', ''),
#     ('q6', 'b', 'Z'): ('q4', 'push:b', ''),
#     ('q4', 'c', 'b'): ('q5', 'pop', ''),
#     ('q5', 'c', 'b'): ('q5', 'pop', ''),
#     ('q5', 'c', 'Z'): ('q5', 'none', ''),
#     ('q4', '', 'b'): ('qf', 'none', ''),
#     ('q5', '', 'Z'): ('qf', 'none', ''),
#     ('q0', '', 'Z'): ('reject', 'none', ''),
#     ('q0', 'b', 'Z'): ('reject', 'none', ''),
#     ('q0', 'c', 'Z'): ('reject', 'none', ''),
#     ('q1', 'b', 'Z'): ('reject', 'none', ''),
#     ('q1', 'c', 'Z'): ('reject', 'none', ''),
#     ('q2', 'c', 'Z'): ('reject', 'none', ''),
#     ('q4', 'c', 'Z'): ('reject', 'none', ''),
#     ('q4', '', 'Z'): ('reject', 'none', ''),
#     ('q5', '', 'b'): ('reject', 'none', ''),
#     ('q6', '', 'Z'): ('reject', 'none', ''),
# }

transitions_lang = {
    ('q0', 'a', 'Z'): ('q0', 'push:a', 'a'),
    ('q0', 'a', 'a'): ('q1', 'push:a', 'aa'),
    ('q1', 'a', 'a'): ('q0', 'push:a', 'aa'),
    ('q0', 'b', 'a'): ('q0', 'ε', 'bb'),
    ('q0', 'b', 'Z'): ('q2', 'none', 'b'),
    ('q2', '', 'Z'): ('qf', 'none', ''),
    ('q2', 'c', 'Z'): ('q2', 'none', 'c'),
}

def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isspace():
            i += 1
            continue
        if expression[i].isdigit():
            num = ''
            while i < len(expression) and expression[i].isdigit():
                num += expression[i]
                i += 1
            tokens.append(('n', num))
            continue
        if expression[i] in '+-*/()':
            tokens.append((expression[i], expression[i]))
            i += 1
            continue
        raise ValueError(f"Недопустимый символ: {expression[i]}")
    return tokens

def convert_to_rpn_verbose(expression):
    print(f"\nВходное выражение: {expression}")
    print("=" * 70)
    print(f"{'Шаг':<4} {'Вход':<18} {'Состояние':<10} {'Стек':<25} {'Выход (ОПЗ)':<30}")
    print("-" * 70)

    try:
        tokens = tokenize(expression)
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    state = 'q0'
    stack = ['Z']
    output = []
    i = 0
    step = 0

    while True:
        step += 1

        if state == 'qf' and (not stack or stack == ['Z'] or len(stack) == 0):
            stack_str = ' '.join(stack) if stack else 'Пусто'
            output_str = ' '.join(output) if output else '(пусто)'
            print(f"{step:<4} {'ГОТОВО':<18} {state:<10} {stack_str:<25} {output_str:<30}")
            print("-" * 70)
            result = ' '.join(output)
            print(f"Результат в ОПЗ: {result}")
            print(f"Выражение корректно → {result}")
            return

        if i < len(tokens):
            symbol, actual = tokens[i]
            input_str = f"{actual} (тип: {symbol})"
            epsilon = False
        else:
            symbol = ''
            actual = ''
            input_str = "ε (конец)"
            epsilon = True

        top = stack[-1] if stack else None

        key = (state, symbol, top) if top is not None else None
        if key not in transitions_rpn and top is not None:
            key = (state, '', top)
            if key in transitions_rpn:
                symbol = ''
                actual = ''
                input_str = "ε-переход"
                epsilon = True

        if key not in transitions_rpn or top is None and key is not None:
            print(f"\nОшибка на шаге {step}:")
            print(f"   Состояние: {state}, Вход: '{symbol}', Вершина стека: {top}")
            print("   Нет подходящего перехода.")
            print("   Вероятно, синтаксическая ошибка во выражении.")
            return

        new_state, action, out = transitions_rpn[key]

        stack_str = ' '.join(stack) if stack else 'Пусто'
        output_str = ' '.join(output) if output else '(пусто)'
        print(f"{step:<4} {input_str:<18} {state:<10} {stack_str:<25} {output_str:<30}")

        if out and out != 'none':
            if out == 'n':
                output.append(actual)
            else:
                output.append(out)

        if action.startswith('push:'):
            stack.append(action[5:])
        elif action == 'pop':
            if stack:
                stack.pop()
            else:
                print("Критическая ошибка: pop из пустого стека")
                return
        elif action != 'none':
            print(f"Неизвестное действие: {action}")
            return

        state = new_state
        if not epsilon:
            i += 1

        if step > 1000:
            print("Слишком много шагов — прерывание")
            return

def check_language(s):
    print(f"\nПроверяем строку: → {s} ←")
    print("=" * 80)
    print(f"{'Шаг':<4} {'Ввод':<8} {'Сост.':<10} {'Стек':<25} {'Действие'}")
    print("-" * 80)

    state = 'q0'
    stack = ['Z']
    i = 0
    step = 0

    while True:
        step += 1

        if state == 'qf' and (not stack or stack == ['Z'] or len(stack) == 0):
            print(f"{step:<4} {'ГОТОВО':<8} {'qf':<10} {'Пусто':<25} {'ПРИНЯТО!'}")
            print("-" * 80)
            return

        sym = s[i] if i < len(s) else ''
        inp = sym if i < len(s) else 'ε'

        top = stack[-1]

        key = (state, sym, top)
        if key not in transitions_lang:
            if i >= len(s):
                key = (state, '', top)
                if key in transitions_lang:
                    inp = 'ε-переход'
                else:
                    key = None
            else:
                key = None

        if key not in transitions_lang:
            print(f"{step:<4} {inp:<8} {state:<10} {' '.join(stack):<25} {'НЕТ ПЕРЕХОДА → ОТКЛОНЕНО'}")
            print("-" * 80)
            return

        new_state, action, _ = transitions_lang[key]
        comment = "ничего"
        if action.startswith('push:'):
            comment = f"push {action[5:]}"
        elif action == 'ε':
            comment = "ε"

        print(f"{step:<4} {inp:<8} {state}→{new_state:<5} {' '.join(stack):<25} {comment}")

        if action.startswith('push:'):
            stack.append(action[5:])
        elif action == 'ε':
            if stack and stack[-1] != 'Z':
                stack.pop()

        state = new_state
        if sym:
            i += 1

def main():
    print("1 → Обратная полька")
    print("2 → Проверка языка")
    print("0 → Выход")

    while True:
        choice = input("\nВыберите режим (0-2): ").strip()

        if choice == '1':
            print("РЕЖИМ 1: Обратная полька")
            while True:
                expr = input("\nВыражение или 'назад': ").strip()
                if expr.lower() in ['назад', 'back', '0']:
                    break
                if expr:
                    convert_to_rpn_verbose(expr)

        elif choice == '2':
            print("РЕЖИМ 2: Проверка языка")
            while True:
                s = input("\nСтрока или 'назад': ").strip()
                if s.lower() in ['назад', 'back', '0']:
                    break
                if not all(c in 'abc' for c in s):
                    print("Только a, b, c!")
                    continue
                check_language(s)

        elif choice == '0':
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()

