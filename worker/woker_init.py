import dramatiq

from dramatiq.brokers.redis import RedisBroker

r = RedisBroker(url="redis://redis_dramatiq:6379")
dramatiq.set_broker(r)


@dramatiq.actor
def check_video_length(file_name, file_bytes_data: bytes):

    ...


@dramatiq.actor
def check_video_size(video_id: int):
    ...
