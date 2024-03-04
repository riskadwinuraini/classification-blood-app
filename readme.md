# Aplikasi Flask

Aplikasi web sederhana menggunakan Flask dan Keras.

## Persyaratan

- Python 3.6 atau lebih baru
- Flask
- Keras
- TensorFlow

## Instalasi

1. Buat virtual environment Python:

    ```bash
    python3 -m venv venv
    ```

2. Aktifkan virtual environment:

    - Pada Windows:

        ```bash
        venv\Scripts\activate
        ```

    - Pada Unix atau MacOS:

        ```bash
        source venv/bin/activate
        ```

3. Instal dependensi:

    ```bash
    pip install flask keras tensorflow
    ```

## Menjalankan Aplikasi

Setelah semua dependensi terinstal, Anda bisa menjalankan aplikasi dengan perintah berikut:

```bash
python run.py
```

Aplikasi sekarang harus berjalan di http://localhost:5000.

## Struktur Aplikasi

Berikut adalah struktur folder aplikasi:

```plaintext
/myflaskapp
    /venv
    /app
        /templates
            home.html
            result.html
        /static
            /css
                main.css
            /js
                main.js
            /img
        /models
            my_model.h5
        __init__.py
        views.py
        models.py
    config.py
    run.py
```

