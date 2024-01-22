ffmpeg -i output_final.mp4 -filter_complex "[0:v]setpts=0.8333*PTS[v];[0:a]atempo=1.2[a]" -map "[v]" -map "[a]" output_final_2.mp4
