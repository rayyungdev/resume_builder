from re import S
import pandas as pd
from .templates import *
import logging

month = {
    1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June', 7 : 'July', 8 : 'August', 9 : 'September', 10 : 'October', 11 : 'November',12 : 'December'    
}

# Get logger
logger = logging.getLogger('builder')

class builder: 
    '''
    my plan is to make this class inheritable for difference types of inputs. 
    '''
    def build_experience(self, tags, max_list = 5, display_project_skills = False):
        logger.info('Build experience')
        logger.debug('Create job lookup as dataframe')
        if type(self.jobs) is dict:
            self.jobs = pd.DataFrame.from_dict(self.jobs, orient='index' )
        self.jobs['start'] = pd.to_datetime(self.jobs ['start'])
        self.jobs ['end'] = pd.to_datetime(self.jobs['end'])
        self.jobs  = self.jobs.sort_values('start', ascending = False)
        self.jobs['type'] = self.jobs['type'].apply(lambda x: x.upper())
        logger.debug('\n%s', self.jobs)
        logger.debug('Filter for tags')
        job_lookup = self.jobs[self.jobs.tags.apply(lambda x: any(k in x for k in tags))]
        logger.debug('\n%s', job_lookup)

        logger.debug('Set work experience')
        company_list = job_lookup[job_lookup.type == 'J'].company.to_list()
        experience = dict()
        work = dict() #will get put in experience later        
        count = 1
        def check_null_date(row_input):
            return pd.isnull(row_input.item())
        for company in company_list:
            if count > max_list :
                logger.warning('Max limit reached!')
                experience.update({'work': work})
                logger.warning(experience)
                return experience
            
            count += 1
            row = job_lookup[job_lookup.company == company]
            start_date = month[pd.to_datetime(row.start).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.start).dt.year.astype(str).item()
            if not check_null_date(row.end):
                end_date = month[pd.to_datetime(row.end).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.end).dt.year.astype(str).item()
            else:
                end_date = 'present'
            
            work[company] = {
                'location' : row.location.item(), 
                'title' : row.title.item(), 
                'date' : start_date + ' - ' + end_date,
                'detail' : row.detail.item()
            }
            
        experience['work'] = work
        projects = dict() #will get put in experience later
        project_list = job_lookup[job_lookup.type == 'P'].title.to_list()

        logger.debug('Set project experience')
        for project in project_list:
            if count > max_list : 
                 break
            count +=1
            row = job_lookup[job_lookup.title == project]

            if not check_null_date(row.start):
                start_date = month[pd.to_datetime(row.start).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.start).dt.year.astype(str).item()
                if not check_null_date(row.end):
                    end_date = month[pd.to_datetime(row.end).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.end).dt.year.astype(str).item()
                else: 
                    end_date = "present"
                if not display_project_skills:
                    projects[project] = {
                        'date' : start_date + ' - ' + end_date,
                        'detail' : row.detail.item()
                    }
                else: 
                    projects[project] = {
                        'date' : start_date + ' - ' + end_date,
                        'detail' : row.detail.item(),
                        'skills': row.skills.item()
                    }
            else: 
                if not display_project_skills:
                    projects[project] = {
                        'date' : None,
                        'detail' : row.detail.item()
                    }
                else: 
                    projects[project] = {
                        'date' : None,
                        'detail' : row.detail.item(),
                        'skills': row.skills.item()
                    }
        experience['projects'] = projects
        logger.info(experience)
        return experience
        
    def build_skills(self, max_list = 5):
        logger.info('Build skills')
        for skill in self.skills:
            skill_set = self.skills[skill]
            if len(skill_set) < max_list:
                continue
            else: 
                self.skills[skill] = skill_set[0:max_list]
        logger.info(self.skills)
        return self.skills
    
    def build_resume(self, template, keys, output, max_experience = 7, max_skills = 7, display_project_skills = False, header_font_size = 12, body_font_size = 10.5, title_font_size =20, font = 'Helvetica'):
        name = self.name
        address = self.address
        education = self.education
        experience = self.build_experience(tags = keys, max_list = max_experience, display_project_skills= display_project_skills) 
        skills = self.build_skills(max_list=max_skills)
        logger.info('Fill template')
        template.fill_resume(name, address, skills, experience['work'], education, experience['projects'], header_font_size = header_font_size, body_font_size = body_font_size, title_font_size = title_font_size, font = font)
        template.output(output)
        logger.info('Resume made')


