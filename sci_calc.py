import math
import customtkinter as ctk
import re
from engine.ast_eval import ASTEvaluator
from engine.memory import Memory
from ui.history import HistoryPanel
from ui.graph import GraphPanel




# =============================
# 1. SAFE MATH ENGINE
# =============================
class MathEngine:
    def __init__(self):
        self.angle_mode = "RAD"  # RAD or DEG
        self.evaluator = ASTEvaluator(self)
        self.memory = Memory()

    def _deg(self, x):
        return math.radians(x) if self.angle_mode == "DEG" else x

    def allowed_names(self):
        return {
            # constants
            "pi": math.pi,
            "e": math.e,

            # trig
            "sin": lambda x: math.sin(self._deg(x)),
            "cos": lambda x: math.cos(self._deg(x)),
            "tan": lambda x: math.tan(self._deg(x)),
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,

            # math
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "pow": pow,
            "abs": abs,
            "round": round,
        }

    def evaluate(self, expr: str, **variables):
        expr = expr.replace("^", "**")

        if not re.match(r"^[0-9+\-*/().,^ a-zA-Z]*$", expr):
            raise ValueError("Invalid characters")

        return self.evaluator.evaluate(expr, **variables)


# =============================
# 2. UI COMPONENTS
# =============================
class Display(ctk.CTkEntry):
    def __init__(self, master):
        super().__init__(
            master,
            justify="right",
            font=("Consolas", 26)
        )

    def set(self, text):
        self.delete(0, "end")
        self.insert(0, text)


class CalcButton(ctk.CTkButton):
    def __init__(self, master, text, command, color=None):
        super().__init__(master, text=text, command=command)
        if color:
            self.configure(fg_color=color)


# =============================
# 3. MAIN APPLICATION
# =============================
class SciCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.engine = MathEngine()

        self.title("Scientific Calculator")
        self.geometry("420x580")
        ctk.set_appearance_mode("dark")

        self._build_ui()
        self.history = HistoryPanel(self)
        self.history.grid(row=0, column=6, rowspan=10, sticky="nsew")
        
        self.graph = None
        
        self._bind_keys()

    # -------------------------
    # UI
    # -------------------------
    def _build_ui(self):
        self.display = Display(self)
        self.display.grid(row=0, column=0, columnspan=6, padx=12, pady=10, sticky="nsew")

        self.status = ctk.CTkLabel(self, text="RAD", anchor="e")
        self.status.grid(row=1, column=0, columnspan=6, padx=12, pady=(0, 8), sticky="nsew")

        for r in range(2, 10):
            self.grid_rowconfigure(r, weight=1)
        for c in range(6):
            self.grid_columnconfigure(c, weight=1)
            self.grid_columnconfigure(6, weight=1)

        self._buttons()

    def _buttons(self):
        def b(t, cmd, r, c, cs=1, col=None):
            CalcButton(self, t, cmd, col).grid(
                row=r, column=c, columnspan=cs, padx=6, pady=6, sticky="nsew"
            )

        # Controls
        b("C", self.clear, 2, 0, col="#b84040")
        b("DEL", self.backspace, 2, 1)
        b("DEG/RAD", self.toggle_angle, 2, 2, cs=2)
        b("=", self.evaluate, 2, 4, cs=2, col="#2f8f2f")
        b("GRAPH", self.graph_plot, 9, 4, cs=2, col="#4444aa")

        # Scientific
        funcs = ["sin", "cos", "tan", "log", "log10", "sqrt"]
        for i, f in enumerate(funcs):
            b(f, lambda x=f: self.insert(f"{x}("), 3, i)

        b("(", lambda: self.insert("("), 4, 0)
        b(")", lambda: self.insert(")"), 4, 1)
        b("^", lambda: self.insert("^"), 4, 2)
        b("π", lambda: self.insert("pi"), 4, 3)
        b("e", lambda: self.insert("e"), 4, 4)
        b("±", self.toggle_sign, 4, 5)

        digits = [
            ("7",5,0),("8",5,1),("9",5,2),
            ("4",6,0),("5",6,1),("6",6,2),
            ("1",7,0),("2",7,1),("3",7,2),
            ("0",8,0),(".",8,1)
        ]
        for t,r,c in digits:
            b(t, lambda x=t: self.insert(x), r, c)

        ops = [("/",5,3),("*",6,3),("-",7,3),("+",8,3)]
        for t,r,c in ops:
            b(t, lambda x=t: self.insert(x), r, c)

        b("M+", self.mem_add, 9, 0)
        b("M-", self.mem_sub, 9, 1)
        b("MR", self.mem_recall, 9, 2)
        b("MC", self.mem_clear, 9, 3)
    # -------------------------
    # Actions
    # -------------------------
    def graph_plot(self):
        expr = self.display.get().strip()

        if "x" not in expr:
            self.status.configure(text="Graph needs x")
            return

        if self.graph:
            self.graph.destroy()

        self.graph = GraphPanel(self, self.engine)
        self.graph.grid(row=10, column=0, columnspan=7, sticky="nsew", pady=5)
        self.graph.plot(expr)


    def insert(self, text):
        self.display.insert("end", text)

    def clear(self):
        self.display.set("")
        self.status.configure(text=self.engine.angle_mode)

    def backspace(self):
        v = self.display.get()
        self.display.set(v[:-1])

    def toggle_sign(self):
        expr = self.display.get()
        match = re.search(r"(\d+\.?\d*)$", expr)
        if not match:
            return
        start, end = match.span()
        num = match.group()
        self.display.set(expr[:start] + f"(-{num})")

    def toggle_angle(self):
        self.engine.angle_mode = "DEG" if self.engine.angle_mode == "RAD" else "RAD"
        self.status.configure(text=self.engine.angle_mode)

    def evaluate(self):
        expr = self.display.get()
        try:
            result = self.engine.evaluate(expr)
            self.display.set(str(result))
            self.history.add(expr, result)
        except Exception:
            self.status.configure(text="Use GRAPH for x")
            
    def mem_add(self):
        try:
            self.engine.memory.add(float(self.display.get()))
        except ValueError:
            pass

    def mem_sub(self):
        try:
            self.engine.memory.subtract(float(self.display.get()))
        except ValueError:
            pass

    def mem_recall(self):
        self.display.set(str(self.engine.memory.recall()))

    def mem_clear(self):
        self.engine.memory.clear()


    # -------------------------
    # Keyboard
    # -------------------------
    def _bind_keys(self):
        self.bind("<Return>", lambda e: self.evaluate())
        self.bind("<BackSpace>", lambda e: self.backspace())
        self.bind("<Escape>", lambda e: self.clear())
        for ch in "0123456789+-*/().^":
            self.bind(ch, lambda e: self.insert(e.char))


if __name__ == "__main__":
    SciCalculator().mainloop()
