import customtkinter as ctk

class HistoryPanel(ctk.CTkTextbox):
    def add(self, expr, result):
        self.insert("end", f"{expr} = {result}\n")
