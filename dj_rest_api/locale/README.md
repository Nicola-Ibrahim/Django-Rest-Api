# Internationalization

- For windows system:

  Install gettext package by using the following [link](https://mlocati.github.io/articles/gettext-iconv-windows.html)

- For linux system:

  Install the gettext package via the terminal:

  ```bash
  sudo apt install gettext
  ```

## Run translate

- With default translation value (en):

  ```bash
    make translate
  ```

- With custom translation value:

  ```bash
    make translate lang=[fr|de|...]
  ```

## Run compile

  ```bash
    make translate-compile
  ```
