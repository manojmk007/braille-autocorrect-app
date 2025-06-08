
# Braille Autocorrect System

This project is a smart Braille input autocorrect system designed for users entering Braille characters using a standard QWERTY keyboard.

## 🔗 Live Application
Access the app here: [Braille Autocorrect App](https://braille-autocorrect-app-uutmdincghac9qdh9k6dw5.streamlit.app/)

## 💡 Features
- Input Braille characters using QWERTY keys: **D, W, Q, K, O, P** (representing Braille dots 1–6).
- Real-time decoding and autocorrection for typo-prone entries.
- Unicode Braille symbol output.
- Intelligent suggestions when input patterns don’t match exactly.
- Download decoded output as a `.txt` file.
- Clean and intuitive user interface.

## 🧪 Sample Test Input
```
D W
D K
W Q K O P
```
- D W → A
- D K → C
- W Q K O P → Suggests the closest valid Braille letter

## 📁 How to Use
1. Go to the live app link.
2. Enter your Braille combinations, one per line.
3. View real-time decoded output on the right side.
4. Download or copy the output as needed.

---
Made with ❤️ using Python and Streamlit.
