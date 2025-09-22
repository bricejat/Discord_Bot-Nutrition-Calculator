
import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import asyncio
import threading
import json
import sqlite3
from datetime import datetime

DISCORD_BOT_TOKEN = YOUR BOT ID TOKEN
NUTRITION_CHANNEL_ID = YOUR CHANNELID
YOUR_DISCORD_USER_ID = YOUR PROFILE ID

app = Flask(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def init_database():
    conn = sqlite3.connect('nutrition.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT,
            calories INTEGER,
            timestamp TEXT,
            date TEXT
         )
    ''')
    conn.commit()
    conn.close()

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is connected and ready!')
    print(f'📱 Webhook server running on port 5000')
    init_database()

    ## WEBHOOKS endpoint for IOS
@app.route('/nutrition', methods=['POST'])
def receieve__nutrition():
    """Recieve nutrition data from iOS Shortcut"""
    try:
        data = request.json
        print(f"📱 Received: {data}")

        food_name = data.get('food_name', 'Unknown Food')
        calories = int(data.get('calories', 0))

        conn = sqlite3.connect('nutrition.db')
        cursor = conn.cursor()

        now = datetime.now()
        cursor.execute('''
            INSERT INTO food_logs (food_name, calories, timestamp, date)
            VALUES (?, ?, ?, ?)
        ''', (food_name, calories, now.isoformat(), now.strftime('%Y-%m-%d')))

        conn.commit()
        conn.close()

        ## Send to discord (Run Async)
        asyncio.create_task(send_to_discord(food_name, calories))

        return jsonify({
            "status": "success",
            "message": f"Logged {food_name} with {calories} calories"
        }), 200
    
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400
    
async def send_to_discord(food_name, calories):
    """Send the logged food to your Discord Channel"""
    try:
        await bot.wait_until_ready()

        channel = bot.get_channel(INSERT CHANNEL ID)

        if not channel:
            print(f"❌ Could not find channel with ID {CHANNEL ID HERE}")
            return
        
        # Creating a embed message code
        embed = discord.Embed(
            title="Yummers Food Logged LOL",
            color=0x00ff00,
            timestamp=datetime.now()
        )

        embed.add_field(name="📝 Food", value=food_name, inline=False)
        embed.add_field(name="🔥 Calories", value=f"{calories}", inline=True)

        embed.set_footer(text="Logged via iOS Shortcut")

    #Sends a message
        await channel.send(embed=embed)
        print(f"❌ Error sending to Discord: {e}")

    except Exception as e:
         print(f"❌ Error sending to Discord: {e}")

# Commands to show theres been no data and total data added
@bot.command(name='stats')
async def show_stats(ctx):
    """Show your daily nutrion stats"""
    try: 
            today = datetime.now().strftime('%Y-%m-%d')

            conn = sqlite3.connect('nutrition.db')
            cursor= conn.cursor()
        #total
            cursor.execute('''
                SELECT SUM(calories), COUNT(*)
                FROM food_logs WHERE date = ?
            ''', (today,))

            result = cursor.fetchone()

            if not result or result[0] is None:
                await ctx.send("📊 No food logged today yet!")
                return
            
            total_calories, item_count = result

            cursor.execute('''
                SELECT food_name, calories FROM food_logs
                WHERE date = ? ORDER BY timestamps DESC LIMIT 5
            ''', (today,))

            recent_foods = cursor.fetechall()
            conn.close()

            embed = discord.Embed(
                 title="📊 Today's Nutrition Stats",
                color=0x3498db,
                timestamp=datetime.now()
            )
            embed.add_field(name="🔥 Total Calories", value=f"{int(total_calories)}", inline=True)
            embed.add_field(name="📝 Items Logged", value=f"{item_count}", inline=True)

            if recent_foods:
                 recent_text = "\n".join([f"• {food}: {cal} cal" for food, cal in recent_foods])
                 embed.add_field(name="Recent Foods", value=recent_text, inline=False)

            await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Error fetching stats: {e}")

@bot.command(name='log')
async def manual_log(ctx, *, food_info):
    """Manually log food: !log Pizza 300 Calories"""
    try:
        parts = food_info.split()
        food_name = []
        calories = 0

        i = 0
        while i < len(parts):
            part = parts[i].lower()

            if 'cal' in part:  # calories
                    calories = int(''.join(filter(str.isdigit, parts[i-1] if i > 0 else parts[i])))
            elif not any(nutrient in part for nutrient in ['cal']):
                if not part.replace('.', '').isdigit():  # If it's not a number, it's part of food name
                        food_name.append(parts[i])

            i += 1
        
        food_name = ' '.join(food_name) if food_name else 'Manual Entry'

        conn = sqlite3.connect('nutrition.db')
        cursor = conn.cursor()
        
        now = datetime.now()
        cursor.execute('''
            INSERT INTO food_logs (food_name, calories, timestamp, date)
            VALUES (?, ?, ?, ?)
        ''', (food_name, calories, now.isoformat(), now.strftime('%Y-%m-%d')))
        
        conn.commit()
        conn.close()

        await send_to_discord(food_name,calories)
        await ctx.send(f"✅ Logged {food_name} with {calories} calories")

    except Exception as e:
        await ctx.send(f"❌ Error logging food: {e}")
        await ctx.send("Usage: `!log pizza 300 calories`")

def run_flask():
    """Run the Flask webhook server"""
    app.run(host='0.0.0.0', port=5000, debug=False)

def run_bot():
    """Run the Discord bot"""
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    print("🚀 Starting Nutrition Bot...")

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print("📱 Webhook server starting on port 5000...")
    print("🤖 Discord bot starting...")

    run_bot()


    
