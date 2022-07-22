import dramatiq
import psycopg2
from dramatiq.brokers.redis import RedisBroker
import subprocess
import os

connection = psycopg2.connect("postgresql://postgres:postgres@db:5432/video_db")
cursor = connection.cursor()


r = RedisBroker(url="redis://redis_dramatiq:6379")
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
        if float(result.stdout) > 600:
            cursor.execute(
                "UPDATE videos SET status = 'canceled : video length too long' WHERE id = %s",
                (video_id,),
            )
            connection.commit()
            subprocess.call(
                "rm uploads/{file_name}".format(file_name=data[0]), shell=False
            )
            return
        cursor.execute(
            "UPDATE videos SET status = 'done' WHERE id = %s",
            (video_id,),
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
                "UPDATE videos SET status = 'canceled : file size too large' WHERE id = %s",
                (video_id,),
            )
            connection.commit()
            subprocess.call(f"rm uploads/{data[0]}", shell=False)
            return

        check_video_length.send(video_id=video_id)
