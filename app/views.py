# -*- coding: utf-8 -*-
from app import app
from forms import testForm
from flask import render_template, request, redirect
import random

import os
import commands
import timeit
import resource 
from statistics import median, mean
from collections import Counter
from itertools import groupby
import string
import random
import math
import os
from werkzeug.utils import secure_filename

# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


NR_OF_TESTS = 10
console_param = ""

def allowed_file(filename):
	ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
   	f = request.files['file']
   	if not allowed_file:
   		alert('Error! Please choose file to upload')
   	elif not f:
   		alert('Error! Please choose file')
   	if f and allowed_file(f.filename):
   		f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
   		# f.save(secure_filename(f.filename)):
   		return 'file uploaded successfully'
   	


@app.route('/', methods=['GET', 'POST'])
def index():
	form = testForm(request.form, csrf_enabled=True)

	error = ''
	show_chart = False
	exception = False

	first_sys_name = ''
	second_sys_name = ''
	algorithm = 'BMS'
	nr_of_tests = 0
	msg_len = 0
	key_len = 0

	first_time = []
	first_time_median = []
	first_time_avg = []
	first_time_mode = []
	second_time = []
	second_time_median = []
	second_time_avg = []
	second_time_mode = []
	max_value = []

	if request.method == 'POST':

		f1 = request.files['file1']
		f2 = request.files['file2']
		if not f1:
	   		error = '|Error! Please choose the FIRST file to upload'
	   		print error
	   	elif not allowed_file(f1.filename):
	   		ALLOWED_EXTENSIONS = str(app.config['ALLOWED_EXTENSIONS']).replace("'", '').replace('set([', '').replace('])', '')
	   		error = error + "|Error! Wrong Extension of FIRST file. Allowed only: """ + ALLOWED_EXTENSIONS 	
	   		print error
	   	if not f2:
	   		error = error +  "|Error! Please choose the SECOND file to upload"
	   		print error
	   	elif not allowed_file(f2.filename):
	   		ALLOWED_EXTENSIONS = str(app.config['ALLOWED_EXTENSIONS']).replace("'", '').replace('set([', '').replace('])', '')
	   		error = error + "|Error! Wrong Extension of SECOND file. Allowed only: """ + ALLOWED_EXTENSIONS
	   		print error
	  	   		
	   	elif f1 and f2 and allowed_file(f1.filename) and allowed_file(f2.filename):
	   		f1.save(os.path.join(app.config['UPLOAD_FOLDER'], f1.filename))
	   		f2.save(os.path.join(app.config['UPLOAD_FOLDER'], f2.filename))
	   		# f.save(secure_filename(f.filename)):
	   		# return 'file uploaded successfully'


			exception = False
			show_chart = True

			
			try:
				nr_of_tests = int(form.nr_tests.data)
			except:
				exception = True
				print "EXCEPTION:", exception
				nr_of_tests = 0
				show_chart = False

			
			first_sys_name = form.first_sys_name.data
			second_sys_name = form.second_sys_name.data

			if not first_sys_name:
				first_sys_name = 'System 1'
			if not second_sys_name:
				second_sys_name = 'System 2'

			algorithm = 'BMS'

			if not (algorithm == 'BMS' or algorithm == 'AES'):
				exception = True
			else:
				# msg_len = form.msg_len.data
				# key_len = form.key_len.data


				system = f1.filename
				console_param = str(form.first_sys_param.data)
				data_statistics_first = calcPerformance(system, console_param, nr_of_tests)

				first_time = data_statistics_first[0]
				first_time_median = data_statistics_first[1]
				first_time_avg = data_statistics_first[2]
				first_time_mode = data_statistics_first[3]
				first_time_max = data_statistics_first[4]

				system = f2.filename
				console_param = str(form.second_sys_param.data)
				data_statistics_second = calcPerformance(system, console_param, nr_of_tests)

				second_time = data_statistics_second[0]
				second_time_median = data_statistics_second[1]
				second_time_avg = data_statistics_second[2]
				second_time_mode = data_statistics_second[3]
				second_time_max = data_statistics_second[4]

				
				max_value.append(max(first_time_max, second_time_max)* 1000)
				print "max value:", max_value

				print "first_time:", first_time, "second time:", second_time
		
	return render_template("index.html", form=form, first_sys_name=first_sys_name, 
			second_sys_name=second_sys_name,
			first_time=first_time, second_time=second_time, nr_of_tests=nr_of_tests, 
			first_time_median=first_time_median, first_time_avg=first_time_avg, first_time_mode=first_time_mode,
			second_time_median=second_time_median, second_time_avg=second_time_avg, second_time_mode=second_time_mode,
			max_value=max_value, show_chart=show_chart, exception=exception, error=error)



