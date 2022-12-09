import os
import gtts


i = 3599


with open('words.txt', 'r') as f:
	for line in f:
		lst = line.split('|')
		try:
			os.mkdir(os.path.join(os.getcwd(), lst[0]))
		except:
			i += 1
			print(i)
			continue
		with open(lst[0] + '/' + lst[0], 'w') as dirr:
			print(lst[0], file=dirr)
		with open(lst[0] + '/' + 'meaning', 'w') as dirr:
			print(str(lst[1]) + '|' + str(lst[2]), file=dirr)
		tts = gtts.gTTS(text=lst[0], lang='en')
		tts.save(lst[0] + '/' + lst[0] + '.mp3')
		i += 1
		print(i)
