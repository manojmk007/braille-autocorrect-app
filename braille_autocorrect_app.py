import streamlit as st
import time
import io

# Braille key to dot mapping
key_to_dot = {'D': 1, 'W': 2, 'Q': 3, 'K': 4, 'O': 5, 'P': 6}

# Braille alphabet: Letter -> (dots, unicode)
braille_alphabet = {
    'A': ([1], '⠁'), 'B': ([1, 2], '⠃'), 'C': ([1, 4], '⠉'),
    'D': ([1, 4, 5], '⠙'), 'E': ([1, 5], '⠑'), 'F': ([1, 2, 4], '⠋'),
    'G': ([1, 2, 4, 5], '⠛'), 'H': ([1, 2, 5], '⠓'), 'I': ([2, 4], '⠊'),
    'J': ([2, 4, 5], '⠚'), 'K': ([1, 3], '⠅'), 'L': ([1, 2, 3], '⠇'),
    'M': ([1, 3, 4], '⠍'), 'N': ([1, 3, 4, 5], '⠝'), 'O': ([1, 3, 5], '⠕'),
    'P': ([1, 2, 3, 4], '⠏'), 'Q': ([1, 2, 3, 4, 5], '⠟'), 'R': ([1, 2, 3, 5], '⠗'),
    'S': ([2, 3, 4], '⠎'), 'T': ([2, 3, 4, 5], '⠞'), 'U': ([1, 3, 6], '⠥'),
    'V': ([1, 2, 3, 6], '⠧'), 'W': ([2, 4, 5, 6], '⠺'), 'X': ([1, 3, 4, 6], '⠭'),
    'Y': ([1, 3, 4, 5, 6], '⠽'), 'Z': ([1, 3, 5, 6], '⠵')
}

# Reverse mapping: dot pattern to letter and unicode
dots_to_letter = {frozenset(d): (l, u) for l, (d, u) in braille_alphabet.items()}

# Convert user input keys to dots
def keys_to_dots(keys):
    return frozenset(key_to_dot.get(k.upper()) for k in keys if k.upper() in key_to_dot)

# Autocorrect logic
def autocorrect_suggestions(dots):
    suggestions = []
    min_diff = float('inf')
    for known_dots, (letter, braille) in dots_to_letter.items():
        diff = len(known_dots.symmetric_difference(dots))
        if diff < min_diff:
            suggestions = [(letter, braille)]
            min_diff = diff
        elif diff == min_diff:
            suggestions.append((letter, braille))
    return suggestions

# Main interface
st.set_page_config(page_title="Braille Autocorrect", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🔡 Braille Autocorrect System</h1>", unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown("### ⌨️ Instructions")
    st.markdown("""
    - Type Braille using QWERTY key equivalents: **D, W, Q, K, O, P**
    - Each line should be a Braille character combination (e.g., `D W` → **A**)
    - Examples:
        - `D W` → A
        - `D K` → C
        - `W Q K O P` → extra key
    """)
    user_input = st.text_area("Enter Braille combinations (one per line):", height=250, key="braille_input")
    run_decoding = st.button("🔍 Decode Input")

with right:
    st.markdown("### 📋 Output")
    decoded_lines = []

    if run_decoding and user_input.strip():
        lines = user_input.strip().split('\n')
        for i, line in enumerate(lines, 1):
            keys = [k.strip() for k in line.upper().split()]
            dots = keys_to_dots(keys)

            if not dots:
                decoded_lines.append(f"❌ Line {i}: No valid keys detected.")
                continue

            result = dots_to_letter.get(dots)
            if result:
                letter, symbol = result
                decoded_lines.append(f"✅ Line {i}: `{line}` → **{letter}** ({symbol})")
            else:
                suggestions = autocorrect_suggestions(dots)
                formatted = ", ".join([f"**{l}** ({b})" for l, b in suggestions])
                decoded_lines.append(f"⚠️ Line {i}: `{line}` → No exact match. Suggestions: {formatted}")

        for out in decoded_lines:
            st.markdown(f"- {out}")

        # Downloadable decoded result
        decoded_text = '\n'.join([out.replace('`', '') for out in decoded_lines])
        download_file = decoded_text.encode('utf-8')  # Convert to bytes
        st.download_button("📥 Download Decoded Output", data=download_file, file_name="braille_output.txt")

        # Copyable output
        with st.expander("📎 Copyable Output"):
            st.code(decoded_text, language="text")

    elif run_decoding:
        st.info("Start typing Braille combinations to see results.")
