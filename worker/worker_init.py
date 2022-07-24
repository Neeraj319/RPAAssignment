import dramatiq
import psycopg2
from dramatiq.brokers.redis import RedisBroker
import subprocess
import os

connection = psycopg2.connect(os.environ.get("DB_URL"))
cursor = connection.cursor()


r = RedisBroker(url=os.environ.get("REDIS_URL"))
dramatiq.set_broker(r)


@dramatiq.actor
def check_video_length(video_id: int):
    cursor.execute("SELECT url FROM videos WHERE id = %s", (video_id,))
    data = cursor.fetchone()
    if data:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                f"uploads/{data[0]}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        length = float(result.stdout)
        if length > 600:
            cursor.execute(
                "UPDATE videos SET status = 'canceled', remarks = 'video length more than 10 minutes' WHERE id = %s",
                (video_id,),
            )
            connection.commit()
            os.remove(f"uploads/{data[0]}")
            return
        cursor.execute(
            "UPDATE videos SET status = 'done', remarks = 'checks completed', length = %s WHERE id = %s",
            (length, video_id),
        )
        connection.commit()
    else:
        print(data, "video not available")


@dramatiq.actor
def check_video_size(video_id: int):
    cursor.execute("SELECT url FROM videos WHERE id = %s", (video_id,))
    data = cursor.fetchone()
    if data:
        cursor.execute(
            "UPDATE videos SET status = 'processing' WHERE id = %s", (video_id,)
        )
        connection.commit()
        file_name = data[0]
        file_bytes_data = os.stat(f"uploads/{file_name}").st_size
        if file_bytes_data > 1073741824:
            cursor.execute(
                "UPDATE videos SET status = 'canceled', remarks = 'file size greater than 1 GB' WHERE id = %s",
                (video_id,),
            )
            connection.commit()
            os.remove(f"uploads/{file_name}")
            return
        cursor.execute(
            "UPDATE videos SET size = %s WHERE id = %s",
            (file_bytes_data, video_id),
        )
        connection.commit()
        check_video_length.send(video_id=video_id)
