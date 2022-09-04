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
import logging
import sys

# Argument parser
my_parser = argparse.ArgumentParser(description='Generate a resume. Filter experience based on input tags')
my_parser.add_argument('--tags', '-t', metavar='TAG', action='store', nargs='+', type=str, 
                        required=True, help='Tags to filter for')
my_parser.add_argument('--input', '-i', nargs='*', action='store', type=str, required=False, 
                        default='./data/data.yaml', help='Input data file(s), either CSV files or a YAML file')
my_parser.add_argument('--output', '-o', action='store', type=str, required=True, help='Output file name')
my_parser.add_argument('--max-experience', '-me', type= int, required=False, default=7, help='Maximum experience')
my_parser.add_argument('--max-skills', '-ms', type =int, required=False, default=7, help='Maximum skills shown in tab')
my_parser.add_argument('--display-project-skills', '-dps', action='store_true', help='Show skills in job section')
my_parser.add_argument('--header-font-size', '-hs', type=float, required=False, default=12, help='Set header font size')
my_parser.add_argument('--body-font-size', '-bs', type=float, required=False, default=10.5, help='Set body font size')
my_parser.add_argument('--title-font-size', '-ts', type=float, required=False, default=20, help='Set title font size')
my_parser.add_argument('--debug', '-d', action='store_true', help='Print debug logging')

# Parsed args
args = vars(my_parser.parse_args())
template = template_basic()
tags = args['tags']
input = args['input']
output = args['output']
max_experience = args['max_experience']
max_skills = args['max_skills']
display_project_skills = args['display_project_skills']
header_font_size = args['header_font_size']
body_font_size = args['body_font_size']
title_font_size = args['title_font_size']

# Set log level
logging.basicConfig(encoding='utf-8', 
   level=logging.DEBUG if args['debug'] else logging.INFO)
logger = logging.getLogger('main')

# Log input variables
logger.info('Input file(s): %s', input)
logger.info('Max experience: %s', max_experience)
logger.info('Max skills: %s', max_skills)
logger.info('Display project skills: %s', display_project_skills)
logger.info('Output file: %s', output)
logger.info('Skill tags: %s', tags)
logger.info('Header font size: %s', header_font_size)
logger.info('Body font size: %s', body_font_size)
logger.info('Title font size: %s', title_font_size)

# Append default extension
if not output.endswith('.pdf'):
   output = output + '.pdf'
   logger.debug('Updated output filename with ext: %s', output)

# Create resume
resume = None
if len(input) == 1:
   input = input[0]
   if input.endswith('.yaml'):
      resume = builder_from_yaml(input)
   else: 
      logger.error('Expecting a .yaml file, got %s', input)
      sys.exit(1)
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
         logger.error('Expecting either basic_info.csv, experience.csv, or skills.csv, got %s', file)
         sys.exit(1)
   resume = builder_from_csv(job_csv, skills_csv, basic_csv)
resume.build_resume(template, tags, output,
   max_experience=max_experience, 
   max_skills=max_skills, 
   display_project_skills=display_project_skills, 
   header_font_size=header_font_size, 
   body_font_size=body_font_size, 
   title_font_size=title_font_size)