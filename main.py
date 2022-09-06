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
from resume_builder.builder import *
from resume_builder.templates import *
import os
import argparse
import logging
import sys

# Argument parser
my_parser = argparse.ArgumentParser(description='Generate a resume. Filter experience based on input tags')
my_parser.add_argument('--tags', '-t', metavar='TAG', action='store', nargs='+', type=str, required=True, help='Tags to filter for')
my_parser.add_argument('--input', '-i', action='store', type=str, required=False, default='./data/data.yaml', 
                        help='Input data file/directory, either a YAML file or directory of csv files')
my_parser.add_argument('--output', '-o', action='store', type=str, required=True, help='Output file name')
my_parser.add_argument('--max-experience', '-me', type=int, required=False, default=7, help='Maximum experience')
my_parser.add_argument('--max-skills', '-ms', type=int, required=False, default=7, help='Maximum skills shown in skill section')
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

# Append default extension for output file
if not output.endswith('.pdf'):
   output = output + '.pdf'
   logger.debug('Updated output filename with ext: %s', output)

# Parse input file/directory into resume
if input.endswith('.yaml'):
   resume = builder_from_yaml(input)
elif os.path.isdir(input):
   basic_info = 'basic_info.csv'
   experience = 'experience.csv'
   skills = 'skills.csv'
   csv_files = [basic_info, experience, skills]
   list_csv_dir = os.listdir(input)
   remaining = [file for file in csv_files if file not in list_csv_dir]
   if remaining:
      logger.error('Missing csv data files in directory %s: %s', input, remaining)
      sys.exit(1)
   resume = builder_from_csv(f'{input}/{experience}', f'{input}/{skills}', f'{input}/{basic_info}')
else:
   logger.error('Input not a directory or .yaml file: %s', input)
   sys.exit(1)

# Build resume
resume.build_resume(template, tags, output,
   max_experience=max_experience, 
   max_skills=max_skills, 
   display_project_skills=display_project_skills, 
   header_font_size=header_font_size, 
   body_font_size=body_font_size, 
   title_font_size=title_font_size)