import numpy as np
import math

def theoretical_values(eta1, eta2=None):
    """Теоретические значения для одного или двух словарей"""
    if eta2 is None or eta2 == 0:
        # Один словарь
        if eta1 == 0:
            return 0, 0, 0, 0
        M_L = 0.9 * eta1 * math.log2(eta1)
        D_L = (math.pi**2 / 6) * (eta1**2)
    else:
        # Два словаря (формула из первого файла)
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
    # Ограничим длину положительными значениями
    lengths = np.maximum(lengths, 1)
    
    mean_L = np.mean(lengths)
    var_L = np.var(lengths, ddof=1)
    std_L = np.std(lengths, ddof=1)
    delta = std_L / mean_L if mean_L != 0 else 0
    return mean_L, var_L, std_L, delta

def main():
    # Для задания 1: один словарь разных размеров
    etas = [16, 32, 64, 128]
    runs = 50000
    
    print("="*70)
    print("Моделирование для одного словаря")
    print("="*70)
    print("eta |  M(L) теор  |  D(L) теор   |  sqrt(D) теор |  delta теор")
    print("-"*70)
    for eta in etas:
        M, D, Std, delta = theoretical_values(eta)
        print(f"{eta:3d} | {M:10.4f}    | {D:10.4f}    | {Std:10.4f}    | {delta:.4f}")
    
    print("\n" + "="*70)
    print("Моделирование нормальным распределением (runs={})".format(runs))
    print("="*70)
    print("eta |  M(L) модел |  D(L) модел  |  sqrt(D) мод  |  delta мод")
    print("-"*70)
    for eta in etas:
        M_sim, D_sim, Std_sim, delta_sim = simulate_normal(eta, runs=runs)
        print(f"{eta:3d} | {M_sim:10.4f}    | {D_sim:10.4f}    | {Std_sim:10.4f}    | {delta_sim:.4f}")

if __name__ == "__main__":
    main()