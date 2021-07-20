import regex
import os
from os import listdir
from os.path import isfile, join
import json 
from parser import *

syllabus_path = 'Courses'
json_path = 'GeneratedFiles'
instr_path = 'Instructions'
all_docs = listdir(syllabus_path)

#creates the directory for generated JSON files in case it doesn't exist
try:
	os.mkdir(json_path)
except FileExistsError:
	pass

#creates the directory for further instructions on the syllabi
try:
	os.mkdir(instr_path)
except FileExistsError:
	pass

#for reporting
counter_output = 0
counter_input =len([doc for doc in os.listdir(syllabus_path) if os.path.isfile(os.path.join(syllabus_path, doc))])-1

#this conditino allows to ignore other than .tex formats
for doc in all_docs:
	if '.tex' in doc:
		with open(join(syllabus_path, doc), "r") as fin:
			data = fin.read()
		instructions = ""
	else:
		continue

	# remove comments
	data = re.sub(r'%.+', '', data)
	structure = dict()

	if check_admin_details(data):
		continue
	#print(f'{doc} has another structure.')

	else:
		structure['Course info'] = {}
		structure['Course info']['Course name'] = find_course_name(data)
		#{'rus': '', 'eng': find_course_name(data)}
		try:
			structure['Course info']['Key concepts'] = find_key_concepts(data)
		except IndexError:
			instructions += "Add key concepts section\n"
		#{'rus': '', 'eng': find_key_concepts(data)}
		try:
			structure['Course info']['Purpose'] = find_purpose(data)
		except IndexError:
			structure['Course info']['Purpose'] = find_purpose_cd(data)
			instructions += "The purpose of the course is taken from the description of the course. Ckeck it out to make sure it's ok.\n"
		#{'rus': '', 'eng': find_purpose(data)}

		structure['Blooms taxonomy'] = {}
		structure['Blooms taxonomy']['Remember'] = find_remember_section(data)
		#{'rus': '', 'eng': find_remember_section(data)}
		structure['Blooms taxonomy']['Understand'] = find_understand_section(data)
		#{'rus': '', 'eng': find_understand_section(data)}
		structure['Blooms taxonomy']['Apply'] = find_apply_section(data)
		#{'rus': '', 'eng': find_apply_section(data)} 

		structure['Grades'] = {}
		structure['Grades']['Grades range'] = find_grades_range(data)
		structure['Grades']['Course evaluation'] = find_course_evaluation(data)

		structure['Course sections'] = find_course_sections(data)

		doc_name = doc.rsplit('.', 1)[0]

		#if there are additional instructions after parsing it will create a file in the directory instructions
		if instructions is not "":
			with open(join(instr_path, doc_name), 'w') as fout:
				fout.write(instructions)

		with open(join(json_path, f'{doc_name}.json'), 'w') as fout:
			counter_output += 1
			json.dump(structure, fout)

	with open(join(instr_path, "Overall report"), 'w') as fout:
		fout.write(f'{counter_output} files were generated out of {counter_input} files')
