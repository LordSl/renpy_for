from pydub import AudioSegment
from pydub.utils import mediainfo

# 请先使用朗读女将rpy_make生成的合总txt转换成mp3，并生成lrc文件
sourcePath = '输出/潮土油P3/audio'
destPath = '输出/潮土油P3/audio'

#获取时间分割位点
f_lyr =  open(sourcePath+'/voice.lrc', mode = 'r', encoding='ANSI')
lyr = f_lyr.readlines()
time_split = [0]
for i in range(1,len(lyr)-1):
    if lyr[i][-2:-1]!='|':
        line = lyr[i+1]
        tmp = len(line.split(']')[0])-9
        min = line[1:tmp+3]
        s = line[tmp+4:tmp+6]
        ls = line[tmp+7:tmp+9]
        # 单位是ms
        # 朗读女提供的歌词文件时间分割位点不准
        time_stamp = 10*int(ls) + 1000*int(s) + 60*1000*int(min)
        time_split.append(time_stamp)

print(mediainfo(sourcePath+'/voice.mp3')['duration'])
# 读取mp3，切割输出
mp3 = AudioSegment.from_mp3(sourcePath+'/voice.mp3')
for i in range(len(time_split)-1):
# for i in range(10):
    print(i)
    time_begin = time_split[i]
    time_over = time_split[i+1]
    # 已解决，是分句空读所致
    mp3[time_begin:time_over].export(destPath+'/'+str(i)+'.mp3',format='mp3')

# for i in range(0,100):
#     print(i)
#     time_begin = time_split[i]
#     time_over = time_split[i+1]
#     mp3[time_begin:time_over].export(destPath+'/'+str(i)+'.mp3',format='mp3')
#
# for i in range(700,800):
#     print(i)
#     time_begin = time_split[i]
#     time_over = time_split[i+1]
#     mp3[time_begin:time_over].export(destPath+'/'+str(i)+'.mp3',format='mp3')
#
# for i in range(1400,1500):
#     print(i)
#     time_begin = time_split[i]
#     time_over = time_split[i+1]
#     mp3[time_begin:time_over].export(destPath+'/'+str(i)+'.mp3',format='mp3')

print('over')