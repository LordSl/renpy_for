import os

##----此处填写内容开始----

# 填入log路径和目标路径
sourcePath = "源文本/潮土油P3"
destPath = "输出/潮土油P3"
#是否要生成rpy文本 1.是 2.否
rpy_mode = 1
# 声音合成模式 0.不合成 1.合总合成 2.分段合成
audio_mode = 2
# 骰娘列表
diceGirls = ['小满']

##----此处填写内容结束----

f_log =  open(sourcePath+'/log_o.txt', mode = 'r', encoding='utf-8')
if not os.path.exists(destPath+"/audio"): os.makedirs(destPath+"/audio")

roles = []
orders = []
dialogues = []

#分段读取log，按人物切割
log_paras = f_log.readlines()
for i in range(len(log_paras)):
    try:
        if(log_paras[i][0]=='#'):
            continue
        name = log_paras[i][1:].split('>')[0]
        if (name not in roles):
            roles.append(name)
        orders.append(roles.index(name))
        dialogues.append(''.join(log_paras[i].split('>')[1:])[1:-1])
    except Error:
        print('format wrong in txt line',i+1)

dialogues_size = len(dialogues)
print(roles)

if(rpy_mode == 1):
    f_rpy = open(destPath + '/script.rpy', mode='w', encoding='utf-8')
    # 头文件请自行定义
    f_rpy.write('label start:\n')
    # 内容部分
    voice_num = 0
    for i in range(dialogues_size):
        # 开头
        if (orders[i]=='error'):
            print('error in',i)
            continue
        if (i == 0):
            f_rpy.write(
                '    show ' + roles[orders[i]] + '\n')
        # 需要更换立绘
        if (i != 0 and orders[i] != orders[i - 1]):
            f_rpy.write('    hide ' + roles[orders[i - 1]] + '\n\n')
            f_rpy.write('    show ' + roles[orders[i]] + '\n')
        if (roles[orders[i]] not in diceGirls):
            f_rpy.write('    voice \'../audio/' + str(voice_num) + '.mp3\'\n')
            voice_num += 1
        else:# 骰娘音效
            f_rpy.write('    voice \'../audio/骰娘的声音.mp3\'\n')
        f_rpy.write('    ' + roles[orders[i]]+ ' \'' + dialogues[i] + '\''+'\n')

    f_rpy.write('\n    return')

bad = ['。','，','？','！','.','（','）','/','"'] # 连续则停用字符
meme = ['，','。','.','...','......','？？？','？','！','！？','？！'] # 防止被误杀

def getWord(s):
    word = ''
    j = 0
    if(len(s)==1):
        return s
    while (j < len(s)):
        while (j < len(s) - 1 and dialogues[i][j] in bad and s[j + 1] in bad):
            j += 1
        if (s[j] in bad):
            if (0 < j < len(s) - 1):
                word += '|'
        else:
            word += s[j]
        j += 1
        # 去掉引起电流麦的空读
    return word

if (audio_mode == 1):
    # 朗读女txt，合总
    f_voice = open(destPath + '/audio/voice.txt', mode='w', encoding='utf-8')
    for i in range(dialogues_size):
        if (roles[orders[i]] not in diceGirls):
            word = dialogues[i]
            if (word not in meme):
                word = getWord(word)
            f_voice.write('[' + roles[orders[i]] + ']' + ' ' + word + '\n')

elif (audio_mode == 2):
    # 朗读女txt，分段
    voice_num = 0
    for i in range(dialogues_size):
        if (roles[orders[i]] not in diceGirls):
            audio_file_name = roles[orders[i]]
            if not os.path.exists(destPath + '/audio/' + audio_file_name): os.makedirs(
                destPath + '/audio/' + audio_file_name)
            f_voice = open(destPath + '/audio/' + audio_file_name + '/' + str(voice_num) + '.txt', mode='w',
                           encoding='utf-8')
            f_voice.write(dialogues[i]+'\n')
            voice_num += 1

print("over")
