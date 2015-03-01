# -*- coding:utf-8 -*-
"""
Test

"""
import cv
import cv2
from progressbar import *
import os

ffmpeg_path = r'D:\scripts\Muscle plus\ffmpeg.exe'

def get_split_xrange(nFrames, split_frames_numner):
	split_list = [z for z in xrange(0, nFrames, split_frames_numner)]

	if split_list[-1] != nFrames:
		split_list.append(nFrames)

	import copy
	aa = copy.copy(split_list)
	aa.remove(aa[0])
	return [xrange(a[0], a[1]) for a in zip(split_list, aa)]

	
def split_video(filename, split_frames_numner=100, only_audio=None, debug=None):

	vidFile = cv.CaptureFromFile(filename)
	nFrames = int(cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FRAME_COUNT ) )
	fps = cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FPS)
	
	print nFrames
	print fps
	print split_frames_numner/float(fps)

	if debug:
		return
	size = (int(cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FRAME_WIDTH )), 
			int(cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FRAME_HEIGHT )))
			
	ex = int(cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FOURCC ))
	type_1, type_2, type_3, type_4 = [chr(ex & 0XFF),
									 chr((ex & 0XFF00) >> 8),
									 chr((ex & 0XFF0000) >> 16),
									 chr((ex & 0XFF000000) >> 24)]
	
	#print [type_1, type_2, type_3, type_4]
	split_list = get_split_xrange(nFrames, split_frames_numner)

	widgets = [os.path.basename(filename)+':',
			   Percentage(), ' ',
			   Bar(marker='#',left='[',right=']'),
			   ' ', ETA(), ' ', FileTransferSpeed()]
	if only_audio:
		maxval = len(split_list)
	else:
		maxval = nFrames
		
	pbar = ProgressBar(widgets=widgets, maxval=maxval)
	pbar.start()
	pbar.update(0)
		
	audio_pos = 0
	for i, a in enumerate(split_list):
		split_audio(filename, split_frames_numner, 'd:\\test\\SPLIT\\'+str(i)+'.mp3', audio_pos, (split_frames_numner/fps)-0.1)	
		audio_pos += split_frames_numner/fps
		
		if only_audio:
			pbar.update(i)
			continue
		
		#fourcc = cv.CV_FOURCC(type_1, type_2, type_3, type_4)
		fourcc = cv.CV_FOURCC('M', 'J', 'P', 'G')
		videoWriter = cv.CreateVideoWriter('d:\\test\\SPLIT\\'+str(i)+'.AVI', fourcc, fps, size, 1)
			# split audio
	
		for n in a:
			# update cmd progress
			pbar.update(n)
	
			cv.GrabFrame(vidFile)
			frame = cv.RetrieveFrame(vidFile)
			cv.WriteFrame(videoWriter, frame)
	pbar.finish()

	
def split_audio(filename, split_frames_numner=100, out_file=None, start=0, end=0):

	command = '""{ffmpeg_path}" -i "{filename}" -ss {start} -t {end} -af "volume=1.5"  {out_file}"'.format(ffmpeg_path=ffmpeg_path, out_file=out_file, start=start, end=end, filename=filename)

	#os.system(command)
	os.popen(command)

	
if __name__ == '__main__':
		
	split_video(r'D:\\Total Upper Body Dumbbell Workout.mp4', 200,only_audio=True, debug=0)

		