@app.route('/ro', methods=['GET', 'POST'])
def index_ro():
	form = testForm(request.form, csrf_enabled=True)

	error = ''
	show_chart = False
	exception = False

	first_sys_name = ''
	second_sys_name = ''
	algorithm = 'BMS'
	nr_of_tests = 0
	msg_len = 0
	key_len = 0

	first_time = []
	first_time_median = []
	first_time_avg = []
	first_time_mode = []
	second_time = []
	second_time_median = []
	second_time_avg = []
	second_time_mode = []
	max_value = []

	if request.method == 'POST':

		f1 = request.files['file1']
		f2 = request.files['file2']
		if not f1:
	   		error = '|Eroare! Alegeți PRIMUL fișier'
	   		print error
	   	elif not allowed_file(f1.filename):
	   		ALLOWED_EXTENSIONS = str(app.config['ALLOWED_EXTENSIONS']).replace("'", '').replace('set([', '').replace('])', '')
	   		error = error + "|Eroare! Extensia primului fișier e greșită. Extensii permise: """ + ALLOWED_EXTENSIONS 	
	   		print error
	   	if not f2:
	   		error = error +  "|Eroare! Alegeți AL DOILEA fișier"
	   		print error
	   	elif not allowed_file(f2.filename):
	   		ALLOWED_EXTENSIONS = str(app.config['ALLOWED_EXTENSIONS']).replace("'", '').replace('set([', '').replace('])', '')
	   		error = error + "|Eroare! Extensia celui de-al doilea fișier e greșită. Extensii permise: """ + ALLOWED_EXTENSIONS
	   		print error
	  	   		
	   	elif f1 and f2 and allowed_file(f1.filename) and allowed_file(f2.filename):
	   		f1.save(os.path.join(app.config['UPLOAD_FOLDER'], f1.filename))
	   		f2.save(os.path.join(app.config['UPLOAD_FOLDER'], f2.filename))
	   		# f.save(secure_filename(f.filename)):
	   		# return 'file uploaded successfully'


			exception = False
			show_chart = True

			
			try:
				nr_of_tests = int(form.nr_tests.data)
			except:
				exception = True
				print "EXCEPTION:", exception
				nr_of_tests = 0
				show_chart = False

			
			first_sys_name = form.first_sys_name.data
			second_sys_name = form.second_sys_name.data

			if not first_sys_name:
				first_sys_name = 'Sistem 1'
			if not second_sys_name:
				second_sys_name = 'Sistem 2'

			algorithm = 'BMS'

			if not (algorithm == 'BMS' or algorithm == 'AES'):
				exception = True
			else:
				# msg_len = form.msg_len.data
				# key_len = form.key_len.data


				system = f1.filename
				console_param = str(form.first_sys_param.data)
				data_statistics_first = calcPerformance(system, console_param, nr_of_tests)

				first_time = data_statistics_first[0]
				first_time_median = data_statistics_first[1]
				first_time_avg = data_statistics_first[2]
				first_time_mode = data_statistics_first[3]
				first_time_max = data_statistics_first[4]

				system = f2.filename
				console_param = str(form.second_sys_param.data)
				data_statistics_second = calcPerformance(system, console_param, nr_of_tests)

				second_time = data_statistics_second[0]
				second_time_median = data_statistics_second[1]
				second_time_avg = data_statistics_second[2]
				second_time_mode = data_statistics_second[3]
				second_time_max = data_statistics_second[4]

				
				max_value.append(max(first_time_max, second_time_max)* 1000)
				print "max value:", max_value

				print "first_time:", first_time, "second time:", second_time
		
	return render_template("index_ro.html", form=form, first_sys_name=first_sys_name, 
			second_sys_name=second_sys_name,
			first_time=first_time, second_time=second_time, nr_of_tests=nr_of_tests, 
			first_time_median=first_time_median, first_time_avg=first_time_avg, first_time_mode=first_time_mode,
			second_time_median=second_time_median, second_time_avg=second_time_avg, second_time_mode=second_time_mode,
			max_value=max_value, show_chart=show_chart, exception=exception, error=error)




def compileCpp(system):
	os.system("g++ " + "files/uploaded/" + system )
	os.system("g++ -o " + "files/uploaded/main " + "files/uploaded/" + system)

def testSystem(system, args, nr_of_tests):
	time_max = 0.0
	time = []

	if ".py" in system:
		command = "python"
	elif ".c" in system or ".cpp" in system:
		compileCpp(system)
		command = "files/uploaded/main"

	execute = command + " " + "files/uploaded/" +  system + " " + args

	for i in range(nr_of_tests):
		temp_time = timeit.timeit( lambda:os.system(execute), number=1)

		if temp_time > time_max:
			time_max = temp_time

		# time in milliseconds
		time.append(temp_time * 1000)  

	return time, time_max


def calcPerformance(system, console_param, nr_of_tests):

	function_name = "testSystem"

	time = []
	time_median = []
	time_avg = []
	time_mode = []
	
	data = testSystem(system, console_param, nr_of_tests)
	time = data[0]
	time_max = data[1]
	
	for i in range(nr_of_tests):
		time_median.append(median(time))
		time_avg.append(mean(time))
		
	return time, time_median, time_avg, time_mode, time_max




@app.route('/compile')
def compile():
	os.system("g++ BMS_cpp/main_encrypt.cpp BMS_cpp/encryption.cpp BMS_cpp/decryption.cpp BMS_cpp/keylib.cpp" )
	os.system('g++ -o BMS_cpp/encrypt BMS_cpp/main_encrypt.cpp BMS_cpp/encryption.cpp BMS_cpp/decryption.cpp BMS_cpp/keylib.cpp')
	os.system("g++ BMS_cpp/main_decrypt.cpp BMS_cpp/encryption.cpp BMS_cpp/decryption.cpp BMS_cpp/keylib.cpp" )
	os.system('g++ -o BMS_cpp/decrypt BMS_cpp/main_decrypt.cpp BMS_cpp/encryption.cpp BMS_cpp/decryption.cpp BMS_cpp/keylib.cpp')
	# os.system('xxd -c10 -b ./BMS_cpp/main')
	# os.system('./BMS_cpp/main')
	comp_output = "<strong>C++ compilation output:<strong><br>"+ commands.getstatusoutput('./BMS_cpp/encrypt')[1].replace('\n', '<br>')
	comp_output += "<br>---<br>"+ commands.getstatusoutput('./BMS_cpp/decrypt')[1].replace('\n', '<br>')

	print "****", comp_output.replace('<strong>', "").replace('<br>', '\n')

	return comp_output
