# Syllabus Parser

The program is able to convert syllabus from Latex to JSON format. 

## JSON structure

### Background

The structure presented below contains sections that are common to the syllabus and the educational plan (? РПД). A correspondence matrix was constructed for better visualization of intersecting sections (you could find it by [this link](https://docs.google.com/spreadsheets/d/1NrIC6H2qXS8NksnokkIdLbHTqK7KwmHXLzEe7loZxJ8/edit?usp=sharing)). 

JSON structure for the syllabus is following:
* Course info
  - Course name
  - Key concepts
  - Purpose
* Blooms Taxonomy
  - Remember
  - Understand
  - Apply
* Grades
  - Grades range
  - Course evaluation
* Course sections

[*A completed json document on the example of Computer Vision course*](https://docs.google.com/document/d/1bjkWA5q_x4BYuUt5ZArQfn4H4TprZIdqL-ZAc1ur0Rs/edit?usp=sharing).

### Course info

1. *Course name* stores a string with the name of the course.
2. *Key concepts* stores a list of the key concepts of the course.
3. *Purpose* stores a string with the description of the purpose of the course.

### Blooms Taxonomy

1. *Remember* stores a list of the topics that the students should be able to recognize and define by the end of the course.
2. *Understand* stores a list of the topics that the students should be able to describe and explain by the end of the course.
3. *Apply* stores a list of the topics that the students should be able to perform by the end of the course.

### Grades

1. *Grades range* stores a list with a mapping between a letter grade and points range for the final mark.

Example: 
```{"grade": "A", "points": [90, 100]}```

2. *Course evaluation* stores a list with a mapping between a task and how many points it weighs.

Example: 
```{"type": "Exams", "points": 30}```

### Course sections

*Course sections* stores a list of objects where each item is an information about one section.
Section info has the following structure:
* Section number: int
* Section title: string
* Covered topics: list of strings
* Forms of evaluation:
  - Development of individual parts of software product code
  - Homework and group projects
  - Midterm evaluation
  - Testing (written or computer based)
  - Reports
  - Essays
  - Oral polls
  - Discussions
* Questions for ongoing performance evaluation: list of strings
* Questions for seminar classes (labs): list of strings
* Questions for final assessment: list of strings
* Hours distribution:
  - Total
  - Lectures
  - Labs
  - Self-study
  - Knowledge evaluation

*Forms of evaluation* stores an object where for each key the value could be 0 or 1 (depending on whether this form will be used for evaluation in this section).
*Hours distribution* strores an object where for each key the value is the number of hours spent.

## Parser

Regular expressions were used for parsing Latex document.
All functions are stored in `parser.py`.  

To generate JSON versions for the syllabi you should define a path where the Latex documents are stored in `syllabus_path` in `main.py`.
JSON documents will be created in the directory specified in `json_path` in `main.py`.

