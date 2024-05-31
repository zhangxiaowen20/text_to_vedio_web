
import os
# 配置IMAGEMAGICK_BINARY环境变量
os.environ["IMAGEMAGICK_BINARY"] = r"E:\imagemagick\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips,TextClip, CompositeVideoClip
import numpy as np
import csv
import textwrap


def flFunc(gf, t):  # 变换主函数
    return frameScroll(gf(t), 2)  # 一帧往前滚动2行


def frameScroll(frame, x):  # 实现帧数据环绕滚动x行
    global framePos, clipHeight

    moveCount = framePos + x  # 本次移动行数在前一次行数基础上加x行
    if moveCount > clipHeight:  # 环绕判断处理，其实用moveCount %= clipHeight语句更简洁效果相同，但取余的运算效率低一些
        moveCount -= clipHeight
    framePos = moveCount  # 记录本次移动的行数
    remainFrame = frame[:moveCount]  # 取前moveCount-1行
    exceedFrame = frame[moveCount:]  # 取后面剩余行

    return np.vstack((exceedFrame, remainFrame))  # 将两部分数据叠加实现环绕效果，返回作为变换后的帧



def merge_vedio(image_dir_path,audio_dir_path,word_file_path):


    # 将文件名按照顺序排列
    image_files = sorted(os.listdir(image_dir_path))
    audio_files = sorted(os.listdir(audio_dir_path))
    print(image_files)
    clips = []

    #字幕列表
    zimu=[]
    with open(word_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            zimu.append(row[0])
            print(row[0])  # 打印每一行的文本

    # 图片和音频的持续时间
    duration = 5  # 您可以根据需要调整此值
    speed =10
    size =700
    for i in range(len(image_files)):
        image_path = os.path.join(image_dir_path, image_files[i])
        audio_path = os.path.join(audio_dir_path, audio_files[i])
        img_clip = ImageSequenceClip([image_path], duration)
        audio_clip = AudioFileClip(audio_path)

        # 根据音频的持续时间调整图片的持续时间
        fl = lambda gf, t: gf(t)[int(speed * t):int(speed * t) + size,:]
        # 如果你想设置滚动屏幕可以尝试下面的代码
        # img_clip = img_clip.fl(lambda gf, t: gf(t)[int(50*t):int(50*t) + 360, :], apply_to='mask').set_duration(audio_clip.duration)
        img_clip = img_clip.set_position(('center', 'center')).fl(fl,apply_to=['mask']).set_duration(audio_clip.duration)
        # img_clip = img_clip.fl(flFunc, apply_to='mask').set_duration(
        #     audio_clip.duration)

        print(zimu[i])
        # 添加字幕
        wrapped_text = textwrap.fill(zimu[i], width=25)+"\n"+"\n"  # 将文本分割成多行，每行最多10个字符
        txt_clip = TextClip(wrapped_text, fontsize=40, color='white',font="KaiTi")
        txt_clip = txt_clip.set_duration(audio_clip.duration).set_position(('bottom'))
        clip = CompositeVideoClip([img_clip, txt_clip])
        # 将音频添加到图片剪辑中
        clip = clip.set_audio(audio_clip)


        clips.append(clip)

    # 将所有剪辑合并成一个视频
    final_clip = concatenate_videoclips(clips)
    new_parent = image_dir_path.replace("data_image","data_vedio").split("story")[0]
    # 导出视频
    new_path = image_dir_path.replace("data_image","data_vedio")
    final_clip.write_videofile(new_path+".mp4", fps=24,audio_codec="aac")  # 可以根据需要调整fps值
    return new_path+".mp4"

if __name__ == '__main__':
    merge_vedio("data/data_image/长达700","data/data_audio/长达700","data/data_split/长达700.csv")


