import regex as re

# -------------------- COURSE INFO ------------------------------------------

def find_course_name(data):
  match = re.findall(r'Course\s+name\W+\w.+', data)
  course_name = match[0].split(" ", 2)
  return course_name[-1].strip()

def find_course_number(data):
  match = re.findall(r'Course\s+number\W+(.+)', data)
  return match[0]

def find_key_concepts(data):
  regex = re.compile('{Key\s+concepts\s+of\s+the\s+class}(.+?)\\\sub', re.DOTALL) #dotall is to make the dot character match any character including new line
  match = regex.findall(data)
  return get_items_list(match[0])

def find_purpose(data):
  regex = re.compile('{What\s+is\s+the\s+purpose\s+of\s+this\s+course(.+?)\\\sub', re.DOTALL)
  match = regex.findall(data)
  splitted = match[0].split('\n')
  text = " ".join(splitted[1:-1]).strip()
  return text

#find purpose from the course description
def find_purpose_cd(data):
  regex = re.compile('Course\s+description(.+?)\\\sub', re.DOTALL)
  match = regex.findall(data)
  splitted = match[0].split('\n')
  text = " ".join(splitted[1:-1]).strip()
  return text

# ---------------------- BLOOM'S TAXONOMY -----------------------------------

def find_remember_section(data):
  regex = re.compile('What\s+should\s+a\s+student\s+remember(.+?)\\\end\{itemize}', re.DOTALL)
  match = regex.findall(data)
  if len(match) > 0:
   return get_items_list(match[0])
  else:
   return []

def find_understand_section(data):
  regex = re.compile('What\s+should\s+a\s+student\s+be\s+able\s+to\s+understand(.+?)\\\end\{itemize}', re.DOTALL)
  match = regex.findall(data)
  if len(match) > 0:
   return get_items_list(match[0])
  else:
   return []

def find_apply_section(data):
  regex = re.compile('What\s+should\s+a\s+student\s+be\s+able\s+to\s+apply(.+?)\\\end\{itemize}', re.DOTALL)
  match = regex.findall(data)
  if not match:
    regex = re.compile('What\s+should\s+a\s+student\s+be\s+able\s+to\s+perform(.+?)\\\end\{itemize}', re.DOTALL)
    match = regex.findall(data)
  if len(match) > 0:
   return get_items_list(match[0])
  else:
   return []

# ------------------------- GRADES ------------------------------------------

def find_grades_range(data):
  grades = []
  try:
    regex = re.compile('Grades range(.+?)\\\end{table}', re.DOTALL)
    match = regex.search(data)
    table = match.group(0)
    table = table.split('\hline')[2:-1]
    
    for row in table:
      try:
        t, dp, pp = row.split('&')
      except:
        t, dp = row.split('&')
        pp = dp
      t = t.strip()
      dp = re.findall('\d+\W\d+', dp)
      pp = re.findall('\d+\W\d+',pp)
      range = dict()
      try:
        l, h = pp[0].split('-')
      except:
        l, h = dp[0].split('-')
      range['grade'] = t[0]
      range['points'] = [int(l), int(h)]
      grades.append(range)
  except:
    pass
  return grades

def find_course_evaluation(data):
  regex = re.compile('Course evaluation(.+?)\\\end{', re.DOTALL)
  match = regex.search(data)
  if not match:
    regex = re.compile('Evaluation(.+?)\\\end{', re.DOTALL)
    match = regex.search(data)
  grades = []
  try:   
    table = match.group(0)
    table = table.split('\hline')[2:-1]
    for row in table:
      try:
        t, dp, pp = row.split('&')
      except:
        t, dp = row.split('&')
        pp = dp
      t = t.strip()
      dp = re.sub('\D', '', dp)
      pp = re.sub('\D', '', pp)
      distrib = dict()
      try:
        points = int(pp)
      except:
        points = int(dp)
      distrib['type'] = t
      distrib['points'] = points
      grades.append(distrib)
  except:
    try:
      table = get_items_list(match[0])
      for row in table:
        t, p = row.split('(')
        t = t.strip()
        points = int(re.sub('\W', '', p))
        distrib = dict()
        distrib['type'] = t
        distrib['points'] = points
    except:
      pass
  return grades

# ------------------------ COURSE SECTIONS ----------------------------------

