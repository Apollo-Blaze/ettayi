# Ettayi Language

Tired of coding in English? Why not code in Malayalam for a change? Ettayi is a programming language that lets you write code in Manglish, blending Malayalam and English for a fun experience. Bring a little Kerala flair to your code and make programming a bit more exciting!

**Disclaimer:** No, this is *definitely* not copied from Bhai Lang! 😜
![Code](assets/1.jpeg)
![Output](assets/2.jpeg)

## Features

- Write and execute code in Malayalam using **.ettayi** files.
- Supports basic syntax like variables, loops, conditionals, and functions.
- Built on Python, with an intuitive structure.

## Keywords

- **para**: Used to print strings or variables (similar to `print`).
- **ivananu**: For assigning values to variables.
- **sathyavastha**: Boolean assignment (similar to `True` or `False`).
- **anenki**: Conditional.
- **allenki**: Elif statement.
- **avasanam**: Else statement.
- **cheyuka**: While loop.
- **ithinulil**: For loop.
- **choik**: Input statement (equivalent to `input`).

## Grammar Highlights

1. **Print Statement**:
   ```ettayi
   "Namaskaram, Lokame!" para;
   ```
2. **Variable Assignment**:
  ```ettayi
  ivananu x = 5;
  ```
3. **If-else-if-else**
  ```ettayi
  anenki (x > 0) {
    "Positive" para;
}
ithinulil (x = 1..10) {
    x para;
}
allenki{
  "hello" para;
}
````
  


## Installation

To install **Ettayi** Language, follow these steps:

1. Ensure you have Python 3.6 or higher installed on your system.

2. Install **Ettayi** using `pip`:

```bash
pip install ettayi
```

3. Once installed, you can run your `.ettayi` files directly from the terminal:

```bash
ettayi yourfile.ettayi
```

Or using Python:

```bash
python -m ettayi yourfile.ettayi
```

## Tech Stack

- **Python** (for language implementation)
- **Lark-parser** (for parsing the language syntax)

## Contributing

Feel free to fork, modify, and contribute to this project. Open issues and pull requests are welcome!

## License

MIT License. See the LICENSE file for details.


Enjoy coding!
