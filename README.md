# PyLog Threat Analyser 🐍

A lightweight, command-line utility built with Python for parsing Apache web server logs to identify and summarise potential threats based on HTTP error codes. This tool is designed to quickly provide a high-level overview of suspicious activity by identifying top offenders.

---

## 📸 Demo

![PyLog Threat Analyser Demo](demo.png)

---

## ✨ Key Features

* **Log Parsing:** Efficiently reads and processes standard Apache `access.log` files line by line.
* **Error Identification:** Detects and flags both client-side (`4xx`) and server-side (`5xx`) errors.
* **Threat Summarisation:** Aggregates total requests and error counts for each unique IP address.
* **Prioritised Reporting:** Automatically sorts the output to display the IP addresses with the highest error counts at the top.
* **Professional CLI:** Utilises `argparse` for a clean and user-friendly command-line interface.
* **Formatted Output:** Presents the final report in a clean, human-readable table using `beautifultable`.

---

## 🛠️ Tech Stack

* **Language:** Python 3
* **Core Libraries:**
    * `argparse` for command-line argument parsing.
    * `beautifultable` for formatted console output.

---

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Sosars/Apache-Log-Analyser.git](https://github.com/Sosars/Apache-Log-Analyser.git)
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd Apache-Log-Analyser
    ```

3.  **Install the required packages:**
    ```bash
    py -m pip install beautifultable
    ```

---

## 🚀 Usage

Run the script from the command line, providing the path to the log file you wish to analyse using the `-f` or `--file` argument.

```bash
python your_script_name.py --file /path/to/your/access.log
