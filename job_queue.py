import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "rag_jobs"

def push_job(job: dict):
    """Push a new ingestion job to the queue"""
    r.rpush(QUEUE_NAME, json.dumps(job))
    print(f"📥 Job pushed to queue: {job}")

def pop_job():
    """Blocking pop — waits until a job is available"""
    _, data = r.blpop(QUEUE_NAME)
    return json.loads(data)