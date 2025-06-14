import json
import os
import sys
import tkinter as tk
from tkinter import messagebox
import random

# Определяем путь к папке, где находится .exe или скрипт
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Путь к JSON-файлу
file_path = os.path.join(base_path, 'data.json')

# Проверка и создание JSON-файла
if not os.path.exists(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({}, file, ensure_ascii=False, indent=4)

# Функция для чтения JSON
def load_data():
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Функция для сохранения JSON
def save_data(data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Создаем главное окно
main_window = tk.Tk()
main_window.title("Word memory 1.0")
main_window.geometry("600x400")

# Функция для окна добавления слова
def open_add_word_window():
    main_window.withdraw()
    add_window = tk.Toplevel()
    add_window.title("Add a word")
    add_window.geometry("600x400")

    tk.Label(add_window, text="Russian word:", font=("Arial", 12)).pack(pady=15)
    rus_entry = tk.Entry(add_window, width=40, font=("Arial", 12), borderwidth=2, relief="groove")
    rus_entry.pack(pady=10)

    tk.Label(add_window, text="English translation:", font=("Arial", 12)).pack(pady=15)
    eng_entry = tk.Entry(add_window, width=40, font=("Arial", 12), borderwidth=2, relief="groove")
    eng_entry.pack(pady=10)

    def save_word():
        rus = rus_entry.get().strip()
        eng = eng_entry.get().strip()
        if not rus or not eng:
            messagebox.showerror("Error", "Fill in all fields!")
            return
        data = load_data()
        data[rus] = eng
        save_data(data)
        messagebox.showinfo("Success", f"The Word '{rus}' added!")
        rus_entry.delete(0, tk.END)
        eng_entry.delete(0, tk.END)
        update_word_count()  # Обновляем количество слов после добавления

    tk.Button(add_window, text="Save", command=save_word, font=("Arial", 12), padx=10, pady=5, borderwidth=2, relief="groove").pack(pady=15)
    tk.Button(add_window, text="Back", command=lambda: back_to_main(add_window), font=("Arial", 12), padx=10, pady=5, borderwidth=2, relief="groove").pack(pady=15)

# Функция для окна теста
def open_test_window():
    data = load_data()
    if not data:
        messagebox.showerror("Error", "The dictionary is empty! Add words.")
        return

    main_window.withdraw()
    test_window = tk.Toplevel()
    test_window.title("Test")
    test_window.geometry("600x400")

    # Настраиваем сетку
    test_window.grid_columnconfigure(0, weight=1)
    test_window.grid_columnconfigure(1, weight=1)

    # Выбираем случайное слово
    def get_random_word():
        return random.choice(list(data.keys()))

    current_word = get_random_word()
    word_label = tk.Label(test_window, text=f"Word: {current_word}", font=("Arial", 14))
    word_label.grid(row=0, column=0, columnspan=2, pady=20)

    tk.Label(test_window, text="Your translation:", font=("Arial", 12)).grid(row=1, column=0, columnspan=2, pady=15)
    answer_entry = tk.Entry(test_window, width=40, font=("Arial", 12), borderwidth=2, relief="groove")
    answer_entry.grid(row=2, column=0, columnspan=2, pady=10)

    result_label = tk.Label(test_window, text="", font=("Arial", 12))
    result_label.grid(row=3, column=0, columnspan=2, pady=15)

    def check_answer():
        user_answer = answer_entry.get().strip()
        correct_answer = data[current_word]
        result_label.config(text=f"Correct translation: {correct_answer}")

    def check_answer_with_color():
        nonlocal current_word
        user_answer = answer_entry.get().strip()
        correct_answer = data[current_word]
        if user_answer.lower() == correct_answer.lower():
            answer_entry.config(fg="green")
            test_window.after(1000, next_word)  # Переход к следующему слову через 1 секунду
        else:
            answer_entry.config(fg="red")

    def next_word():
        nonlocal current_word
        current_word = get_random_word()
        word_label.config(text=f"Word: {current_word}")
        answer_entry.delete(0, tk.END)
        answer_entry.config(fg="black")  # Сбрасываем цвет на чёрный
        result_label.config(text="")

    tk.Button(test_window, text="Check", command=check_answer_with_color, font=("Arial", 12), padx=15, pady=8, borderwidth=2, relief="groove").grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(test_window, text="Back", command=lambda: back_to_main(test_window), font=("Arial", 12), padx=10, pady=5, borderwidth=2, relief="groove").grid(row=5, column=0, padx=5, pady=5, sticky="e")
    tk.Button(test_window, text="Correct translation", command=check_answer, font=("Arial", 12), padx=10, pady=5, borderwidth=2, relief="groove").grid(row=5, column=1, padx=5, pady=5, sticky="w")

# Функция возврата к главному окну
def back_to_main(window):
    window.destroy()
    main_window.deiconify()
    update_word_count()  # Обновляем количество слов при возврате

# Функция закрытия программы
def close_program():
    main_window.destroy()

# Функция для обновления количества слов
def update_word_count():
    data = load_data()
    word_count = len(data)
    word_count_label.config(text=f"Words in dictionary: {word_count}")

# Элементы главного окна
tk.Label(main_window, text="Learn words, friend.", font=("Arial", 16)).pack(pady=20)
word_count_label = tk.Label(main_window, text="Words in dictionary: 0", font=("Arial", 12))
word_count_label.pack(pady=10)
tk.Button(main_window, text="Add a word", command=open_add_word_window, font=("Arial", 12), padx=10, pady=5, borderwidth=2, relief="groove").pack(pady=15)
tk.Button(main_window, text="Take the test", command=open_test_window, font=("Arial", 12), padx=10, pady=5, borderwidth=2, relief="groove").pack(pady=15)
tk.Button(main_window, text="Close", command=close_program, font=("Arial", 12), padx=10, pady=5, borderwidth=2, relief="groove").pack(pady=15)

# Инициализация количества слов при запуске
update_word_count()

# Запускаем главный цикл
main_window.mainloop()