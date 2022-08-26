from re import S
from tabnanny import process_tokens
import pandas as pd
from .templates import *
import logging
import yaml

month = {
    1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June', 7 : 'July', 8 : 'August', 9 : 'September', 10 : 'October', 11 : 'November',12 : 'December'    
}

# Get logger
logger = logging.getLogger('builder')

class builder: 
    """
    My plan is to make this class inheritable for difference types of inputs. 
    """
    def __init__(self, name, subheader_info, education, skills, jobs):
        self.name = name
        self.subheader_info = subheader_info
        self.education = education
        self.skills = skills
        self.jobs = jobs
        logger.info('Resume Processed')
        logger.info('  name: %s', self.name)
        logger.info('  subheader_info: %s', self.subheader_info)
        logger.info('  skills:')
        for category, items in self.skills.items():
            logger.info('    %s: %s', category, items)
        logger.info('  education:')
        for title, detail in self.education.items():
            logger.info('    %s', title)
            logger.info('      address: %s', detail['address'])
            logger.info('      completed: %s', detail['completed'])
            logger.info('      GPA: %s', detail['GPA'])
        logger.info('  jobs:\n%s', self.jobs)

    def build_experience(self, tags, max_list = 5, display_project_skills = False):
        logger.info('Build experience')
        filtered_jobs = self.jobs[self.jobs.tags.apply(lambda x: any(k in x for k in tags))]
        logger.debug('After filtered tags: \n%s', filtered_jobs)
 
        # Holders for work and project experience
        experience = { 'work': {}, 'projects': {} }

        # Get work experiences up to max_list
        work_items = filtered_jobs[filtered_jobs.type == 'J'].head(max_list)
        work_items['date'] = self._format_experience_date_ranges(work_items)
        work_items = work_items[['company', 'title', 'location', 'date', 'detail']]
        logger.debug('Work experience items: \n%s', work_items)
        experience['work'] = work_items.set_index('company').to_dict('index')

        # Add project experience if no. work items < max_list
        if len(work_items) < max_list:
            project_items = filtered_jobs[filtered_jobs.type == 'P']
            project_items = project_items.head(max_list - len(work_items))
            project_items['date'] = self._format_experience_date_ranges(project_items)
            project_items = project_items[['title', 'date', 'skills', 'detail']]
            if not display_project_skills:
                project_items = project_items.drop(columns=['skills']) # Drop skills column if we're not displaying it
            logger.debug('Project experience items: \n%s', project_items)
            experience['projects'] = project_items.set_index('title').to_dict('index')

        # Return experience
        logger.info('Experience Dict: %s', experience)
        return experience
        
    def build_skills(self, max_list = 5):
        logger.info('Build skills')
        for skill in self.skills:
            skill_set = self.skills[skill]
            if len(skill_set) < max_list:
                continue
            else: 
                self.skills[skill] = skill_set[0:max_list]
        logger.info('Skillset: %s', self.skills)
        return self.skills
    
    def build_resume(self,
            template,
            keys,
            output,
            max_experience = 7,
            max_skills = 7,
            display_project_skills = False,
            header_font_size = 12,
            body_font_size = 10.5,
            title_font_size = 20,
            font = 'Helvetica'):
        name = self.name
        address = self.subheader_info
        education = self.education
        experience = self.build_experience(
            tags = keys,
            max_list = max_experience,
            display_project_skills = display_project_skills) 
        skills = self.build_skills(max_list=max_skills)
        logger.info('Fill template')
        template.fill_resume(
            name,
            address,
            skills,
            experience['work'],
            education,
            experience['projects'],
            header_font_size = header_font_size,
            body_font_size = body_font_size,
            title_font_size = title_font_size,
            font = font)
        template.output(output)
        logger.info('Resume made')

    def _format_experience_date_ranges(self, item):
        date_format = '%B %Y'
        start_str = item.start.dt.strftime(date_format)
        end_str = item.end.dt.strftime(date_format).fillna('Present')
        return start_str + ' - ' + end_str


def builder_from_csv(fjobs, fskills, basic_info):
    jobs = pd.read_csv(fjobs)
    jobs.tags = jobs.tags.apply(lambda x: x.split(', '))
    jobs.detail = jobs.detail.apply(lambda x: x.split(', '))
    jobs['start'] = pd.to_datetime(jobs['start'])
    jobs['end'] = pd.to_datetime(jobs['end'])
    jobs = jobs.sort_values('start', ascending = False)
    jobs['type'] = jobs['type'].apply(lambda x: x.upper())
    basic = pd.read_csv(basic_info)
    basic.edu_1 = basic.edu_1.apply(lambda x:str(x).split('/ '))
    basic.edu_2 = basic.edu_2.apply(lambda x:str(x).split('/ '))
    education = {
        basic.edu_1.item()[0] : 
        {
            'address':basic.edu_1.item()[1], 
            'completed': basic.edu_1.item()[2],
            'GPA': basic.edu_1.item()[3]

        },
        basic.edu_2.item()[0] : 
        {
            'address': basic.edu_2.item()[1],
            'completed': basic.edu_2.item()[2],
            'GPA': basic.edu_2.item()[3]
        }
    }
    address = basic.address.item()
    skills = pd.read_csv(fskills)
    for col in skills:
        skills[col] = skills[col].apply(lambda x: x.split(', '))
    skills = skills.to_dict()
    for i in skills:
        skills[i] = skills[i][0]
    name = basic.name.item()
    return builder(name, address, education, skills, jobs)


def builder_from_yaml(fname):
    with open (fname, 'r') as f:
        data = yaml.safe_load(f)
    jobs = pd.DataFrame.from_dict(data['experience'], orient='index')
    jobs['start'] = pd.to_datetime(jobs['start'])
    jobs['end'] = pd.to_datetime(jobs['end'])
    jobs = jobs.sort_values('start', ascending = False)
    jobs['type'] = jobs['type'].apply(lambda x: x.upper())
    skills = data['skills']
    name = data['name']
    address = data['subheader_info']
    education = data['education']
    return builder(name, address, education, skills, jobs)