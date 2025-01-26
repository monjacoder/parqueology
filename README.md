# Parqueology
This is a personal fun project where I play with and learn about **Parquet** and **Python**.

## What is Parquet?
[Apache Parquet](https://parquet.apache.org/) is a columnar storage file format optimized for use with big data processing frameworks. It is designed for efficiency and performance, making it a popular choice for storing and analyzing large datasets.

## What does Parqueology do?
So far, I built two functionalities that were inspired by my struggle with parquet files.
#### 1. CSV to Parquet Converter:
Using this tab, you can upload a csv file (max 200MB in size) and convert it to a Parquet file.
#### 2. Parquet File Viewer:
Using this tab, you can upload a parquet file, and it will show you details about its metadata and schema, and a preview of the first 20 rows.

## What's Inside the repo so far?
Right now, the whole app is in one file: app/streamlit_app.py

    .
    ├── app                   # parqueology app files
    ├── data                  # Sample data
    ├── requirements.txt
    └── README.md

> **Note**: This app uses [Streamlit](https://streamlit.io/), an open-source framework for building data apps. For simple experimental projects like this one, Streamlit is often recommended over heavier frameworks like Django or Flask.
  
## Clone and run the parqueology app on Linux

Assuming you're a debian/ubuntu-based linux environment (personally I use [Linux Mint](https://linuxmint.com/)), 
here are the basic steps you need to follow:

1. **Ensure you have the latest version of `python3`, `python3-pip`, `python3-venv` and `git`**
    ```bash
    sudo apt update
    sudo apt install --only-upgrade python3 python3-pip python3-venv git
    python3 --version
    pip3 --version
    git --version
2. **Clone this repo**
    ```bash
    cd ~Projects/ # Replace with your preferred directory for Git repos
    git clone https://github.com/monjacoder/parqueology.git
    cd parqueology
3. **Set up a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
4. **Install dependencies**
    ```bash
    pip install -r requirements.txt
5. **Run the app using `streamlit`**
    ```bash
    streamlit run app/streamlit_app.py
## Contributions
If you have suggestions, feedback, or ideas, feel free to open an issue or reach out to me!
