class QueueConnectionError(Exception):
    pass


class MessageProcessingError(Exception):
    pass


class DataConversionError(Exception):
    pass

class ConfigError(Exception):
    pass


class StorageError(Exception):
    pass
