import aiosqlite
from config import config

async def get_db():
    return await aiosqlite.connect(config.db)

async def create_table():
    db = await get_db()
    await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''') # question_index используется для сохранения индекса вопроса, на котором остановился пользователь.
    await db.execute('''CREATE TABLE IF NOT EXISTS score (user_id INTEGER PRIMARY KEY, user_score INTEGER)''')
    await db.commit()

# Получение индекса вопроса
async def get_quiz_index(user_id : int) -> int:
    db = await get_db()
    async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
        results = await cursor.fetchone()
        return results[0] if results else 0

# Обновление индекса        
async def update_quiz_index(user_id, index):
    db = await get_db()
    await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
    await db.commit()

# Получение количества правильных ответов
async def get_user_score(user_id):
    db = await get_db()
    async with db.execute('SELECT user_score FROM score WHERE user_id = (?)', (user_id, )) as cursor:
        results = await cursor.fetchone()
        return results[0] if results else 0
        
async def update_user_score(user_id, score):
    db = await get_db()
    await db.execute('INSERT OR REPLACE INTO score (user_id, user_score) VALUES (?, ?)', (user_id, score))
    await db.commit()