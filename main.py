from builder import *
from templates import *
import sys, getopt
'''
    Eventual Goal for this file is to run everything to the command line    
'''

job_file = './data/experience.csv'
skill_file = './data/skills.csv'
basic_info = './data/basic_info.csv'

#### Template_basic no skills
template = template_basic()
resume = resume_builder(job_file, skill_file, basic_info)
key = ['programming']
fname = 'template_basic_1.pdf'
resume.build_resume(template, key, fname, max_experience = 7, display_project_skills = False) 

template = template_basic()
resume_2 = resume_builder(job_file, skill_file, basic_info)
fname = 'template_basic_2.pdf'
resume_2.build_resume(template, key, fname, max_experience = 7, display_project_skills=True)