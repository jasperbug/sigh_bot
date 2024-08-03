import os
from twitchio.ext import commands
import time
import json

# 用於存儲用戶簽到記錄的字典
user_checkins = {}

# 從文件加載簽到數據
def load_checkins():
    global user_checkins
    if os.path.exists('checkins.json'):
        with open('checkins.json', 'r') as f:
            user_checkins = json.load(f)

# 保存簽到數據到文件
def save_checkins():
    with open('checkins.json', 'w') as f:
        json.dump(user_checkins, f)

class Bot(commands.Bot):

    def __init__(self):
        # 請替換為您的實際信息
        super().__init__(token='你的OAuth', prefix='!', initial_channels=['你的圖奇頻道id'])
        load_checkins()

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command(name='簽到')
    async def check_in(self, ctx):
        username = ctx.author.name
        current_time = time.time()
        
        if username in user_checkins:
            last_checkin_time = user_checkins[username]['last_checkin']
            # 檢查是否在同一次實況中（假設一次實況最長12小時）
            if current_time - last_checkin_time < 12 * 3600:
                await ctx.send(f"@{username}，你已經在這次實況中簽到過了。總共簽到次數：{user_checkins[username]['count']}次")
                return
        
        # 更新簽到記錄
        if username in user_checkins:
            user_checkins[username]['count'] += 1
        else:
            user_checkins[username] = {'count': 1}
        
        user_checkins[username]['last_checkin'] = current_time
        save_checkins()
        await ctx.send(f"@{username} 簽到成功！總共簽到次數：{user_checkins[username]['count']}次")

    @commands.command(name='排行榜')
    async def leaderboard(self, ctx):
        sorted_users = sorted(user_checkins.items(), key=lambda x: x[1]['count'], reverse=True)
        top_5 = sorted_users[:5]
        leaderboard_text = "簽到排行榜 Top 5:\n" + "\n".join([f"{i+1}. {user}: {data['count']}次" for i, (user, data) in enumerate(top_5)])
        await ctx.send(leaderboard_text)

bot = Bot()
bot.run()
