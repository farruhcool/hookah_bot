import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("TOKEN"))

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))

admins = [
    os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")

db_host = ip

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{db_host}/{DATABASE}"

