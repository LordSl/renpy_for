import os
from aip import AipSpeech

##----此处填写内容开始----

# 填入log路径和目标路径
sourcePath = "源文本/replay1"
destPath = "输出/replay1"
# 人物名称列表，为了便于处理，请将骰娘也加入其中
roles = ['墨刺','木刀','{指定唯一神}满大人']
# 骰娘列表
diceGirls = ['{指定唯一神}满大人']
roles_param = [
    {'原名':'墨刺','显示名':'KP','头像名':'kp.jfif','长':500,'宽':500,'位置':'left'},
    {'原名':'木刀','显示名':'PL','头像名':'pl.jfif','长':500,'宽':500,'位置':'right'},
    {'原名':'{指定唯一神}满大人','显示名':'DiceGirl','头像名':'kp.jfif','长':500,'宽':500,'位置':'left'}
]

bg_param = {'背景名':'bg c.png','长':1360*1.5,'宽':768*1.5}

roles_voice_param =[
    {'显示名':'KP','发音人':'Microsoft Kangkang Mobile - Chinese (Simplified, PRC)','音量':100,'语速':5,'语调':0},
    {'显示名':'PL','发音人':'Microsoft Kangkang Mobile - Chinese (Simplified, PRC)','音量':100,'语速':5,'语调':0},
    {'显示名':'{指定唯一神}满大人','发音人':'Microsoft Kangkang Mobile - Chinese (Simplified, PRC)','音量':100,'语速':5,'语调':0},
]

f_log =  open(sourcePath+'/log.txt', mode = 'r', encoding='utf-8')
if not os.path.exists(destPath+"/audio"): os.makedirs(destPath+"/audio")

##----此处填写内容结束----

# 人物台词列表，按roles顺序存放台词列表
roles_dialogue = []
#台词顺序-角色表
orders = []


for i in range(len(roles)):
    t = []
    roles_dialogue.append(t)

#分段读取log，按人物切割
log_paras = f_log.readlines()
for i in range(len(log_paras)):
    name = log_paras[i][1:].split('>')[0]
    for j in range(len(roles)):
        if(roles[j]==name):
            orders.append(j)
            roles_dialogue[j].append(log_paras[i])

if_rpy = int(input('是否要生成rpy文本\n1.是\n2.否\n'))
if(if_rpy == 1):
    f_rpy = open(destPath + '/script.rpy', mode='w', encoding='utf-8')
    # 输出rpy文本
    for i in range(len(roles_param)):
        f_rpy.write('define ' + roles_param[i]['显示名'] + ' = Character(\'' + roles_param[i]['显示名'] + '\')\n')
    f_rpy.write(
        'image ' + bg_param['背景名'].split('.')[0] + ' = im.Scale(\'' + bg_param['背景名'] + '\', ' + str(bg_param['长']) + ' ,' + str(
            bg_param['宽']) + ')\n')
    for i in range(len(roles_param)):
        f_rpy.write(
            'image ' + roles_param[i]['显示名'] + '_resized' + ' = im.Scale(\'' + roles_param[i]['头像名'] + '\', ' + str(
                roles_param[i]['长']) + ' ,' + str(roles_param[i]['宽']) + ')\n')
    f_rpy.write('\nlabel start:\n')
    f_rpy.write('    scene ' + bg_param['背景名'].split('.')[0] + '\n')
    # 内容部分
    voice_num = 0
    for i in range(len(orders)):
        # 开头
        if (i == 0):
            f_rpy.write(
                '    show ' + roles_param[orders[i]]['显示名'] + '_resized at ' + roles_param[orders[i]]['位置'] + '\n')
        # 需要更换立绘
        if (i != 0 and orders[i] != orders[i - 1]):
            f_rpy.write('    hide ' + roles_param[orders[i - 1]]['显示名'] + '_resized\n\n')
            f_rpy.write(
                '    show ' + roles_param[orders[i]]['显示名'] + '_resized at ' + roles_param[orders[i]]['位置'] + '\n')
        # 骰娘音效
        if (orders[i] < len(roles) - len(diceGirls)):
            f_rpy.write('    voice \'../audio/' + str(voice_num) + '.mp3\'\n')
            voice_num += 1
        else:
            f_rpy.write('    voice \'../audio/骰娘的声音.mp3\'\n')
        f_rpy.write('    ' + roles_param[orders[i]]['显示名'] + ' \'' + log_paras[i][1:].split('>')[1][1:-1] + '\'\n')

    f_rpy.write('\n    return')

if_audio = int(input('是否要生成声音合成文本\n1.是\n2.否\n'))
if(if_audio==1):
    audio_mode = int(input('请选择声音合成模式\n1.合总合成\n2.分段合成\n'))
    if (audio_mode == 1):
        # 朗读女txt，合总
        f_voice = open(destPath + '/audio/log.txt', mode='w', encoding='utf-8')
        for i in range(len(log_paras)):
            if (orders[i] < len(roles) - len(diceGirls)):
                # if(log_paras[i][-2:-1]=='"'):
                #     f_voice.write('[' + log_paras[i].split('>')[0][1:] + ']' + log_paras[i][1:].split('>')[1][1:-1] + '|' + '\n')  # 是引号就加到引号外边，避免电流麦 # 好像木大
                f_voice.write('[' + log_paras[i].split('>')[0][1:] + ']' + log_paras[i][1:].split('>')[1][1:-2]+'|'+log_paras[i][1:].split('>')[1][-2:]) #为了使歌词顺利分隔，此处加入无实际意义的|
    elif (audio_mode == 2):
        # 朗读女txt，分段
        voice_num = 0
        for i in range(len(log_paras)):
            if (orders[i] < len(roles) - len(diceGirls)):
                if not os.path.exists(destPath + '/audio/' + str(orders[i])): os.makedirs(destPath + '/audio/' + str(orders[i]))
                f_voice = open(destPath + '/audio/' + str(orders[i]) + '/' + str(voice_num) + '.txt', mode='w',encoding='utf-8')
                # f_voice.write('<\_@TTS\_/>\n')
                # for j in range(len(roles_voice_param)):
                #     f_voice.write('<_/1>'+roles_voice_param[j]['显示名']+'<_/2>'+roles_voice_param[j]['发音人']+'<_/3>'+roles_voice_param[j]['音量']+'<_/4>'+roles_voice_param[j]['语速']+'<_/5>'+roles_voice_param[j]['语调']+'<_/6></++/>\n')
                # f_voice.write('<\_@TTS\_/>\n')
                f_voice.write(log_paras[i][1:].split('>')[1][1:])
                voice_num += 1
    else:
        print('wrong input')

print("over")
