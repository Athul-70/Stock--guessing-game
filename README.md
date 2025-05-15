# 📈 Stock Market Guessing Game

An interactive Python game built with Tkinter that challenges users to guess whether selected stock prices will go up or down. Players make predictions based on real-time data from a public API.

---

## 🎮 Features

- 🎯 Single Player Mode
- 🔁 Real-time Stock Price Retrieval (via RapidAPI)
- 📊 Currency Display Conversion (USD, EUR, INR, GBP)
- ⏱️ Difficulty Levels:
  - Easy: 10s to decide, 10s prediction delay
  - Medium: 7s to decide, 20s prediction delay
  - Hard: 5s to decide, 30s prediction delay
- 🎨 Theme Selection: Light, Sky Blue, Mint Green
- 📈 Score Tracker & Accuracy Breakdown per Stock
- 🎉 Visual Feedback (Background Color Changes)
- 🔔 Timer and Countdown Displays

---

## 🧠 How it Works

1. Player enters their name
2. Select stocks from the list (AAPL, GOOGL, etc.)
3. Choose difficulty, theme, and display currency
4. Guess whether the stock will go UP or DOWN
5. After a timed delay, the app fetches updated price
6. Score updates based on correctness

---

## 🧰 OOP Principles Used

This game is developed using core Object-Oriented Programming concepts:

- ✅ **Encapsulation** – All components are organized into classes (`Player`, `StockDataFetcher`, `GUI`)
- ✅ **Abstraction** – Complex logic (e.g. API calls, prediction evaluation) is hidden behind clean method interfaces
- ✅ **Inheritance** – `Player` and `AIPlayer` inherit from a shared `BasePlayer`
- ✅ **Polymorphism** – `record_result()` behaves differently for `AIPlayer` and `Player`

---

## 🔧 Requirements

- Python 3.7+
- `requests` module

Install dependencies:

```bash
pip install requests
```

---

## 🚀 Run the Game

```bash
python stock_guess_game.py
```

---

## 📂 APIs Used

- 🧾 [Twelve Data API](https://rapidapi.com/twelvedata/api/twelve-data1)
- 🌐 [ExchangeRate API](https://open.er-api.com)

---

## 📊 Example Output

```
Ammu's Score: 4/5
AAPL: 2/2 correct (100.0%)
GOOGL: 1/2 correct (50.0%)
TSLA: 1/1 correct (100.0%)
```

---

## 🧪 Scope & Limitations

- Designed for learning and demonstration
- Slight delays may affect API prediction timing
- Currently supports **single player only**

---

## 💡 Potential Future Features

- AI Auto-Guess Mode 🤖
- Leaderboard with Local High Scores 🏆
- Visual Analytics (Trend Charts) 📈

---

## 👨‍💻 Author

Developed by **Athul Antony, Krishnapriya Kumaran, Aswanth Krishna**  
_Object-Oriented Programming Coursework Project_

> “Guess the market. Beat the odds!”
