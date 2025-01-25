import psycopg2
from pymongo import MongoClient
import redis
import time

# PostgreSQL
def write_to_postgresql():
    conn = psycopg2.connect("dbname=mydb user=user password=password host=postgres_container")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, data TEXT);")
    cur.execute("INSERT INTO test (data) VALUES ('Hello Abdullah!');")
    conn.commit()
    # Sorgulama ve yazılan veriyi al
    cur.execute("SELECT data FROM test ORDER BY id DESC LIMIT 1;")
    result = cur.fetchone()
    print("PostgreSQL:", result[0])  # Veriyi konsola yazdır
    cur.close()
    conn.close()

# Mongo
def write_to_mongo():
    client = MongoClient('mongo_container', 27017)
    db = client.test_db
    db.test_collection.insert_one({'message': 'Hello, Abdullah!'})
    message = db.test_collection.find_one({'message': 'Hello, Abdullah!'})
    print('MongoDB:', message['message'])

# Redis
def write_to_redis():
    r = redis.Redis(host='redis_container', port=6379)
    r.set('message', 'Hello, Abdullah!')
    print('Redis:', r.get('message').decode('utf-8'))


if __name__ == "__main__":
    print("WAITING")
    time.sleep(30)
    print("WRITING DATA")
    write_to_postgresql()
    write_to_mongo()
    write_to_redis()

