import asyncio
from highrise import BaseBot
from highrise.api.auth import AuthToken
from highrise.models import User, Message
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MJSystemBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.room_id = "679053c7bc45b5bbdd63bcd4"
        self.moderator = "Sigma_Boy__"
        self.emote_loop_active = False
        self.current_emote_index = 0
        self.emotes = ["relaxing", "ponder", "smooch", "laidback", "ghostfloat", "cozynap", "posh"]
        self.music_queue = []
        self.wallet = {}

    async def on_start(self) -> None:
        logger.info(f"✅ Bot started")
        await self.chat("🤖 MJ-SYSTEM Bot online!")

    async def on_message(self, user: User, message: Message) -> None:
        msg = message.content.strip().lower()
        
        if msg == "1":
            self.emote_loop_active = True
            self.current_emote_index = 0
            await self.chat("🎭 Emote loop started!")
            await self.start_emote_loop()
        
        elif msg == "0":
            self.emote_loop_active = False
            await self.chat("⏹️ Emote loop stopped")
        
        elif msg.startswith("!play"):
            song = msg.replace("!play", "").strip()
            if song:
                self.music_queue.append(song)
                await self.chat(f"🎵 Added: {song}")
        
        elif msg == "!queue":
            if self.music_queue:
                queue_str = "\n".join([f"{i+1}. {s}" for i, s in enumerate(self.music_queue[:10])])
                await self.chat(f"🎶 Queue:\n{queue_str}")
            else:
                await self.chat("Queue is empty!")
        
        elif msg == "!skip":
            if self.music_queue:
                self.music_queue.pop(0)
                await self.chat("⏭️ Skipped!")
        
        elif msg.startswith("!tip"):
            parts = msg.split()
            if len(parts) >= 2:
                try:
                    amount = int(parts[1])
                    username = user.username
                    if username not in self.wallet:
                        self.wallet[username] = 0
                    self.wallet[username] += amount
                    await self.chat(f"💰 {username} tipped {amount}!")
                except:
                    pass
        
        elif msg == "!help":
            await self.chat("🤖 Commands: !play [song] | !queue | !skip | !tip [amount] | 1=start | 0=stop")

    async def start_emote_loop(self) -> None:
        while self.emote_loop_active:
            try:
                emote = self.emotes[self.current_emote_index]
                await self.emote(emote)
                self.current_emote_index = (self.current_emote_index + 1) % len(self.emotes)
                await asyncio.sleep(8)
            except Exception as e:
                logger.error(f"Error: {e}")
                break

async def main():
    token = os.getenv("HIGHRISE_TOKEN", "9fb100cb59582676e411e87568273d94310fd815398cd0c479672554ce0ba16d")
    bot = MJSystemBot()
    await bot.run(AuthToken(token))

if __name__ == "__main__":
    asyncio.run(main())
