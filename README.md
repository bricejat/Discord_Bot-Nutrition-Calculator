# Discord_Bot-Nutrition-Calculator
This is a discord bot that lets you use "iPhone Shortcut app" to send data to a discord bot into a server of your owns. 

<img width="871" height="511" alt="discord sc" src="https://github.com/user-attachments/assets/354edc9e-39cb-40c8-9081-dfecf8eb5256" />

## USAGE
- Use your iOS shortcut to log food
- Type !stats in Discord to see daily summary
- Type !log pizza 300 calories to manually log food


SETUP INSTRUCTIONS IF YOU WANT TO DO THIS:

1. INSTALL REQUIREMENTS:
   pip install discord.py flask

2. GET DISCORD BOT TOKEN:
   - Go to https://discord.com/developers/applications
   - Create New Application
   - Go to Bot section → Add Bot
   - Copy the Token

3. GET CHANNEL ID:
   - In Discord: Right-click your Discord channel → Copy ID (You need Developer Mode enabled in Discord settings)
     
5. RUN THE BOT:
   python nutrition_bot.py

6. UPDATE YOUR iOS SHORTCUT:
   - URL: http://YOUR_SERVER_IP:5000/nutrition
   - Method: POST
   - Headers: Content-Type: application/json
   - Body: 
   {
     "food_name": "Pizza",
     "calories": 300,
   }

7. INVITE BOT TO YOUR SERVER:
   - Go to OAuth2 → URL Generator in Discord Developer Portal
   - Select 'bot' scope and 'Send Messages' permission
   - Use generated URL to invite bot to your server

 WHAT IS THE USAGE OF THIS BOT?:
- Use your iOS shortcut to log food
- Type !stats in Discord to see daily summary
- Type !log pizza 300 calories to manually log food
"""
