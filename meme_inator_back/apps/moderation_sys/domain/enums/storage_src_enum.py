from enum import Enum

class StorageLocationEnum(str, Enum):
    """
    Conveys WHERE content, usually the BLOB, is stored within infrastructure layer.

    Location may depend on lifecycle BLOB. Early on, BLOB might actually be stored in a HTTP request.

    Where this enum is used changes which on of the enums will be used. 
        ContentToModerate, which is inside ModerationRequest, contains content_src attribute, REQUEST_BODY value maybe used to indicate BLOB is stored in HTTP Request. 

        Enum being used in the backend converys if BLOB is stored in meme-inator server OR in external storage provider (like AWS S3)
    """
    LOCAL_DB = "local_db"              # fetch from local database using content_id + retrieval_key
    EXTERNAL_STORAGE = "external_storage"  # fetch from S3/blob storage