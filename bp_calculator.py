import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import time
import sys
import ctypes


class AnimatedBPCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BP Calculator")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0d0d0d')
        self.root.resizable(True, True)

        # === УСТАНОВКА ИКОНКИ ПРИЛОЖЕНИЯ ===
        try:
            # Для EXE файла
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(os.path.dirname(sys.executable), 'icon.ico')
            else:
                # Для запуска как скрипт
                icon_path = 'icon.ico'

            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                print(f"✅ Иконка загружена: {icon_path}")
            else:
                print(f"⚠️ Файл иконки не найден: {icon_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки иконки: {e}")

        # Установка для панели задач Windows
        self.set_windows_taskbar_icon()

        # Получаем путь для сохранения данных рядом с исполняемым файлом
        if getattr(sys, 'frozen', False):
            # Если запущен как exe
            self.data_path = os.path.join(os.path.dirname(sys.executable), 'bp_data.json')
        else:
            # Если запущен как скрипт Python
            self.data_path = 'bp_data.json'

        # Переменные для хранения состояния
        self.tasks = {}
        self.favorites = set()
        self.total_bp = 0
        self.total_bp_vip = 0
        self.is_vip = tk.BooleanVar()
        self.notification_label = None

        # Данные заданий
        self.task_data = [
            ("Посетить любой сайт в браузере", 1, 2),
            ("Зайти в любой канал в Brawl", 1, 2),
            ("Поставить лайк любой анкете в Match", 1, 2),
            ("Прокрутить за DP серебрянный, золотой или driver кейс", 10, 20),
            ("Кинуть мяч питомцу 15 раз", 2, 4),
            ("15 выполненных питомцем команд", 2, 4),
            ("Ставка в колесе удачи в казино (межсерверное колесо)", 3, 6),
            ("Проехать 1 станцию на метро", 2, 4),
            ("Поймать 20 рыб", 4, 8),
            ("Выполнить 2 квеста любых клубов", 4, 8),
            ("Починить деталь в автосервисе", 1, 2),
            ("Забросить 2 мяча в баскетболе", 1, 2),
            ("Забить 2 гола в футболе", 1, 2),
            ("Победить в армрестлинге", 1, 2),
            ("Победить в дартс", 1, 2),
            ("Поиграть 1 минуту в волейбол", 1, 2),
            ("Поиграть 1 минуту в настольный теннис", 1, 2),
            ("Поиграть 1 минуту в большой теннис", 1, 2),
            ("Сыграть в мафию в казино", 3, 6),
            ("Сделать платеж по лизингу", 1, 2),
            ("Посадить траву в теплице", 4, 8),
            ("Запустить переработку обезболивающих в лаборатории", 4, 8),
            ("Принять участие в двух аирдропах", 4, 8),
            ("Выполнить 3 заказа дальнобойщиком", 2, 4),
            ("7 закрашенных граффити", 1, 2),
            ("Сдать 5 контрабанды", 2, 4),
            ("Участие в каптах/бизварах", 1, 2),
            ("Сдать Хаммер с ВЗХ", 3, 6),
            ("5 выданных медкарт в EMS", 2, 4),
            ("Закрыть 15 вызовов в EMS", 2, 4),
            ("Отредактировать 40 объявлений в WN", 2, 4),
            ("Взломать 15 замков на ограблениях домов или автоугонах", 2, 4),
            ("Закрыть 5 кодов в силовых структурах", 2, 4),
            ("Поставить на учет 2 автомобиля (для LSPD)", 1, 2),
            ("Произвести 1 арест в КПЗ", 1, 2),
            ("Выкупить двух человек из КПЗ", 2, 4),
            ("3 часа в онлайне (можно выполнять многократно за день)", 2, 4),
            ("Нули в казино", 2, 4),
            ("25 действий на стройке", 2, 4),
            ("25 действий в порту", 2, 4),
            ("25 действий в шахте", 2, 4),
            ("3 победы в Дэнс Баттлах", 2, 4),
            ("Заказ материалов для бизнеса вручную", 1, 2),
            ("20 подходов в тренажерном зале", 1, 2),
            ("Успешная тренировка в тире", 1, 2),
            ("10 посылок на почте", 1, 2),
            ("Арендовать киностудию", 2, 4),
            ("Купить лотерейный билет", 1, 2),
            ("Выиграть гонку в картинге", 1, 2),
            ("10 действий на ферме", 1, 2),
            ("Потушить 25 'огоньков' пожарным", 1, 2),
            ("Выкопать 1 сокровище(не мусор)", 1, 2),
            ("Проехать 1 уличную гонку", 1, 2),
            ("Выполнить 3 заказа дальнобойщиком", 2, 4),
            ("Два раза оплатить смену внешности у хирурга в EMS", 2, 4),
            ("Добавить 5 видео в кинотеатре", 1, 2),
            ("Выиграть 5 игр в тренировочном комплексе со ставкой (от 100$)", 1, 2),
            ("Выиграть 3 любых игры на арене со ставкой (от 100$)", 1, 2),
            ("2 круга на любом маршруте автобусника", 2, 4),
            ("5 раз снять 100% шкуру с животных", 2, 4)
        ]

        self.set_custom_theme()
        self.load_data()
        self.create_widgets()
        self.update_totals()
        self.create_notification_area()

        # Сообщение при первом запуске
        self.check_first_run()

    def set_windows_taskbar_icon(self):
        """Устанавливает иконку для панели задач Windows"""
        try:
            myappid = 'milv1e.bpcalculator.1.0'  # произвольный идентификатор
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            print("✅ AppUserModelID установлен для панели задач")
        except Exception as e:
            print(f"⚠️ Не удалось установить AppUserModelID: {e}")

    def check_first_run(self):
        """Проверяет первый ли это запуск и показывает справку"""
        if not os.path.exists(self.data_path):
            self.show_notification("🎯 Добро пожаловать! Двойной клик - выполнить, клик по ⭐ - в избранное", 5000)

    def set_custom_theme(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Настраиваем цвета для темной темы
        style.configure("Custom.Treeview",
                        background="#2d2d2d",
                        foreground="#ffffff",
                        fieldbackground="#2d2d2d",
                        borderwidth=0,
                        font=('Arial', 14))  # Увеличен шрифт с 12 до 14

        style.configure("Custom.Treeview.Heading",
                        background="#404040",
                        foreground="#ffffff",
                        relief="flat",
                        font=('Arial', 16, 'bold'))  # Увеличен шрифт заголовков

        style.map("Custom.Treeview.Heading",
                  background=[('active', '#505050')])

        style.configure("TFrame", background="#0d0d0d")
        style.configure("TLabel", background="#0d0d0d", foreground="#ffffff", font=('Arial', 11))
        style.configure("TLabelframe", background="#0d0d0d", foreground="#ffffff")
        style.configure("TLabelframe.Label", background="#0d0d0d", foreground="#ffffff", font=('Arial', 12, 'bold'))

        # Стиль для вкладок
        style.configure("Custom.TNotebook", background="#0d0d0d", borderwidth=0)
        style.configure("Custom.TNotebook.Tab",
                        background="#404040",
                        foreground="#ffffff",
                        padding=[15, 5],
                        font=('Arial', 12, 'bold'))
        style.map("Custom.TNotebook.Tab",
                  background=[("selected", "#00ff88")],
                  foreground=[("selected", "#000000")])

    def create_animated_button(self, parent, text, command, color="#404040", hover_color="#505050", width=20):
        btn = tk.Button(parent,
                        text=text,
                        command=command,
                        bg=color,
                        fg="#ffffff",
                        font=('Arial', 12, 'bold'),
                        borderwidth=0,
                        relief='flat',
                        width=width,
                        cursor='hand2')

        # Анимация при наведении
        def on_enter(e):
            btn.config(bg=hover_color)

        def on_leave(e):
            btn.config(bg=color)

        def on_press(e):
            btn.config(bg=color)
            self.root.after(100, lambda: btn.config(bg=hover_color))

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_press)

        return btn

    def create_vip_toggle(self, parent):
        toggle_frame = tk.Frame(parent, bg='#0d0d0d')

        # Текст статуса
        self.vip_status_label = tk.Label(toggle_frame,
                                         text="Обычный статус",
                                         font=('Arial', 12, 'bold'),
                                         bg='#0d0d0d',
                                         fg='#ffffff')
        self.vip_status_label.grid(row=0, column=0, padx=(0, 15))

        # Анимированный переключатель
        self.toggle_canvas = tk.Canvas(toggle_frame,
                                       width=80,
                                       height=40,
                                       bg='#0d0d0d',
                                       highlightthickness=0)
        self.toggle_canvas.grid(row=0, column=1)

        # Создаем переключатель
        self.draw_toggle()

        # Привязываем клик
        self.toggle_canvas.bind('<Button-1>', self.toggle_vip)

        return toggle_frame

    def draw_toggle(self):
        self.toggle_canvas.delete("all")

        if self.is_vip.get():
            # VIP включен - зеленый
            self.toggle_canvas.create_rectangle(0, 0, 80, 40, fill='#00ff88', outline='')
            self.toggle_canvas.create_oval(40, 5, 75, 35, fill='#ffffff', outline='')
            self.toggle_canvas.create_text(20, 20, text="VIP", font=('Arial', 10, 'bold'), fill='#000000')
        else:
            # VIP выключен - серый
            self.toggle_canvas.create_rectangle(0, 0, 80, 40, fill='#666666', outline='')
            self.toggle_canvas.create_oval(5, 5, 35, 35, fill='#ffffff', outline='')
            self.toggle_canvas.create_text(55, 20, text="OFF", font=('Arial', 10, 'bold'), fill='#ffffff')

    def toggle_vip(self, event):
        self.is_vip.set(not self.is_vip.get())
        self.animate_toggle()
        self.update_totals()
        self.save_data()  # Сохраняем при изменении VIP статуса
        self.show_notification("✅ Статус VIP изменен!", 2000)

    def animate_toggle(self):
        # Простая анимация перемещения
        for i in range(5):
            self.root.after(i * 50, self.draw_toggle)

        # Обновляем текст статуса
        status_text = "🌟 VIP статус" if self.is_vip.get() else "⚪ Обычный статус"
        status_color = "#ffaa00" if self.is_vip.get() else "#ffffff"
        self.vip_status_label.config(text=status_text, fg=status_color)

    def create_notification_area(self):
        # Создаем область для уведомлений
        self.notification_frame = tk.Frame(self.root, bg='#0d0d0d', height=40)
        self.notification_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
        self.notification_frame.pack_propagate(False)

    def show_notification(self, message, duration=3000):
        # Удаляем предыдущее уведомление
        if hasattr(self, 'notification_label') and self.notification_label:
            self.notification_label.destroy()

        # Создаем новое уведомление
        self.notification_label = tk.Label(self.notification_frame,
                                           text=message,
                                           font=('Arial', 11, 'bold'),
                                           bg='#00ff88',
                                           fg='#000000',
                                           padx=20,
                                           pady=10)
        self.notification_label.pack(fill=tk.X, pady=5)

        # Автоматически скрываем через указанное время
        self.root.after(duration, self.hide_notification)

    def hide_notification(self):
        if hasattr(self, 'notification_label') and self.notification_label:
            self.notification_label.destroy()
            self.notification_label = None

    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Верхняя панель с автором слева
        top_frame = tk.Frame(main_frame, bg='#0d0d0d')
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # Автор слева
        author_label = tk.Label(top_frame,
                                text="by: milv1e",
                                font=("Arial", 12, "bold"),
                                bg="#0d0d0d",
                                fg="#ffaa00")
        author_label.pack(side=tk.LEFT)

        # Заголовок по центру
        title_label = tk.Label(main_frame,
                               text="🎯 BP CALCULATOR",
                               font=("Arial", 24, "bold"),
                               bg="#0d0d0d",
                               fg="#00ff88")
        title_label.pack(pady=(0, 10))

        subtitle_label = tk.Label(main_frame,
                                  text="Трекер Bonus Points",
                                  font=("Arial", 14),
                                  bg="#0d0d0d",
                                  fg="#cccccc")
        subtitle_label.pack(pady=(0, 20))

        # Панель управления СВЕРХУ
        self.create_control_panel(main_frame)

        # VIP переключатель ЛЕВЕЕ
        vip_frame = self.create_vip_toggle(main_frame)
        vip_frame.pack(pady=(20, 15))

        # Фрейм для отображения итогов
        totals_frame = ttk.LabelFrame(main_frame, text="📊 СТАТИСТИКА BP", padding="15")
        totals_frame.pack(fill=tk.X, pady=(0, 15))

        # Создаем фрейм для меток статистики
        stats_frame = ttk.Frame(totals_frame)
        stats_frame.pack(fill=tk.X)

        self.total_label = tk.Label(stats_frame,
                                    text="Всего BP: 0",
                                    font=("Arial", 14, "bold"),
                                    bg="#0d0d0d",
                                    fg="#00ff88")
        self.total_label.grid(row=0, column=0, padx=(0, 30))

        self.total_vip_label = tk.Label(stats_frame,
                                        text="Всего BP с VIP: 0",
                                        font=("Arial", 14, "bold"),
                                        bg="#0d0d0d",
                                        fg="#ffaa00")
        self.total_vip_label.grid(row=0, column=1, padx=(0, 30))

        self.current_bp_label = tk.Label(stats_frame,
                                         text="Текущие BP: 0",
                                         font=("Arial", 16, "bold"),
                                         bg="#0d0d0d",
                                         fg="#ff4444")
        self.current_bp_label.grid(row=0, column=2)

        # Создаем Notebook для вкладок
        self.notebook = ttk.Notebook(main_frame, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Вкладка всех заданий
        self.all_tasks_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.all_tasks_frame, text="📋 ВСЕ ЗАДАНИЯ")

        # Вкладка избранных заданий
        self.favorites_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.favorites_frame, text="⭐ ИЗБРАННЫЕ")

        # Создаем содержимое для обеих вкладок
        self.create_all_tasks_tab()
        self.create_favorites_tab()

    def create_all_tasks_tab(self):
        # Фрейм для списка заданий с прокруткой
        tasks_frame = ttk.LabelFrame(self.all_tasks_frame, text="🎯 ВСЕ ЗАДАНИЯ", padding="10")
        tasks_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем Treeview для заданий
        columns = ('favorite', 'task', 'bp', 'status')
        self.tree = ttk.Treeview(tasks_frame, columns=columns, show='headings', height=20, style="Custom.Treeview")

        # Настраиваем колонки (фиксированные размеры)
        self.tree.heading('favorite', text='⭐')
        self.tree.heading('task', text='ЗАДАНИЕ')
        self.tree.heading('bp', text='BP')
        self.tree.heading('status', text='СТАТУС')

        self.tree.column('favorite', width=70, anchor=tk.CENTER, stretch=False)  # Увеличена ширина
        self.tree.column('task', width=800, anchor=tk.W, stretch=False)  # Увеличена ширина
        self.tree.column('bp', width=150, anchor=tk.CENTER, stretch=False)  # Увеличена ширина
        self.tree.column('status', width=160, anchor=tk.CENTER, stretch=False)  # Увеличена ширина

        # Запрещаем изменение размера колонок
        def disable_resize(event):
            if self.tree.identify_region(event.x, event.y) == "separator":
                return "break"

        self.tree.bind('<Button-1>', disable_resize)
        self.tree.bind('<B1-Motion>', disable_resize)

        # Создаем теги для цветов
        self.tree.tag_configure('completed', background='#1e3a28', foreground='#00ff88')
        self.tree.tag_configure('not_completed', background='#2d2d2d', foreground='#ffffff')
        self.tree.tag_configure('favorite', foreground='#ffd700')
        self.tree.tag_configure('vip_bonus', foreground='#ffaa00')

        # Добавляем scrollbar
        scrollbar = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Заполняем данными
        self.populate_all_tasks_tree()

        # Привязываем обработчики
        self.tree.bind('<Double-1>', self.on_task_double_click)
        self.tree.bind('<Button-1>', self.on_task_click)

    def create_favorites_tab(self):
        # Фрейм для избранных заданий
        favorites_tasks_frame = ttk.LabelFrame(self.favorites_frame, text="⭐ ИЗБРАННЫЕ ЗАДАНИЯ", padding="10")
        favorites_tasks_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем Treeview для избранных заданий
        columns = ('task', 'bp', 'status')
        self.favorites_tree = ttk.Treeview(favorites_tasks_frame, columns=columns, show='headings', height=25,
                                           style="Custom.Treeview")

        # Настраиваем колонки (РАЗРЕШАЕМ изменение размера)
        self.favorites_tree.heading('task', text='ЗАДАНИЕ')
        self.favorites_tree.heading('bp', text='BP')
        self.favorites_tree.heading('status', text='СТАТУС')

        # Устанавливаем начальные размеры, но разрешаем растягивание
        self.favorites_tree.column('task', width=700, anchor=tk.W, stretch=True)  # Увеличена ширина
        self.favorites_tree.column('bp', width=150, anchor=tk.CENTER, stretch=True)  # Увеличена ширина
        self.favorites_tree.column('status', width=160, anchor=tk.CENTER, stretch=True)  # Увеличена ширина

        # Теги для избранных
        self.favorites_tree.tag_configure('completed', background='#1e3a28', foreground='#00ff88')
        self.favorites_tree.tag_configure('not_completed', background='#2d2d2d', foreground='#ffffff')
        self.favorites_tree.tag_configure('favorite', foreground='#ffd700')

        # Добавляем scrollbar
        fav_scrollbar = ttk.Scrollbar(favorites_tasks_frame, orient=tk.VERTICAL, command=self.favorites_tree.yview)
        self.favorites_tree.configure(yscrollcommand=fav_scrollbar.set)

        self.favorites_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        fav_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Привязываем обработчик двойного клика
        self.favorites_tree.bind('<Double-1>', self.on_favorite_double_click)

        # Метка если нет избранных
        self.no_favorites_label = tk.Label(favorites_tasks_frame,
                                           text="⭐ Нет избранных заданий\n\nДобавьте задания в избранное, нажав на звездочку в основном списке",
                                           font=("Arial", 14),
                                           bg="#2d2d2d",
                                           fg="#666666")

    def create_control_panel(self, parent):
        control_frame = ttk.Frame(parent)
        control_frame.pack(pady=(0, 20))

        # Создаем анимированные кнопки (только сброс и статистика)
        self.reset_btn = self.create_animated_button(control_frame,
                                                     "🔄 СБРОСИТЬ ВСЕ",
                                                     self.reset_all,
                                                     "#ff4444", "#ff6666")
        self.reset_btn.grid(row=0, column=0, padx=(0, 10))

        self.stats_btn = self.create_animated_button(control_frame,
                                                     "📊 СТАТИСТИКА",
                                                     self.show_stats,
                                                     "#ffaa00", "#ffcc00")
        self.stats_btn.grid(row=0, column=1, padx=(0, 10))

    def populate_all_tasks_tree(self):
        # Очищаем дерево
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Добавляем задания
        for i, (task, bp, bp_vip) in enumerate(self.task_data):
            status = "✅ ВЫПОЛНЕНО" if self.tasks.get(i, False) else "❌ НЕ ВЫПОЛНЕНО"
            bp_text = f"{bp} | {bp_vip} 🌟"
            favorite = "⭐" if i in self.favorites else ""

            tags = []
            if self.tasks.get(i, False):
                tags.append('completed')
            else:
                tags.append('not_completed')

            if i in self.favorites:
                tags.append('favorite')

            tags.append('vip_bonus')

            self.tree.insert('', tk.END, iid=str(i),
                             values=(favorite, task, bp_text, status),
                             tags=tags)

    def populate_favorites_tree(self):
        # Очищаем дерево
        for item in self.favorites_tree.get_children():
            self.favorites_tree.delete(item)

        # Показываем/скрываем метку "нет избранных"
        if not self.favorites:
            self.no_favorites_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            self.no_favorites_label.place_forget()

        # Добавляем избранные задания
        for task_id in sorted(self.favorites):
            if task_id < len(self.task_data):
                task, bp, bp_vip = self.task_data[task_id]
                status = "✅ ВЫПОЛНЕНО" if self.tasks.get(task_id, False) else "❌ НЕ ВЫПОЛНЕНО"
                bp_text = f"{bp} | {bp_vip} 🌟"

                tags = ['favorite']
                if self.tasks.get(task_id, False):
                    tags.append('completed')
                else:
                    tags.append('not_completed')

                self.favorites_tree.insert('', tk.END, iid=str(task_id),
                                           values=(task, bp_text, status),
                                           tags=tags)

    def on_task_click(self, event):
        # Обработка клика по звездочке
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if item and column == '#1':  # Колонка с звездочкой
            task_id = int(item)
            if task_id in self.favorites:
                self.favorites.remove(task_id)
                self.show_notification("❌ Задание удалено из избранного", 2000)
            else:
                self.favorites.add(task_id)
                self.show_notification("⭐ Задание добавлено в избранное", 2000)

            self.update_task_display(task_id)
            self.populate_favorites_tree()
            self.save_data()  # Сохраняем при изменении избранных

    def on_task_double_click(self, event):
        # Переключение статуса выполнения при двойном клике
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if item and column != '#1':  # Не колонка с звездочкой
            task_id = int(item)
            self.tasks[task_id] = not self.tasks.get(task_id, False)
            self.update_task_display(task_id)
            self.update_totals()
            self.populate_favorites_tree()
            self.save_data()  # Сохраняем при изменении статуса выполнения

    def on_favorite_double_click(self, event):
        # Переключение статуса выполнения в избранных
        item = self.favorites_tree.identify_row(event.y)
        if item:
            task_id = int(item)
            self.tasks[task_id] = not self.tasks.get(task_id, False)
            self.update_task_display(task_id)
            self.update_totals()
            self.populate_favorites_tree()
            self.save_data()  # Сохраняем при изменении статуса выполнения

    def update_task_display(self, task_id):
        # Обновляем отображение в основном дереве
        status = "✅ ВЫПОЛНЕНО" if self.tasks.get(task_id, False) else "❌ НЕ ВЫПОЛНЕНО"
        favorite = "⭐" if task_id in self.favorites else ""

        tags = []
        if self.tasks.get(task_id, False):
            tags.append('completed')
        else:
            tags.append('not_completed')

        if task_id in self.favorites:
            tags.append('favorite')

        tags.append('vip_bonus')

        # Обновляем элемент в основном дереве
        self.tree.set(str(task_id), 'status', status)
        self.tree.set(str(task_id), 'favorite', favorite)
        self.tree.item(str(task_id), tags=tags)

        # Обновляем в избранных если нужно
        if task_id in self.favorites:
            if self.favorites_tree.exists(str(task_id)):
                self.favorites_tree.set(str(task_id), 'status', status)
                fav_tags = ['favorite']
                if self.tasks.get(task_id, False):
                    fav_tags.append('completed')
                else:
                    fav_tags.append('not_completed')
                self.favorites_tree.item(str(task_id), tags=fav_tags)

    def update_totals(self):
        self.total_bp = 0
        self.total_bp_vip = 0

        for task_id, completed in self.tasks.items():
            if completed and task_id < len(self.task_data):
                bp, bp_vip = self.task_data[task_id][1], self.task_data[task_id][2]
                self.total_bp += bp
                self.total_bp_vip += bp_vip

        # Обновляем отображение
        current_bp = self.total_bp_vip if self.is_vip.get() else self.total_bp
        self.total_label.config(text=f"Всего BP: {self.total_bp}")
        self.total_vip_label.config(text=f"Всего BP с VIP: {self.total_bp_vip}")
        self.current_bp_label.config(text=f"Текущие BP: {current_bp}")

        # Обновляем цвет текущих BP в зависимости от VIP статуса
        if self.is_vip.get():
            self.current_bp_label.config(fg="#ffaa00")
        else:
            self.current_bp_label.config(fg="#00ff88")

    def show_stats(self):
        completed = sum(self.tasks.values())
        total = len(self.task_data)
        percentage = (completed / total) * 100 if total > 0 else 0
        fav_count = len(self.favorites)

        # Создаем окно статистики с цветными смайликами
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Детальная статистика")
        stats_window.geometry("400x300")
        stats_window.configure(bg='#0d0d0d')
        stats_window.resizable(False, False)

        # Заголовок
        title_label = tk.Label(stats_window,
                               text="📊 ПОДРОБНАЯ СТАТИСТИКА",
                               font=("Arial", 16, "bold"),
                               bg="#0d0d0d",
                               fg="#00ff88")
        title_label.pack(pady=15)

        # Статистика
        stats_text = f"""
✅ Выполнено: {completed}/{total} заданий
📈 Прогресс: {percentage:.1f}%
⭐ Избранных: {fav_count} заданий
🎯 BP без VIP: {self.total_bp}
🌟 BP с VIP: {self.total_bp_vip}
💫 Текущий статус: {'VIP 🌟' if self.is_vip.get() else 'Обычный'}

💡 Совет: Используйте избранные для быстрого
доступа к важным заданиям!
        """

        stats_label = tk.Label(stats_window,
                               text=stats_text,
                               font=("Arial", 12),
                               bg="#0d0d0d",
                               fg="#ffffff",
                               justify=tk.LEFT)
        stats_label.pack(pady=10)

        # Кнопка закрытия
        close_btn = self.create_animated_button(stats_window,
                                                "❌ ЗАКРЫТЬ",
                                                stats_window.destroy,
                                                "#ff4444", "#ff6666",
                                                width=15)
        close_btn.pack(pady=10)

    def save_data(self):
        """Сохраняем данные в файл"""
        try:
            data = {
                'tasks': self.tasks,
                'favorites': list(self.favorites),
                'is_vip': self.is_vip.get()
            }
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Данные сохранены: {len(self.tasks)} выполненных, {len(self.favorites)} избранных")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")

    def reset_all(self):
        if messagebox.askyesno("🔄 Сброс всех данных",
                               "Вы уверены, что хотите сбросить ВСЕ задания?\nЭто действие нельзя отменить!"):
            self.tasks.clear()
            self.favorites.clear()
            self.populate_all_tasks_tree()
            self.populate_favorites_tree()
            self.update_totals()
            self.save_data()  # Сохраняем изменения после сброса
            self.show_notification("🔄 Все задания сброшены!", 3000)

    def load_data(self):
        """Загрузка данных из файла"""
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Загружаем выполненные задания
                    self.tasks = {int(k): v for k, v in data.get('tasks', {}).items()}
                    # Загружаем избранные задания
                    self.favorites = set(data.get('favorites', []))
                    # Загружаем VIP статус
                    self.is_vip.set(data.get('is_vip', False))

                    print(f"✅ Загружено: {len(self.tasks)} выполненных заданий, {len(self.favorites)} избранных")

                    # Обновляем отображение после загрузки
                    self.populate_all_tasks_tree()
                    self.populate_favorites_tree()

        except Exception as e:
            print(f"❌ Ошибка загрузки данных: {str(e)}")


def main():
    root = tk.Tk()
    app = AnimatedBPCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()