@echo off
echo Starting Steganography Tool Server...
echo.
echo The server will be accessible at:
echo - Local: http://localhost:5000
echo - Network: http://YOUR_IP_ADDRESS:5000
echo.
echo To find your IP address, run: ipconfig
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
pause 