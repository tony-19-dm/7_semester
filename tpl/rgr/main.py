import tkinter as tk
from gui import RegularGrammarApp

def main():
    root = tk.Tk()
    app = RegularGrammarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()