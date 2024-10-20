# Research_Paper

## 📚 Overview

Research_Paper is a Streamlit web application designed to extract key metadata—such as the title, authors, and publication year—from research paper PDFs. By leveraging GROBID, a powerful tool for extracting information from scholarly documents, this app provides an efficient way to parse and analyze academic papers.

## ✨ Features

- 📄 Upload PDF: Easily upload research paper PDFs.
- 🔍 Extract Metadata: Automatically extract titles, authors, and publication years using GROBID.
- 📊 View Results: Display extracted metadata within the app.
- 💾 Download CSV: Download the metadata as a CSV file for your records.
- 🐳 Docker Integration: Simplified setup of GROBID using Docker containers.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your computer:

- Python 3.6 or higher: [Download Python](https://www.python.org/downloads/)
- Git: [Download Git](https://git-scm.com/downloads)
- Docker: [Download Docker](https://www.docker.com/products/docker-desktop)

> Note: Docker is used to run GROBID, which handles the metadata extraction.

## 🚀 Installation**

Follow these steps to set up and run **Research_Paper** on your local machine.

### 1. Clone the Repository

Start by cloning the project repository to your local machine using Git.

```bash
git clone https://github.com/your-username/Research_Paper.git
cd Research_Paper
```

*Replace `your-username` with your actual GitHub username.*

### 2. Set Up a Virtual Environment

A virtual environment helps manage project-specific dependencies without affecting other Python projects.

#### On macOS/Linux:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

#### On Windows:

```batch
python -m venv myenv
myenv\Scripts\activate
```

*After activation, your terminal will show `(myenv)` indicating the virtual environment is active.*

### 3. Install Dependencies

With the virtual environment activated, install the required Python packages.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install and Run GROBID Using Docker

GROBID is essential for extracting metadata from PDFs. Using Docker simplifies its setup.

#### a. Pull the GROBID Docker Image

```bash
docker pull lfoppiano/grobid:0.7.2
```

#### b. Run the GROBID Docker Container

```bash
docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.7.2
```

- `-d`: Runs the container in detached mode (in the background).
- `--name grobid`: Names the container `grobid` for easy reference.
- `-p 8070:8070`: Maps port `8070` of the container to port `8070` on your computer.

#### c. Verify GROBID is Running

Open your web browser and go to [http://localhost:8070](http://localhost:8070). You should see the GROBID service page.

### 5. Run the Application

Start the Streamlit app to begin using the metadata extractor.

```bash
streamlit run app.py
```

*This command will open the application in your default web browser at [http://localhost:8501](http://localhost:8501).*

---

## 🖥️ Usage

Once the application is running, follow these steps to extract metadata from your research papers:

1. Open the App:
   - Navigate to [http://localhost:8501](http://localhost:8501) in your web browser.

2. Upload a PDF:
   - Click on the "Browse files" button and select a research paper PDF from your computer.

3. Extract Metadata:
   - The app will process the PDF using GROBID and display the extracted metadata, including the title, authors, and publication year.

4. Download CSV:
   - Click the "Download Metadata as CSV" button to save the extracted information for your records.

---

## 🛠️ **Troubleshooting**

Encountering issues during setup or usage? Below are some common problems and their solutions.

### 1. GROBID Not Running

- Symptom: Unable to access [http://localhost:8070](http://localhost:8070); extraction fails.
- Solution:
  - Ensure Docker is installed and running.
  - Check if the GROBID container is active:

    ```bash
    docker ps
    ```

    You should see a container named `grobid` running.

  - If not running, start the container:

    ```bash
    docker start grobid
    ```

### 2. Port Conflicts

- Symptom: Ports `8070` (GROBID) or `8501` (Streamlit) are already in use.
- Solution:
  - Change GROBID's Port:

    ```bash
    docker run -d --name grobid -p 8071:8070 lfoppiano/grobid:0.7.2
    ```

    - Update the `grobid_process_pdf` function in `app.py` to use the new port (`8071`).

  - Change Streamlit's Port:

    ```bash
    streamlit run app.py --server.port=8502
    ```

    - Update the URL accordingly when accessing the app.

### 3. Virtual Environment Activation Issues

- Symptom: Errors when activating the virtual environment.
- Solution:
  - Ensure you're in the correct project directory.
  - For macOS/Linux, make sure the `setup.sh` script has execute permissions:

    ```bash
    chmod +x setup.sh
    ```

### 4. Dependency Installation Errors

- **Symptom: Errors during `pip install -r requirements.txt`.
- Solution:
  - Ensure `requirements.txt` is correctly formatted and lists all necessary packages.
  - Verify your internet connection.
  - Try upgrading `pip`:

    ```bash
    pip install --upgrade pip
    ```

### 5. Streamlit App Not Launching

- Symptom: App doesn't open or shows errors.
- Solution:
  - Ensure all dependencies are installed.
  - Check the terminal for error messages and address them accordingly.
  - Verify that GROBID is running and accessible.

---

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any questions, suggestions, or feedback, feel free to reach out:

Email: titikshit@gmail.com
