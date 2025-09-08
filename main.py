import json
import tkinter as tk
from tkinter import messagebox, simpledialog

DATA_FILE = "fabrics.json"

def load_fabrics():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_fabrics(fabrics):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(fabrics, f, ensure_ascii=False, indent=4)

def convert_to_kg(meters, coef):
    return meters / coef

def convert_to_meters(kg, coef):
    return kg * coef

def refresh_listbox():
    listbox.delete(0, tk.END)
    for fabric in fabrics:
        listbox.insert(tk.END, fabric)

def add_fabric():
    name = simpledialog.askstring("Добавить ткань", "Введите название ткани:")
    if not name:
        return
    coef = simpledialog.askfloat("Коэффициент", "Сколько метров в 1 кг?:")
    if not coef:
        return
    fabrics[name] = coef
    save_fabrics(fabrics)
    refresh_listbox()

def edit_fabric():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Ошибка", "Выберите ткань для редактирования.")
        return
    name = listbox.get(selection[0])
    new_coef = simpledialog.askfloat("Редактировать", f"Новый коэффициент для {name}:")
    if new_coef:
        fabrics[name] = new_coef
        save_fabrics(fabrics)
        refresh_listbox()

def delete_fabric():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Ошибка", "Выберите ткань для удаления.")
        return
    name = listbox.get(selection[0])
    confirm = messagebox.askyesno("Подтверждение", f"Удалить ткань {name}?")
    if confirm:
        del fabrics[name]
        save_fabrics(fabrics)
        refresh_listbox()

def calculate():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Ошибка", "Выберите ткань.")
        return
    fabric = listbox.get(selection[0])
    coef = fabrics[fabric]
    try:
        value = float(entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите число.")
        return
    if var.get() == 1:
        result = convert_to_kg(value, coef)
        messagebox.showinfo("Результат", f"{value} м = {result:.2f} кг")
    else:
        result = convert_to_meters(value, coef)
        messagebox.showinfo("Результат", f"{value} кг = {result:.2f} м")

fabrics = load_fabrics()

root = tk.Tk()
root.title("Калькулятор тканей")

frame = tk.Frame(root)
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=30, height=10)
listbox.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

refresh_listbox()

entry = tk.Entry(root)
entry.pack(pady=5)

var = tk.IntVar(value=1)
rb1 = tk.Radiobutton(root, text="Метры → Килограммы", variable=var, value=1)
rb2 = tk.Radiobutton(root, text="Килограммы → Метры", variable=var, value=2)
rb1.pack()
rb2.pack()

btn_calc = tk.Button(root, text="Рассчитать", command=calculate)
btn_calc.pack(pady=5)

btn_add = tk.Button(root, text="Добавить ткань", command=add_fabric)
btn_add.pack(pady=2)

btn_edit = tk.Button(root, text="Редактировать ткань", command=edit_fabric)
btn_edit.pack(pady=2)

btn_delete = tk.Button(root, text="Удалить ткань", command=delete_fabric)
btn_delete.pack(pady=2)

root.mainloop()
