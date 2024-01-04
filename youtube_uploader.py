from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo


def upload_to_youtube(file_path, title):
    # loggin into the channel
    channel = Channel()
    channel.login("client_secret.json", "credentials.storage")

    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path=file_path)

    # setting snippet
    video.set_title(title + " | #horrorstories #spookytales #scarytales")
    video.set_description("#scary #creepy #creepytales #halloween #hauntedtales #horrorshorts #horrorstories" +
                          " #mysteryshorts #paranormaltales #scarystories")
    # video.set_tags(["this", "tag"])
    video.set_category("people")
    video.set_default_language("en-US")

    # setting status
    video.set_embeddable(True)
    video.set_license("youtube")
    video.set_privacy_status("public")
    # video.set_publish_at("2021-10-31T12:00:00Z")
    # video.set_public_stats_viewable(True)
    video = channel.upload_video(video)
    print(video.id)


# upload_to_youtube("Outputs/2024_01_02_18_04_05/output_final.mp4", "Turbulence Above the Abyss")
