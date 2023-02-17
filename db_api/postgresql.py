from typing import Union

import asyncpg
from asyncpg import Pool, Connection

import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def close(self):
        await self.pool.close()

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_table_drones(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Drones (
        peer_id BIGINT PRIMARY KEY,
        id SERIAL,
        username VARCHAR(255) NOT NULL,
        last_activity INT DEFAULT 0, 
        status VARCHAR(255) DEFAULT 'training',
        work_experience INT DEFAULT 0,
        fire_balance BIGINT DEFAULT 0,
        chung_balance BIGINT DEFAULT 0,
        bonus_day SMALLINT DEFAULT 0,
        bonus_time INT DEFAULT 0,
        body SMALLINT DEFAULT 3,
        dirt SMALLINT DEFAULT 1,
        face SMALLINT DEFAULT 2,
        room_lvl SMALLINT DEFAULT 1,
        hall SMALLINT DEFAULT 0,
        kitchen SMALLINT DEFAULT 0,
        bathroom SMALLINT DEFAULT 0,
        bedroom SMALLINT DEFAULT 0,
        current_clothes SMALLINT DEFAULT 1,
        clothes SMALLINT[] DEFAULT '{1}',
        health REAL DEFAULT 1000,
        max_health SMALLINT DEFAULT 100,
        happiness REAL DEFAULT 100,
        time_draw INT DEFAULT 0,
        time_read INT DEFAULT 0,
        max_happiness SMALLINT DEFAULT 100,
        satiety REAL DEFAULT 100,
        time_ration INT DEFAULT 0,
        reserve_satiety INT DEFAULT 0,
        max_satiety SMALLINT DEFAULT 100,
        hygiene REAL DEFAULT 100,
        time_shower INT DEFAULT 0,
        time_toilet INT DEFAULT 0,
        max_hygiene SMALLINT DEFAULT 100,
        energy REAL DEFAULT 100,
        time_sleep INT DEFAULT 0,
        time_rest INT DEFAULT 0,
        max_energy SMALLINT DEFAULT 100
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        peer_id BIGINT PRIMARY KEY
        );
        """
        await self.execute(sql, execute=True)

    async def check_user(self, peer_id):
        sql = "SELECT true FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)
