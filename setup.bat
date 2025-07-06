@echo off
REM setup.bat - Initial project setup for Windows

echo ================================================
echo Trendyol Test Automation Framework Setup
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo Creating project structure...

REM Create directories
if not exist mobile mkdir mobile
if not exist mobile\base mkdir mobile\base
if not exist mobile\pages mkdir mobile\pages
if not exist mobile\tests mkdir mobile\tests
if not exist pages mkdir pages
if not exist tests mkdir tests
if not exist utils mkdir utils
if not exist reports mkdir reports
if not exist screenshots mkdir screenshots
if not exist logs mkdir logs
if not exist monitoring mkdir monitoring
if not exist monitoring\grafana mkdir monitoring\grafana
if not exist monitoring\grafana\dashboards mkdir monitoring\grafana\dashboards
if not exist monitoring\grafana\datasources mkdir monitoring\grafana\datasources

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Installing Appium globally...
npm install -g appium
npm install -g appium-doctor

echo Installing Appium drivers...
appium driver install uiautomator2

echo Creating batch scripts...

REM Create start_appium.bat
echo @echo off > start_appium.bat
echo echo Starting Appium Server... >> start_appium.bat
echo if not exist logs mkdir logs >> start_appium.bat
echo start "Appium Server" cmd /k "appium server --port 4723 --log logs\appium.log" >> start_appium.bat
echo timeout /t 5 >> start_appium.bat
echo echo Appium server started on port 4723 >> start_appium.bat
echo echo Press any key to close this window... >> start_appium.bat
echo pause >> start_appium.bat

REM Create stop_appium.bat
echo @echo off > stop_appium.bat
echo echo Stopping Appium Server... >> stop_appium.bat
echo taskkill /f /im node.exe /fi "WINDOWTITLE eq Appium Server*" 2^>nul >> stop_appium.bat
echo echo Appium server stopped >> stop_appium.bat
echo pause >> stop_appium.bat

REM Create start_emulator.bat
echo @echo off > start_emulator.bat
echo if "%%ANDROID_HOME%%"=="" ( >> start_emulator.bat
echo     echo ERROR: ANDROID_HOME is not set >> start_emulator.bat
echo     echo Please set ANDROID_HOME environment variable >> start_emulator.bat
echo     pause >> start_emulator.bat
echo     exit /b 1 >> start_emulator.bat
echo ^) >> start_emulator.bat
echo echo Starting Android Emulator... >> start_emulator.bat
echo echo Available AVDs: >> start_emulator.bat
echo %%ANDROID_HOME%%\emulator\emulator -list-avds >> start_emulator.bat
echo echo. >> start_emulator.bat
echo set /p avd_name="Enter AVD name (or press Enter for default): " >> start_emulator.bat
echo if "%%avd_name%%"=="" set avd_name=Pixel_4_API_29 >> start_emulator.bat
echo start "Android Emulator" %%ANDROID_HOME%%\emulator\emulator -avd %%avd_name%% -no-snapshot-load >> start_emulator.bat
echo echo Emulator starting... Please wait for it to fully boot. >> start_emulator.bat
echo pause >> start_emulator.bat

REM Create run_web_tests.bat
echo @echo off > run_web_tests.bat
echo call venv\Scripts\activate.bat >> run_web_tests.bat
echo echo Running Web Tests... >> run_web_tests.bat
echo python run_tests.py --web >> run_web_tests.bat
echo echo. >> run_web_tests.bat
echo echo Tests completed. Check reports folder for results. >> run_web_tests.bat
echo pause >> run_web_tests.bat

REM Create run_mobile_tests.bat
echo @echo off > run_mobile_tests.bat
echo call venv\Scripts\activate.bat >> run_mobile_tests.bat
echo echo Starting Mobile Test Environment... >> run_mobile_tests.bat
echo echo 1. Starting Appium server... >> run_mobile_tests.bat
echo call start_appium.bat >> run_mobile_tests.bat
echo timeout /t 10 >> run_mobile_tests.bat
echo echo 2. Running Mobile Tests... >> run_mobile_tests.bat
echo python run_tests.py --mobile >> run_mobile_tests.bat
echo echo. >> run_mobile_tests.bat
echo echo Tests completed. Check reports folder for results. >> run_mobile_tests.bat
echo pause >> run_mobile_tests.bat

REM Create run_all_tests.bat
echo @echo off > run_all_tests.bat
echo call venv\Scripts\activate.bat >> run_all_tests.bat
echo echo Running All Tests (Web + Mobile)... >> run_all_tests.bat
echo python run_tests.py >> run_all_tests.bat
echo echo. >> run_all_tests.bat
echo echo All tests completed. Check reports folder for results. >> run_all_tests.bat
echo pause >> run_all_tests.bat

REM Create cleanup.bat
echo @echo off > cleanup.bat
echo echo Cleaning up old reports and screenshots... >> cleanup.bat
echo call venv\Scripts\activate.bat >> cleanup.bat
echo python run_tests.py --cleanup >> cleanup.bat
echo echo Cleanup completed. >> cleanup.bat
echo pause >> cleanup.bat

REM Create check_environment.bat
echo @echo off > check_environment.bat
echo echo ================================================ >> check_environment.bat
echo echo Environment Check >> check_environment.bat
echo echo ================================================ >> check_environment.bat
echo echo. >> check_environment.bat
echo echo Python Version: >> check_environment.bat
echo python --version >> check_environment.bat
echo echo. >> check_environment.bat
echo echo Node.js Version: >> check_environment.bat
echo node --version >> check_environment.bat
echo echo. >> check_environment.bat
echo echo NPM Version: >> check_environment.bat
echo npm --version >> check_environment.bat
echo echo. >> check_environment.bat
echo echo Java Version: >> check_environment.bat
echo java -version >> check_environment.bat
echo echo. >> check_environment.bat
echo echo Android Home: >> check_environment.bat
echo echo %%ANDROID_HOME%% >> check_environment.bat
echo echo. >> check_environment.bat
echo echo Appium Doctor Check: >> check_environment.bat
echo appium-doctor --android >> check_environment.bat
echo echo. >> check_environment.bat
echo echo ADB Devices: >> check_environment.bat
echo adb devices >> check_environment.bat
echo echo. >> check_environment.bat
echo pause >> check_environment.bat

echo ================================================
echo Setup completed successfully!
echo ================================================
echo.
echo Available commands:
echo - run_web_tests.bat      : Run web automation tests
echo - run_mobile_tests.bat   : Run mobile automation tests
echo - run_all_tests.bat      : Run both web and mobile tests
echo - start_appium.bat       : Start Appium server
echo - stop_appium.bat        : Stop Appium server
echo - start_emulator.bat     : Start Android emulator
echo - check_environment.bat  : Check environment setup
echo - cleanup.bat            : Clean old reports
echo.
echo Next steps:
echo 1. Run check_environment.bat to verify setup
echo 2. Create Android emulator if needed
echo 3. Download Trendyol APK for mobile testing
echo 4. Run run_web_tests.bat to start testing
echo.
pause