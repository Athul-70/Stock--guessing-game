import tkinter as tk
from tkinter import messagebox
import json
import requests

class BasePlayer:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.history = []

    def record_result(self, result):
        self.history.append(result)

class Player(BasePlayer):
    def record_result(self, result):
        super().record_result(result)

class AIPlayer(BasePlayer):
    def record_result(self, result):
        print(f"[AI DEBUG] {result}")
        super().record_result(result)

class StockDataFetcher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StockDataFetcher, cls).__new__(cls)
        return cls._instance

    def fetch_current_price(self, symbol):
        url = f"https://twelve-data1.p.rapidapi.com/price?symbol={symbol}&format=json"
        headers = {
            "X-RapidAPI-Key": "eee06b3aa1mshf2ae03a7b08ce33p1dfbdcjsn1745b9893cca",
            "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
        }
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            return float(data.get("price", 0.0))
        except:
            return 0.0

    def fetch_exchange_rate(self, from_curr, to_curr):
        url = f"https://open.er-api.com/v6/latest/{from_curr}"
        try:
            response = requests.get(url)
            data = response.json()
            return float(data["rates"].get(to_curr, 1.0))
        except:
            return 1.0

class PredictionManager:
    def evaluate_guess(self, old_price, new_price, guess):
        return ('U' if new_price > old_price else 'D') == guess

class StockGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Market Guessing Game")
        self.root.geometry("500x600")

        self.difficulty = tk.StringVar(value="Medium")
        self.theme = tk.StringVar(value="Light")
        self.currency = tk.StringVar(value="USD")
        self.symbols = ["AAPL", "GOOGL", "AMZN", "TSLA", "MSFT"]

        self.fetcher = StockDataFetcher()
        self.manager = PredictionManager()
        self.player1 = None
        self.current_player = None

        self.rounds = tk.IntVar(value=5)
        self.selected_symbols = []
        self.timer_seconds = 15
        self.prediction_delay = 10
        self.timer_id = None
        self.current_symbol_index = 0
        self.current_round = 0
        self.old_price = 0.0
        self.usd_to_selected = self.fetcher.fetch_exchange_rate("USD", self.currency.get())

        self.load_theme()
        self.create_widgets()
        self.apply_theme()

    def load_theme(self):
        try:
            with open("settings.json", "r") as f:
                saved = json.load(f)
                self.theme.set(saved.get("theme", "Light"))
        except:
            pass

    def apply_theme(self, _=None):
        themes = {
            "Light": {"bg": "#ffffff", "fg": "#000000"},
            "Sky Blue": {"bg": "#e0f7fa", "fg": "#004d40"},
            "Mint Green": {"bg": "#e6f9f0", "fg": "#2e7d32"}
        }
        theme = themes.get(self.theme.get(), themes["Light"])
        self.root.config(bg=theme["bg"])
        self.frame.config(bg=theme["bg"])
        self.button_frame.config(bg=theme["bg"])
        for widget in self.frame.winfo_children():
            try:
                widget.config(bg=theme["bg"], fg=theme["fg"])
            except:
                pass
        for widget in self.button_frame.winfo_children():
            try:
                widget.config(bg=theme["bg"], fg=theme["fg"])
            except:
                pass
        with open("settings.json", "w") as f:
            json.dump({"theme": self.theme.get()}, f)

    def create_widgets(self):
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        tk.Label(self.frame, text="Enter your name:").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()

        tk.Label(self.frame, text="Select stock:").pack()
        self.stock_listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE)
        for symbol in self.symbols:
            self.stock_listbox.insert(tk.END, symbol)
        self.stock_listbox.pack()

        tk.Label(self.frame, text="Number of Rounds:").pack()
        tk.Spinbox(self.frame, from_=1, to=20, textvariable=self.rounds).pack()

        tk.Label(self.frame, text="Currency:").pack()
        tk.OptionMenu(self.frame, self.currency, "USD", "EUR", "GBP", "INR", command=self.update_currency).pack()

        tk.Label(self.frame, text="Select Difficulty:").pack()
        tk.OptionMenu(self.frame, self.difficulty, "Easy", "Medium", "Hard").pack()

        tk.Label(self.frame, text="Select Theme:").pack()
        tk.OptionMenu(self.frame, self.theme, "Light", "Sky Blue", "Mint Green", command=self.apply_theme).pack()

        self.start_button = tk.Button(self.frame, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.score_label = tk.Label(self.frame, text="Score: 0")
        self.score_label.pack()

        self.timer_label = tk.Label(self.frame, text="")
        self.timer_label.pack()

        self.feedback_label = tk.Label(self.frame, text="")
        self.feedback_label.pack()

        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=5)
        self.up_button = tk.Button(self.button_frame, text="⬆ UP", command=lambda: self.handle_guess('U'))
        self.up_button.grid(row=0, column=0, padx=10)
        self.down_button = tk.Button(self.button_frame, text="⬇ DOWN", command=lambda: self.handle_guess('D'))
        self.down_button.grid(row=0, column=1, padx=10)

        self.disable_guess_buttons()

    def update_currency(self, _):
        self.usd_to_selected = self.fetcher.fetch_exchange_rate("USD", self.currency.get())

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        selection = self.stock_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a stock.")
            return
        self.symbol = self.stock_listbox.get(selection[0])
        self.player1 = Player(name)
        self.current_player = self.player1

        self.selected_symbols = [self.symbol]
        self.current_symbol_index = 0
        self.current_round = 0

        level = self.difficulty.get()
        self.timer_seconds = {"Easy": 10, "Medium": 7, "Hard": 5}.get(level, 7)
        self.prediction_delay = {"Easy": 10, "Medium": 20, "Hard": 30}.get(level, 20)

        self.apply_theme()
        self.play_round()

    def play_round(self):
        if self.current_round >= self.rounds.get():
            self.show_results()
            return
        symbol = self.selected_symbols[self.current_symbol_index]
        self.old_price = self.fetcher.fetch_current_price(symbol)
        converted_price = self.old_price * self.usd_to_selected
        display_currency = self.currency.get()
        self.feedback_label.config(text=f"{symbol} price: ${self.old_price:.2f} ({display_currency} {converted_price:.2f})", fg="black")
        self.timer_label.config(text=f"Time remaining: {self.timer_seconds}s")
        self.enable_guess_buttons()
        self.countdown()

    def countdown(self):
        if self.timer_seconds > 0:
            self.timer_label.config(text=f"Time remaining: {self.timer_seconds}s")
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self.countdown)
        else:
            self.disable_guess_buttons()
            self.feedback_label.config(text="⏱ Time's up! Skipping round.", fg="orange")
            self.frame.config(bg="#fff3cd")
            self.current_round += 1
            self.root.after(1500, self.reset_feedback_and_continue)

    def handle_guess(self, guess):
        self.root.after_cancel(self.timer_id)
        self.disable_guess_buttons()
        self.prediction_countdown = self.prediction_delay
        self.update_prediction_wait(guess)

    def update_prediction_wait(self, guess):
        if self.prediction_countdown > 0:
            self.feedback_label.config(text=f"⏳ Waiting... {self.prediction_countdown}s", fg="blue")
            self.prediction_countdown -= 1
            self.root.after(1000, lambda: self.update_prediction_wait(guess))
        else:
            self.evaluate_guess_delayed(guess)

    def evaluate_guess_delayed(self, guess):
        symbol = self.selected_symbols[self.current_symbol_index]
        new_price = self.fetcher.fetch_current_price(symbol)
        correct = self.manager.evaluate_guess(self.old_price, new_price, guess)

        result = {
            "round": self.current_round + 1,
            "symbol": symbol,
            "old_price": self.old_price,
            "new_price": new_price,
            "guess": guess,
            "correct": correct
        }
        self.current_player.record_result(result)

        if correct:
            self.current_player.score += 1
            self.feedback_label.config(text="✅ Correct Guess!", fg="green")
            self.root.config(bg="#d4edda"); self.frame.config(bg="#d4edda")
        else:
            self.feedback_label.config(text="❌ Wrong Guess!", fg="red")
            self.root.config(bg="#f8d7da"); self.frame.config(bg="#f8d7da")

        self.current_round += 1
        self.root.after(1500, self.reset_feedback_and_continue)

    def reset_feedback_and_continue(self):
        self.frame.config(bg=self.root.cget("bg"))
        self.feedback_label.config(fg="black")
        self.timer_label.config(text="")
        self.play_round()

    def enable_guess_buttons(self):
        self.up_button.config(state=tk.NORMAL)
        self.down_button.config(state=tk.NORMAL)

    def disable_guess_buttons(self):
        self.up_button.config(state=tk.DISABLED)
        self.down_button.config(state=tk.DISABLED)

    def show_results(self):
        summary = f"{self.player1.name}'s Score: {self.player1.score}/{self.rounds.get()}\n"
        stock_perf = {}
        for record in self.player1.history:
            sym = record['symbol']
            if sym not in stock_perf:
                stock_perf[sym] = {'correct': 0, 'total': 0}
            stock_perf[sym]['total'] += 1
            if record['correct']:
                stock_perf[sym]['correct'] += 1
        for sym, stats in stock_perf.items():
            percent = (stats['correct'] / stats['total']) * 100
            summary += f"{sym}: {stats['correct']}/{stats['total']} correct ({percent:.1f}%)\n"
        messagebox.showinfo("Game Over", summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockGameGUI(root)
    root.mainloop()
