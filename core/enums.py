import enum


class StatusEnum(enum.Enum):
    on_queue = "on_queue"
    processing = "processing"
    done = "done"
    canceled = "canceled"
