from enum import Enum


# Moderation Media
# That is tracks particular forms of media ie mediums
# 
# Definition
# medium: concrete data that conveys content. 
#   In other words, matter that a subject processes 
#   into information ie content. 
#   text, img, video, audio, caption, url 
class MediaTypeEnum(str, Enum):
    IMG = "image"
    VIDEO = "video"
    TEXT = "comment"