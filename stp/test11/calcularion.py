import numpy as np
import math
import tokenize
import io
import keyword

def get_program_lexemes(code):
    """Возвращает список лексем программы (без комментариев и пробелов)"""
    lexemes = []
    try:
        tokens = tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline)
        for tok in tokens:
            if tok.type in (tokenize.NAME, tokenize.OP, tokenize.NUMBER, tokenize.STRING):
                lexemes.append(tok.string)
    except Exception as e:
        print(f"Ошибка токенизации: {e}")
    return lexemes

def analyze_program_text():
    """Анализирует текст текущей программы"""
    with open(__file__, 'r', encoding='utf-8') as f:
        code = f.read()
    
    lexemes = get_program_lexemes(code)
    total_length = len(lexemes)
    unique_lexemes = set(lexemes)
    eta = len(unique_lexemes)
    
    predicted_length = 0.9 * eta * math.log2(eta) if eta > 0 else 0
    
    return eta, total_length, predicted_length

def theoretical_values(eta1, eta2=None):
    """Теоретические значения для одного или двух словарей"""
    if eta2 is None or eta2 == 0:
        if eta1 == 0:
            return 0, 0, 0, 0
        M_L = 0.9 * eta1 * math.log2(eta1)
        D_L = (math.pi**2 / 6) * (eta1**2)
    else:
        M_L = 0.9 * (eta1 * math.log2(eta1) + eta2 * math.log2(eta2))
        D_L = (math.pi**2 / 6) * (eta1**2 + eta2**2)
    
    Std_L = math.sqrt(D_L)
    delta = Std_L / M_L if M_L != 0 else 0
    return M_L, D_L, Std_L, delta

def simulate_normal(eta1, eta2=None, runs=10000):
    """Моделирование L как нормальной случайной величины"""
    if eta2 is None:
        eta2 = 0
    
    M, D, _, _ = theoretical_values(eta1, eta2)
    Std = math.sqrt(D)
    lengths = np.random.normal(M, Std, runs)
    lengths = np.maximum(lengths, 1)
    
    mean_L = np.mean(lengths)
    var_L = np.var(lengths, ddof=1)
    std_L = np.std(lengths, ddof=1)
    delta = std_L / mean_L if mean_L != 0 else 0
    return mean_L, var_L, std_L, delta

def main():
    # Пункты 1-2
    etas = [16, 32, 64, 128]
    runs = 50000
    
    print("="*70)
    print("Пункты 1-2: Моделирование для одного словаря")
    print("="*70)
    print("eta |  M(L) теор  |  D(L) теор   |  sqrt(D) теор |  delta теор")
    print("-"*70)
    theoretical_results = {}
    for eta in etas:
        M, D, Std, delta = theoretical_values(eta)
        theoretical_results[eta] = (M, D, Std, delta)
        print(f"{eta:3d} | {M:10.4f}    | {D:10.4f}    | {Std:10.4f}    | {delta:.4f}")
    
    print("\n" + "="*70)
    print("Моделирование нормальным распределением (runs={})".format(runs))
    print("="*70)
    print("eta |  M(L) модел |  D(L) модел  |  sqrt(D) мод  |  delta мод")
    print("-"*70)
    for eta in etas:
        M_sim, D_sim, Std_sim, delta_sim = simulate_normal(eta, runs=runs)
        print(f"{eta:3d} | {M_sim:10.4f}    | {D_sim:10.4f}    | {Std_sim:10.4f}    | {delta_sim:.4f}")
    
    # Пункт 4
    print("\n"+ "="*70)
    eta_prog, L_real, L_pred = analyze_program_text()
    print(f"Длина словаря программы η = {eta_prog}")
    print(f"Реальная длина программы L = {L_real} лексем")
    print(f"Прогнозируемая длина по формуле M(L) = 0.9η log2 η = {L_pred:.2f}")
    print(f"Отклонение: {abs(L_real - L_pred) / L_real * 100:.2f}%")
    
    # Пункт 5
    print("\n" + "="*70)
    M_prog, D_prog, Std_prog, delta_prog = theoretical_values(eta_prog)
    print(f"Для программы с η={eta_prog}:")
    print(f"M(L)={M_prog:.2f}, D(L)={D_prog:.2f}")
    # Если n² = η (гипотеза), то:
    n_squared = eta_prog
    print(f"n² (предположительно размер словаря) = {n_squared}")
    print(f"Прогнозируемая длина по модели: {M_prog:.2f}")
    print(f"Реальная длина: {L_real}")
    print(f"Сравнение: прогноз/реальность = {M_prog/L_real:.2%}")

if __name__ == "__main__":
    main()