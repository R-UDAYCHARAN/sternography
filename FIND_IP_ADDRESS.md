# How to Find Your IP Address and Access from Mobile

## Step 1: Find Your IP Address

### On Windows:
1. **Open Command Prompt:**
   - Press `Windows + R`
   - Type `cmd` and press Enter

2. **Run the command:**
   ```bash
   ipconfig
   ```

3. **Look for your IP address:**
   ```
   Wireless LAN adapter Wi-Fi:
      IPv4 Address. . . . . . . . . . . : 192.168.1.100
   ```
   - Copy the IP address (e.g., `192.168.1.100`)

### On Mac:
1. **Open Terminal**
2. **Run the command:**
   ```bash
   ifconfig
   ```
3. **Look for your IP address:**
   ```
   inet 192.168.1.100 netmask 0xffffff00
   ```

## Step 2: Start Your Flask Server

1. **Open Command Prompt/Terminal**
2. **Navigate to your project folder:**
   ```bash
   cd C:\path\to\your\project
   ```
3. **Start the server:**
   ```bash
   python app.py
   ```
4. **You should see:**
   ```
   Running on http://0.0.0.0:5000
   ```

## Step 3: Access from Mobile Device

### Prerequisites:
- ✅ Your computer is running the Flask server
- ✅ Your mobile device is connected to the **same WiFi network**
- ✅ You have your computer's IP address

### Steps:
1. **On your mobile device:**
   - Open any web browser (Chrome, Safari, Firefox, etc.)

2. **Enter the URL:**
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   - Replace `YOUR_IP_ADDRESS` with your actual IP
   - Example: `http://192.168.1.100:5000`

3. **Press Enter or Go**
   - Your steganography tool should load on your mobile device!

## Example Workflow:

### On Your Computer:
```bash
# 1. Find your IP
ipconfig

# 2. Start the server
python app.py
```

### On Your Mobile:
1. Connect to same WiFi
2. Open browser
3. Go to: `http://192.168.1.100:5000`
4. Use your steganography tool!

## Troubleshooting:

### Problem: "This site can't be reached"
**Solutions:**
1. Make sure both devices are on the same WiFi
2. Check that your Flask server is running
3. Verify the IP address is correct
4. Try turning off mobile data (use WiFi only)

### Problem: "Connection refused"
**Solutions:**
1. Make sure Flask is running on port 5000
2. Check Windows Firewall settings
3. Try a different port in `app.py`

### Problem: IP address changes
**Solution:** 
- IP addresses can change when you reconnect to WiFi
- Run `ipconfig` again to get the new IP

## Security Note:
- This only works on your local network
- Only people on the same WiFi can access it
- Your computer is not exposed to the internet
- This is safe for sharing with friends/family on the same network

## Benefits:
- ✅ No internet required (works offline)
- ✅ Fast and secure
- ✅ No external services needed
- ✅ Works on any device on the same network
- ✅ Free and unlimited

Your steganography tool will now be accessible from any mobile device on your WiFi network! 