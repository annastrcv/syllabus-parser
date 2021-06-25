import regex as re
from os import listdir
from os.path import isfile, join
import json 
from parser import *

syllabus_path = 'Courses'
json_path = 'GeneratedFiles'
all_docs = listdir(syllabus_path)

for doc in all_docs:
	with open(join(syllabus_path, doc), "r") as fin:
		data = fin.read()

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
		structure['Course info']['Key concepts'] = find_key_concepts(data)
		#{'rus': '', 'eng': find_key_concepts(data)}
		structure['Course info']['Purpose'] = find_purpose(data)
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
		with open(join(json_path, f'{doc_name}.json'), 'w') as fout:
			json.dump(structure, fout)