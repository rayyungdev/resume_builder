from xmlrpc.client import Boolean
from resume_builder.builder import *
from resume_builder.templates import *
import argparse

'''
    Eventual Goal for this file is to run everything to the command line    
'''

default_file = './data/data.yaml'

# template = template_basic()
# resume = csv_builder(job_csv, skill_csv, basic_csv)
# key = ['programming']
# fname = 'template_basic_1.pdf'
# resume.build_resume(template, key, fname, max_experience = 7, display_project_skills = False) 

# template = template_basic()
# resume = csv_builder(job_csv, skill_csv, basic_csv)
# fname = 'template_basic_2.pdf'
# resume_2.build_resume(template, key, fname, max_experience = 7, display_project_skills=True)

'''
   Arguments:
      - data 
      - template
      - max_experience
      - max_skills
      - display_project_skills 
      - file name
      - keys
'''
my_parser = argparse.ArgumentParser(description='Resume Generator based off Key')
my_parser.add_argument('--input','-i', nargs = '*', action = 'store', type = str, required = False, help = 'Input Data')
my_parser.add_argument('--fname','-f', action = 'store', type = str, required = True, help = 'file name')
my_parser.add_argument('--key','-k', action = 'store', nargs = '+', type = str, required = True, help = 'keys')
my_parser.add_argument('--template','-t',action = 'store', type = str, required = False, help ='template type (only basic available)')
my_parser.add_argument('--max_experience', '-me', type= int, required = False, help = 'maximum experience, default = 7')
my_parser.add_argument('--max_skills', '-ms', type =int, required=False, help = 'maximum skills shown in tab, default = 7')
my_parser.add_argument('--display_project_skills', '-dps', type = Boolean, required=False, help = 'show skills in job section, default = False')
my_parser.add_argument('--header_font_size', '-hs', type = float, required=False, help = 'set header font size')
my_parser.add_argument('--body_font_size', '-bs', type = float, required=False, help = 'set body font size')
my_parser.add_argument('--title_font_size', '-ts', type = float, required=False, help = 'set title font size')

args = vars(my_parser.parse_args())
input = args['input']
template = args['template']
me = args['max_experience']
ms = args['max_skills']
dps = args['display_project_skills']
fname = args['fname']
key = args['key']

header_font_size = args['header_font_size']
body_font_size = args['body_font_size']
title_font_size = args['title_font_size']

if not fname.endswith('.pdf'):
   fname = fname + '.pdf'
if input is None:
   input = [default_file]

if template is None: 
   template = template_basic()

if header_font_size is None:
   header_font_size = 12
if body_font_size is None:
   body_font_size = 10.5
if title_font_size is None:
   title_font_size = 20

if me is None:
   me = 7

if ms is None:
   ms = 7

resume = False

if len(input) == 1:
   input = input[0]
   if input.endswith('.yaml'):
      resume = yaml_builder(input)
   else: 
      print('invalid argument' + input)
else:
   for file in input:
      check = 0
      if 'basic_info.csv' in file:
         basic_csv = file
      elif 'experience.csv' in file:
         job_csv = file
      elif 'skills.csv' in file:
         skills_csv = file 
      else:
         print('Invalid Argument : ', file)
         check +=1
   if check == 0:
      resume = csv_builder(job_csv, skills_csv, basic_csv)
if dps is None:
   dps = False

if resume:
   resume.build_resume(template, key, fname, max_experience = me, max_skills = ms, display_project_skills=dps, header_font_size=header_font_size, body_font_size=body_font_size, title_font_size=title_font_size)