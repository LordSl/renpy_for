import os
from aip import AipSpeech

##----此处填写内容开始----

# 填入log路径和目标路径
sourcePath = "源文本/潮土油P0"
destPath = "输出/潮土油P0"
# 人物名称列表，为了便于处理，请将骰娘也加入其中
roles = ['墨刺','木刀','村上','镇长','路人甲','店长','瓦拉','小满']
# 骰娘列表
diceGirls = ['小满']
roles_param = [
    {'原名':'墨刺','显示名':'墨刺'},
    {'原名':'木刀','显示名':'木刀'},
    {'原名':'村上','显示名':'村上'},
    {'原名':'镇长','显示名':'镇长'},
    {'原名':'路人甲','显示名':'路人甲'},
    {'原名':'店长','显示名':'店长'},
    {'原名':'瓦拉','显示名':'瓦拉'},
    {'原名': '小满', '显示名': '小满'},
]

f_log =  open(sourcePath+'/log_o.txt', mode = 'r', encoding='utf-8')
if not os.path.exists(destPath+"/audio"): os.makedirs(destPath+"/audio")

##----此处填写内容结束----

#台词顺序-角色表
orders = []

#分段读取log，按人物切割
log_paras = f_log.readlines()
for i in range(len(log_paras)):
    try:
        if (log_paras[i].split('>')[1] == '\n'):
            print('出现空行，空行的前一行内容是' + log_paras[i - 1])
    except IndexError:
        print(i)
    name = log_paras[i][1:].split('>')[0]
    for j in range(len(roles)):
        if(roles[j]==name):
            orders.append(j)
            break
        if(j==len(roles)-1):
            orders.append('error')

if_rpy = int(input('是否要生成rpy文本\n1.是\n2.否\n'))
if(if_rpy == 1):
    f_rpy = open(destPath + '/script.rpy', mode='w', encoding='utf-8')
    # 头文件请自行定义
    f_rpy.write('label start:\n')
    # f_rpy.write('    scene ' + bg_param['背景名'].split('.')[0] + '\n')
    # 内容部分
    voice_num = 0
    for i in range(len(orders)):
        # 开头
        if (i == 0):
            f_rpy.write(
                '    show ' + roles_param[orders[i]]['显示名'] + '\n')
        # 需要更换立绘
        if (i != 0 and orders[i] != orders[i - 1]):
            f_rpy.write('    hide ' + roles_param[orders[i - 1]]['显示名'] + '\n\n')
            f_rpy.write('    show ' + roles_param[orders[i]]['显示名'] + '\n')
        if (orders[i] < len(roles) - len(diceGirls)):
            f_rpy.write('    voice \'../audio/' + str(voice_num) + '.mp3\'\n')
            voice_num += 1
        else:# 骰娘音效
            f_rpy.write('    voice \'../audio/骰娘的声音.mp3\'\n')
        f_rpy.write('    ' + roles_param[orders[i]]['显示名'] + ' \'' + log_paras[i][1:].split('>')[1][1:-1] + '\'\n')

    f_rpy.write('\n    return')

if_audio = int(input('是否要生成声音合成文本\n1.是\n2.否\n'))

bad = ['。','，','？','！','.','（','）','/','"'] # 停用词

if(if_audio==1):
    audio_mode = int(input('请选择声音合成模式\n1.合总合成\n2.分段合成\n'))
    if (audio_mode == 1):
        # 朗读女txt，合总
        f_voice = open(destPath + '/audio/log_o.txt', mode='w', encoding='utf-8')
        # f_voice.write('<\_@TTS\_/>\n')
        # for j in range(len(roles_voice_param)-len(diceGirls)):
        #     f_voice.write('<_/1>'+roles_voice_param[j]['原名']+'<_/2>'+roles_voice_param[j]['发音人']+'<_/3>'+str(roles_voice_param[j]['音量'])+'<_/4>'+str(roles_voice_param[j]['语速'])+'<_/5>'+str(roles_voice_param[j]['语调'])+'<_/6></++/>\n')
        # f_voice.write('<\_@TTS\_/>')
        for i in range(len(log_paras)):
            if (orders[i] < len(roles) - len(diceGirls)):
                while(log_paras[i][-2:-1] in bad):
                    log_paras[i] = log_paras[i][:-2] + '\n' # 去掉引起电流麦的空读
                f_voice.write('[' + log_paras[i].split('>')[0][1:] + ']' + log_paras[i].split('>')[1][1:-1] + '|\n')  #为了使歌词顺利分隔，此处加入无实际意义的|
    elif (audio_mode == 2):
        # 朗读女txt，分段
        voice_num = 0
        for i in range(len(log_paras)):
            if (orders[i] < len(roles) - len(diceGirls)):
                if not os.path.exists(destPath + '/audio/' + str(orders[i])): os.makedirs(destPath + '/audio/' + str(orders[i]))
                f_voice = open(destPath + '/audio/' + str(orders[i]) + '/' + str(voice_num) + '.txt', mode='w',encoding='utf-8')
                f_voice.write(log_paras[i][1:].split('>')[1][1:])
                voice_num += 1
    else:
        print('wrong input')

print("over")
