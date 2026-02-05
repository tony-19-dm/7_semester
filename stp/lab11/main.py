import subprocess
import sys


def main():
    """Запуск всех компонентов системы"""
    
    print("ЗАПУСК ПОЛНОГО ЭКСПЕРИМЕНТА ПО МОДЕЛИРОВАНИЮ")
    print("="*70)
    
    print("\n1. Запуск основного моделирования...")
    print("-"*70)
    subprocess.run([sys.executable, "model_programming.py"])
    
    print("\n\n2. Запуск тестов...")
    print("-"*70)
    subprocess.run([sys.executable, "test_model.py"])
    
    print("\n\n3. Пример анализа программ...")
    print("-"*70)
    subprocess.run([sys.executable, "metrics_calculator.py"])


if __name__ == "__main__":
    main()