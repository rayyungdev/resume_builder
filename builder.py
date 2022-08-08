from re import S
import pandas as pd
from templates import *

month = {
    1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June', 7 : 'July', 8 : 'August', 9 : 'September', 10 : 'October', 11 : 'November',12 : 'December'    
}

class resume_builder:
    def __init__(self, fjobs, fskills, basic_info):
        self.jobs = pd.read_csv(fjobs)
        self.jobs['start'] = pd.to_datetime(self.jobs['start'])
        self.jobs['end'] = pd.to_datetime(self.jobs['end'])
        self.jobs = self.jobs.sort_values('start', ascending = False)
        self.jobs.tags = self.jobs.tags.apply(lambda x: x.split(', '))
        self.jobs.detail = self.jobs.detail.apply(lambda x: x.split(', '))
        
        self.skills = pd.read_csv(fskills)
        # for col in self.skills.columns:
        #     self.skills[col] = self.skills[col].apply(lambda x: str(x).split(', '))

        # self.language = pd.read_csv(flanguage)
        # for col in self.language.columns:
        #     self.language[col] = self.language[col].apply(lambda x: str(x).split(', '))

        self.basic = pd.read_csv(basic_info)
        self.basic.edu_1 = self.basic.edu_1.apply(lambda x:str(x).split('/ '))
        self.basic.edu_2 = self.basic.edu_2.apply(lambda x:str(x).split('/ '))
    def build_experience(self, tags, max_list = 5, display_project_skills = False):
        '''
            we'll use this section to build our experience section in the resume
        '''
        
        # Choose all experience that contains at least 1 of the listed tags
        job_lookup = self.jobs[self.jobs.tags.apply(lambda x: any(k in x for k in tags))]
        company_list = job_lookup[job_lookup.type == 'J'].company.to_list()
        experience = dict()
        work = dict() #will get put in experience later        
        count = 1
        for company in company_list:
            if count > max_list :
                experience.update({'work': work})
                return experience
            
            count += 1
            row = job_lookup[job_lookup.company == company]
            start_date = month[pd.to_datetime(row.start).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.start).dt.year.astype(str).item()
            end_date = month[pd.to_datetime(row.end).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.end).dt.year.astype(str).item()
            
            work[company] = {
                'location' : row.location.item(), 
                'title' : row.title.item(), 
                'date' : start_date + ' - ' + end_date,
                'detail' : row.detail.item()
            }
            
        experience['work'] = work
        projects = dict() #will get put in experience later
        project_list = job_lookup[job_lookup.type == 'P'].title.to_list()

        for project in project_list:
            if count > max_list : 
                 break
            count +=1
            row = job_lookup[job_lookup.title == project]
            start_date = month[pd.to_datetime(row.start).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.start).dt.year.astype(str).item()
            try:
                end_date = month[pd.to_datetime(row.end).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.end).dt.year.astype(str).item()
            except: 
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
        experience['projects'] = projects
        return experience
                
    def build_skills(self, max_list = 5):
        ## May implement some classification algorithm in the future
        skills = dict()
        count = 1
        for col in self.skills.columns:
            skill_list = self.skills[col].item().split(', ')
            if len(skill_list) > max_list:
                while(len(skill_list) > max_list):
                    skill_list.pop(-1)
            skills[col] = skill_list
        return skills
    
    def build_resume(self, template, keys, output, max_experience = 7, max_skills = 4, display_project_skills = False):
        name = self.basic.name.item()
        education = {
            self.basic.edu_1.item()[0] : 
            {
                'address':self.basic.edu_1.item()[1], 
                'completed': self.basic.edu_1.item()[2],
                'GPA': self.basic.edu_1.item()[3]

            },
            self.basic.edu_2.item()[0] : 
            {
                'address': self.basic.edu_2.item()[1],
                'completed': self.basic.edu_2.item()[2],
                'GPA': self.basic.edu_2.item()[3]
            }
        }
        address = self.basic.address.item()
        experience = self.build_experience(tags = keys, max_list = max_experience, display_project_skills= display_project_skills) 
        skills = self.build_skills(max_list=max_skills)
        template.fill_resume(name, address, skills, experience['work'], education, experience['projects'])
        template.output(output)
        print('resume made')

import yaml

class yaml_builder: 
    def __init__(self, fname):
        with open (fname, 'r') as f:
            self.data = yaml.safe_load(f)
    
    def build_skills(self, key_search = None, max_list = 5):
        # for skill in self.data['skills']:
        #     print(self.data['skills'].get(skill))
        return self.data['skills']
    
    def build_experiences(self, tags, max_list = 7, display_project_skills = False):
        experience_df = pd.DataFrame.from_dict(self.data['experience'], orient='index' )
        experience_df ['start'] = pd.to_datetime(experience_df ['start'])
        experience_df ['end'] = pd.to_datetime(experience_df['end'])
        experience_df  = experience_df.sort_values('start', ascending = False)

        job_lookup = experience_df[experience_df.tags.apply(lambda x: any(k in x for k in tags))]

        company_list = job_lookup[job_lookup.type == 'J'].company.to_list()
        experience = dict()
        work = dict() #will get put in experience later        
        count = 1
        for company in company_list:
            if count > max_list :
                experience.update({'work': work})
                return experience
            
            count += 1
            row = job_lookup[job_lookup.company == company]
            start_date = month[pd.to_datetime(row.start).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.start).dt.year.astype(str).item()
            end_date = month[pd.to_datetime(row.end).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.end).dt.year.astype(str).item()
            
            work[company] = {
                'location' : row.location.item(), 
                'title' : row.title.item(), 
                'date' : start_date + ' - ' + end_date,
                'detail' : row.detail.item()
            }
            
        experience['work'] = work
        projects = dict() #will get put in experience later
        project_list = job_lookup[job_lookup.type == 'P'].title.to_list()

        for project in project_list:
            if count > max_list : 
                 break
            count +=1
            row = job_lookup[job_lookup.title == project]
            start_date = month[pd.to_datetime(row.start).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.start).dt.year.astype(str).item()
            try:
                end_date = month[pd.to_datetime(row.end).dt.month.astype(int).item()] + ' ' + pd.to_datetime(row.end).dt.year.astype(str).item()
            except: 
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
        experience['projects'] = projects
        return experience

    def build_resume(self, template, keys, output, max_experience = 7, max_skills = 4, display_project_skills = False):
        name = self.data['name']
        address = self.data['subheader_info']
        education = self.data['education']

        skills = self.build_skills()
        experience = self.build_experiences(tags = keys, display_project_skills=display_project_skills)
        skills = self.build_skills(max_list=max_skills)
        template.fill_resume(name, address, skills, experience['work'], education, experience['projects'])
        template.output(output)
        print('resume made')
if __name__ == "__main__":
    fname = './data/data.yaml'
    test = yaml_builder(fname)
    template = template_basic()
    keys = ['programming']
    output = 'test.pdf'
    test.build_resume(template, keys = keys, output = output, display_project_skills=True)