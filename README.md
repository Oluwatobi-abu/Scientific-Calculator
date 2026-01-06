# 🧮 Scientific Calculator (Python) — v1.0.0

A full-featured **Scientific Calculator with Graph Plotting**, built using **Python**, **CustomTkinter**, and **Matplotlib**.

Supports numerical evaluation, trigonometric functions, graphing expressions involving `x`, and exporting graphs as images.

---

## ✨ Features

- 🧠 Safe AST-based math engine (no `eval`)
- 📐 DEG / RAD angle mode
- 🧮 Scientific functions:
  - `sin`, `cos`, `tan`
  - `log`, `log10`, `sqrt`
- 📊 Graph plotting with:
  - Domain control (`x min`, `x max`)
  - Zoom & pan toolbar
  - Save graph as PNG
  - Clear / close graph panel
- 🕘 Calculation history
- 💾 Memory functions (M+, M-, MR, MC)
- ⌨️ Keyboard support
- 🪟 Windows `.exe` build available (no Python required)

---

## 🚀 How to Run (Source Code)

### 1️ Clone the repository
```bash
git clone https://github.com/your-username/scientific-calculator.git
cd scientific-calculator

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the application
python sci_calc.py

🧱 Build Windows Executable (.exe)
pyinstaller --onefile --windowed sci_calc.py


The executable will appear in:

dist/sci_calc.exe


Users can run it without installing Python.

📂 Project Structure
Scientific Calculator/
│
├─ engine/
│   ├─ ast_eval.py
│   ├─ evaluator.py
│   └─ memory.py
│
├─ ui/
│   ├─ graph.py
│   └─ history.py
│
├─ sci_calc.py
├─ README.md
└─ requirements.txt

🛡️ Security

No use of eval

Only whitelisted math functions allowed

Safe AST parsing

📜 License

MIT License — free to use, modify, and distribute.

👤 Author

Abubakar Oluwatobi
Built with ❤️ using Python


---

## 3️⃣ requirements.txt (correct & minimal)

Yes — this is **perfect**:

```txt
customtkinter
matplotlib
numpy


Nothing else needed 👍