@echo off
REM setup.bat - Script to set up the Research Paper Metadata Extractor

echo === Research Paper Metadata Extractor Setup ===

REM 1. Activate the virtual environment or create it if it doesn't exist
IF EXIST myenv (
    echo Activating existing virtual environment...
    call myenv\Scripts\activate
) ELSE (
    echo Virtual environment 'myenv' not found. Creating...
    python -m venv myenv
    call myenv\Scripts\activate
)

REM 2. Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM 3. Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM 4. Check if Docker is installed
where docker >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Docker could not be found. Please install Docker before proceeding.
    call myenv\Scripts\deactivate.bat
    exit /b 1
)

echo Docker is installed.

REM 5. Pull GROBID Docker image
echo Pulling GROBID Docker image...
docker pull lfoppiano/grobid:0.7.2

REM 6. Run GROBID Docker container
docker ps -a -q -f name=grobid >nul
IF %ERRORLEVEL% EQU 0 (
    docker inspect -f "{{.State.Running}}" grobid | findstr /i "true" >nul
    IF %ERRORLEVEL% EQU 0 (
        echo GROBID container is already running.
    ) ELSE (
        echo Starting GROBID Docker container...
        docker start grobid
        echo GROBID is running on http://localhost:8070
    )
) ELSE (
    echo Running GROBID Docker container...
    docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.7.2
    echo GROBID is running on http://localhost:8070
)

REM 7. Run the Streamlit app
echo Starting the Streamlit app...
start cmd /k streamlit run app.py

REM 8. Deactivate the virtual environment when done
echo Deactivating virtual environment...
call myenv\Scripts\deactivate.bat

