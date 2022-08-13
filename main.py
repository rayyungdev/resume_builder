"""
Eventual Goal for this file is to run everything to the command line

Arguments:
   - data 
   - template
   - max_experience
   - max_skills
   - display_project_skills 
   - file name
   - keys
"""
from xmlrpc.client import Boolean
from resume_builder.builder import *
from resume_builder.templates import *
import argparse

my_parser = argparse.ArgumentParser(description='Resume Generator based off Key')
my_parser.add_argument('--input', '-i', nargs='*', action='store', type=str, required=False, 
                        default='./data/data.yaml', help='Input data file(s), either CSV files or a YAML file')
my_parser.add_argument('--fname', '-f', action='store', type=str, required=True, help='Output file name')
my_parser.add_argument('--key', '-k', action='store', nargs='+', type=str, required=True, help='Skill keys to filter for')
my_parser.add_argument('--max_experience', '-me', type= int, required=False, default=7, help='Maximum experience')
my_parser.add_argument('--max_skills', '-ms', type =int, required=False, default=7, help='Maximum skills shown in tab')
my_parser.add_argument('--display_project_skills', '-dps', type=Boolean, required=False, default=False, help='Show skills in job section')
my_parser.add_argument('--header_font_size', '-hs', type=float, required=False, default=12, help='Set header font size')
my_parser.add_argument('--body_font_size', '-bs', type=float, required=False, default=10.5, help='Set body font size')
my_parser.add_argument('--title_font_size', '-ts', type=float, required=False, default=20, help='Set title font size')

args = vars(my_parser.parse_args())
template = template_basic()
input = args['input']
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

if resume:
   resume.build_resume(template, key, fname, 
                        max_experience=me, 
                        max_skills=ms, 
                        display_project_skills=dps, 
                        header_font_size=header_font_size, 
                        body_font_size=body_font_size, 
                        title_font_size=title_font_size)