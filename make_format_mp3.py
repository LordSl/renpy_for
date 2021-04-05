from pydub import AudioSegment
from pydub.utils import mediainfo

sourcePath = 'format/'
destPath = 'format/'

mp3 = AudioSegment.from_mp3(sourcePath+'format_mp3.mp3')
for i in range(1000):
    mp3.export(destPath+'/'+str(i)+'.mp3',format='mp3')
    print(i)