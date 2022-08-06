from re import S
import pandas as pd
from templates import *

month = {
    1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June', 7 : 'July', 8 : 'August', 9 : 'September', 10 : 'October', 11 : 'November',12 : 'December'    
}

class resume_builder:
    def __init__(self, fjobs, fskills, flanguage, basic_info):
        self.jobs = pd.read_csv(fjobs)
        self.jobs['start'] = pd.to_datetime(self.jobs['start'])
        self.jobs['end'] = pd.to_datetime(self.jobs['end'])
        self.jobs = self.jobs.sort_values('start', ascending = False)
        self.jobs = self.jobs
        self.jobs.tags = self.jobs.tags.apply(lambda x: x.split(', '))
        self.jobs.detail = self.jobs.detail.apply(lambda x: x.split(', '))
        
        self.skills = pd.read_csv(fskills)
        # for col in self.skills.columns:
        #     self.skills[col] = self.skills[col].apply(lambda x: str(x).split(', '))

        self.language = pd.read_csv(flanguage)
        for col in self.language.columns:
            self.language[col] = self.language[col].apply(lambda x: str(x).split(', '))

        self.basic = pd.read_csv(basic_info)
        self.basic.edu_1 = self.basic.edu_1.apply(lambda x:str(x).split('/ '))
        self.basic.edu_2 = self.basic.edu_2.apply(lambda x:str(x).split('/ '))


    def build_experience(self, tags, max_list = 5):
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
            if not self.display_project_skills:
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
            skill_list=', '.join(skill_list)
            skname = col + ': '
            skills[skname] = skill_list
        return skills
    
    def build_resume(self, template, keys, output, max_experience = 7, max_skills = 4, display_project_skills = False):
        self.display_project_skills = display_project_skills
        name = self.basic.name.item()
        education = {
            self.basic.edu_1.item()[0] : self.basic.edu_1.item()[1],
            self.basic.edu_2.item()[0] : self.basic.edu_2.item()[1]
        }
        address = self.basic.address.item()
        experience = self.build_experience(tags = keys, max_list = max_experience) 
        skills = self.build_skills(max_list=max_skills)
        template.fill_resume(name, address, skills, experience['work'], education, experience['projects'])
        template.output(output)
        print('resume made')

if __name__ == "__main__":
    job_file = './data/experience.csv'
    skill_file = './data/skills.csv'
    language_file = './data/languages.csv'
    basic_info = './data/basic_info.csv'

    #### Template_basic_1
    template_1 = template_basic_1()
    resume = resume_builder(job_file, skill_file, language_file, basic_info)
    key = ['programming']
    fname = 'resume_1.pdf'
    resume.build_resume(template_1, key, fname, max_experience = 7)
    ####

    template_2 = template_basic_2()
    resume_2 = resume_builder(job_file, skill_file, language_file, basic_info)
    fname = 'resume_2.pdf'
    resume_2.build_resume(template_2, key, fname, max_experience = 7, display_project_skills=True)