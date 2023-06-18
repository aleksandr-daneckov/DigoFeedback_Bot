from environs import Env
import os

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

IP = env.str("DB_HOST")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")



admins = [
    5986362309
]

channels = [-1001910291225]



banned_users = [123421342, 432412341]