class csv_builder(builder):
    def __init__(self, fjobs, fskills, basic_info):
        self.jobs = pd.read_csv(fjobs)
        self.jobs.tags = self.jobs.tags.apply(lambda x: x.split(', '))
        self.jobs.detail = self.jobs.detail.apply(lambda x: x.split(', '))

        basic = pd.read_csv(basic_info)
        basic.edu_1 = basic.edu_1.apply(lambda x:str(x).split('/ '))
        basic.edu_2 = basic.edu_2.apply(lambda x:str(x).split('/ '))
        self.education = {
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
        self.address = basic.address.item()

        self.skills = pd.read_csv(fskills)
        for col in self.skills:
            self.skills[col] = self.skills[col].apply(lambda x: x.split(', '))
        self.skills = self.skills.to_dict()
        for i in self.skills:
            self.skills[i] = self.skills[i][0]
        self.name = basic.name.item()
        logger.info('Resume Processed')
        logger.info('  name: %s', self.name)
        logger.info('  subheader_info: %s', self.address)
        logger.info('  skills:')
        for category, items in self.skills.items():
            logger.info('    %s: %s', category, items)
        logger.info('  education:')
        for title, detail in self.education.items():
            logger.info('    %s', title)
            logger.info('      address: %s', detail['address'])
            logger.info('      completed: %s', detail['completed'])
            logger.info('      GPA: %s', detail['GPA'])
        logger.info('  jobs:')
        for job in self.jobs.values():
            logger.info('    - type:     %s', job['type'])
            logger.info('      tags:     %s', job['tags'])
            logger.info('      title:    %s', job['title'])
            logger.info('      skills:   %s', job['skills'])
            logger.info('      start:    %s', job['start'])
            logger.info('      end:      %s', job['end'])
            logger.info('      company:  %s', job['company'])
            logger.info('      location: %s', job['location'])
            logger.info('      details:')
            for detail in job['detail']:
                logger.info('        - %s', detail)


import yaml

class yaml_builder(builder): 
    def __init__(self, fname):
        with open (fname, 'r') as f:
            self.data = yaml.safe_load(f)
        self.jobs = self.data['experience']
        self.skills = self.data['skills']
        self.name = self.data['name']
        self.address = self.data['subheader_info']
        self.education = self.data['education']
        logger.info('Resume Processed')
        logger.info('  name: %s', self.name)
        logger.info('  subheader_info: %s', self.address)
        logger.info('  skills:')
        for category, items in self.skills.items():
            logger.info('    %s: %s', category, items)
        logger.info('  education:')
        for title, detail in self.education.items():
            logger.info('    %s', title)
            logger.info('      address: %s', detail['address'])
            logger.info('      completed: %s', detail['completed'])
            logger.info('      GPA: %s', detail['GPA'])
        logger.info('  jobs:')
        for job in self.jobs.values():
            logger.info('    - type:     %s', job['type'])
            logger.info('      tags:     %s', job['tags'])
            logger.info('      title:    %s', job['title'])
            logger.info('      skills:   %s', job['skills'])
            logger.info('      start:    %s', job['start'])
            logger.info('      end:      %s', job['end'])
            logger.info('      company:  %s', job['company'])
            logger.info('      location: %s', job['location'])
            logger.info('      details:')
            for detail in job['detail']:
                logger.info('        - %s', detail)

if __name__ == "__main__":
    fname = './data/data.yaml'
    test = yaml_builder(fname)
    template = template_basic()
    keys = ['programming']
    output = 'test.pdf'
    test.build_resume(template, keys = keys, output = output, display_project_skills=True)