from pydub import AudioSegment

# 请先使用朗读女将rpy_make生成的合总txt转换成mp3，并生成lrc文件
sourcePath = '输出/replay1/audio'
destPath = '输出/replay1/audio'
# sourcePath = '输出/test'
# destPath = '输出/test'

#获取时间分割位点
f_lyr =  open(sourcePath+'/log.lrc', mode = 'r', encoding='ANSI')
lyr = f_lyr.readlines()
time_split = [0]
for i in range(1,len(lyr)):
    if lyr[i][-3:-2]=='|' or lyr[i].split(']')[1]=='|\n':
        line = lyr[i+1]
        tmp = len(line.split(']')[0])-9
        min = line[1:tmp+3]
        s = line[tmp+4:tmp+6]
        ls = line[tmp+7:tmp+9]
        # 单位是ms
        time_stamp = 10*(int(ls) + 100*int(s) + 60*100*int(min))
        time_split.append(time_stamp-300)

# 读取mp3，切割输出
mp3 = AudioSegment.from_mp3(sourcePath+'\log.mp3')
for i in range(len(time_split)-1):
# for i in range(10):
    print(i)
    time_begin = time_split[i]
    time_over = time_split[i+1]
    # # 不知为何朗读女合成大段语音时会有电流麦，为规避此现象，请尽量避免使用微软的几位发音人
    # 已解决，是分句空读所致
    mp3[time_begin:time_over].export(destPath+'/'+str(i)+'.mp3',format='mp3')

print('over')