def find_hours_distrib(data):
  hours_list = []
  try:
    regex = re.compile('\\\subsection{Course Sections}(.+?)\\\sub', re.DOTALL)
    match = regex.search(data)
    table = match.group(0)
    table = table.split('\hline')[2:-1]
    
    for row in range(1, len(table)+1):
      hours = dict()
      splitted = re.sub('\\\&', 'and', table[row-1]).split('&')
      if len(splitted) == 6:
        hours["Lectures"] = int(re.sub('\W', '', splitted[2]))
        hours["Labs"] = int(re.sub('\W', '', splitted[3]))
        hours["Self-study"] = int(re.sub('\W', '', splitted[4]))
        hours["Knowledge evaluation"] = int(re.sub('\W', '', splitted[5]))
        hours["Total"] = sum(hours.values())
        hours["Section number"] = row
      if len(splitted) == 3:
        try:
          hours["Total"] = int(re.sub('\W', '', splitted[2]))
          hours["Lectures"] = 0
          hours["Labs"] = 0
        except:
          lec, lab = re.sub('[a-zA-Z]+', ' ', re.sub('\W', '', splitted[2])).split()
          hours["Total"] = int(lec)+int(lab)
          hours["Lectures"] = int(lec)
          hours["Labs"] = int(lab)
        hours["Self-study"] = 0
        hours["Knowledge evaluation"] = 0
        hours["Section number"] = row
      if hours:
        hours_list.append(hours)
  except:
    pass
  return hours_list

def find_section_title(s):
  try:
    match = re.search(r'Section title\W+.+', s)
    return match.group().split('\n')[-1].strip()
  except:
    return ''

def find_section_topics(s):
  regex = re.compile('Topics covered in this section.+?\\\end\{itemize}', re.DOTALL)
  match = regex.findall(s)
  if len(match) > 0:
   return get_items_list(match[0])
  else:
   return []

def find_perf_eval_qs(s):
  regex = re.compile('ongoing performance evaluation.+?\\\end\{', re.DOTALL)
  match = regex.findall(s)
  if len(match) > 0:
   return get_items_list(match[0])
  else:
   return []

def find_seminar_qs(s):
  regex = re.compile('for seminar classes.+?\\\end\{', re.DOTALL)
  match = regex.findall(s)
  if len(match) > 0:
   return get_items_list(match[0])
  else:
   return []

def find_test_qs(s):
  regex = re.compile('for final assessment.+?\\\end\{', re.DOTALL)
  match = regex.findall(s)
  if len(match) > 0:
   return get_items_list(match[0])
  else:
   return []

def find_forms_of_eval(s):
  forms_dict  = dict()
  try:
    regex = re.compile('{table}.+?{table}', re.DOTALL)
    if regex.findall(s):
      table = regex.findall(s)[0]
      regex2 = re.compile(r'[\n\r\t]')
      forms_list = regex2.sub(" ", table.split('\hline')[2]).split('\\\\')
      
      for row in forms_list[:-1]:
        form, flag = row.split('&')
        form = form.strip()
        flag = int(flag.strip())
        forms_dict[form] = flag
  except:
    pass
  return forms_dict

def find_course_sections(data):

  sections_list = []
  
  regex1 = re.compile('\\\subsubsection{Section \d}.+?\\\subsubsection{Section \d}', re.DOTALL)
  match1 = regex1.findall(data, overlapped=True)
  regex2 = re.compile(f'subsubsection{{Section {len(match1)+1}.+', re.DOTALL)
  match1.extend(regex2.findall(data))
  hours = find_hours_distrib(data)

  for i in range(len(match1)):
    sec_info = {}
    section = match1[i]
    sec_info["Section number"] = i+1
    sec_info["Section title"] = find_section_title(section)
    sec_info["Covered topics"] = find_section_topics(section)
    sec_info["Questions for ongoing performance evaluation"] = find_perf_eval_qs(section)
    sec_info["Questions for seminar classes"] = find_seminar_qs(section)
    sec_info["Questions for final assessment"] = find_test_qs(section)
    sec_info["Forms of evaluation"] = find_forms_of_eval(section)
    if hours:
      for hours_info in hours:
        if hours_info["Section number"] == sec_info["Section number"]:
          sec_info["Hours distribution"] = hours_info 
    sections_list.append(sec_info)
  
  for section in sections_list:
    if "Hours distribution" in section.keys():
      del section["Hours distribution"]["Section number"] 

  return sections_list

# ------------------------ HELP FUNCTIONS ----------------------------------

def get_items_list(s):
  items = re.findall(r'item\s.+', s)
  items_list = []
  for item in items:
    formatted = re.sub('\\\&', '&', item.split(" ", 1)[1].strip())
    items_list.append(formatted)
  return items_list  

def check_admin_details(data):
  ad = re.findall(r'Administrative details\W+\w.+', data)
  return ad