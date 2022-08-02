'''
Next Priority : Let's making something that will make our PDF
    We'll make it barebones to start with : 
        Let's have at most 5 sections:
            - Header, Skills, Work Experience, Relevant Projects, Education 
'''

from fpdf import FPDF

class template_basic_1(FPDF):
    '''
        Default Colors: 
            Headers (Blue) : 66, 81, 245 
            Texts (Grey) : 39, 39, 46
        
        Let's assume that all of our data is going to be thrown in as a dictionary --

        input format: 
            jobs = { 
                company : {
                    'location' : string,
                    'title' : string,
                    'date' : string (month year),
                    'detail' : list },
            }

            projects ={
                project name : {
                    'date' : string (month year), 
                    'detail' : list,
                } 
            }

            skills = {
                skill_1 : string,
                skill_2 : string,
                skill_3 : string,..., 
                skill_n : string
            }
    '''
    
    def head(self, name, address, font = 'Helvetica'):
        self.font = font
        self.set_font(self.font, 'B', 20)
            
        # Calculate width of title and position
        w = self.get_string_width(name) + 6
        self.set_x((210 - w) / 2)
        
        # Title
        self.set_text_color(66, 81, 245)
        self.cell(w, 7, txt = name, align = 'C', new_y = 'NEXT')
        self.set_font(self.font, 'I', 11)
        self.ln(0.5)
        w = self.get_string_width(address) + 6
        self.set_x((210 - w) / 2)
        
        ## Subsection Font
        self.set_text_color(39, 39, 46)
        self.cell(w, 5, address, align = 'C', new_y = "NEXT", new_x = "LMARGIN")
        
        ## Divider
        x = self.get_x()
        y = self.get_y()
        self.line(x, y+2, 195, y+2)
        self.ln(6)
        
    def section_header(self, header):
        self.set_font(self.font, 'B', 16)
        # Background color
        self.set_fill_color(255, 255, 255)
        self.set_text_color(66, 81, 245)
        
        # Title
        self.cell(0, 6, header, align = 'L', new_x = "LMARGIN", new_y = "NEXT")
        x = self.get_x()
        y = self.get_y()
        self.line(x, y, 200, y)
        self.ln(1)
        self.set_text_color(39, 39, 46)

    def skills(self, skills): 
        header = 'Skills'
        self.section_header(header)
        for skill in skills:
            self.set_font(self.font, 'B', 12)
            #self.set_x(15)
            
            self.cell(0, 6, skill, align = 'L', new_x = "END")
            self.set_font(self.font, 'I', 12)
            #w = self.get_string_width(skill)
            #self.set_x(w + 12)
            self.multi_cell(0, 6, skills.get(skill), new_x = "LMARGIN", new_y = "NEXT", align = 'L')
        self.ln(2)
        
    def work_exp(self, w_exp):
        header = 'Professional Experience'
        self.section_header(header)
        
        for company in w_exp:
            info = w_exp.get(company)
            date_location = info.get('date') + ', ' + info.get('location')
            title = info.get('title')
            self.set_font(self.font, 'B', 12)
            
            self.cell(0, 6, title, align = 'L', new_y = "NEXT", new_x="LMARGIN")
            self.cell(0, 6, company, align = 'L')
            self.set_font(self.font, 'I', 12)
            self.cell(0, 6, txt = date_location, align = 'R', new_x = "LMARGIN", new_y = "NEXT")
            self.set_font(self.font, '', 12)
            for detail in info.get('detail'):
                self.set_x(self.get_x() + 5)
                self.multi_cell(0, 6, txt = ('\u00b7 '+detail), align = 'L', new_y = "NEXT", new_x = "LMARGIN")
            
        self.ln(2)

    def proj_exp(self, p_exp):
        header = 'Relevant Projects'
        self.section_header(header)
        for project in p_exp:
            info = p_exp.get(project)
            date = info.get('date')
            self.set_font(self.font, 'B', 12)
            
            self.cell(0, 6, project, align = 'L')
            self.set_font(self.font, 'I', 12)
            self.cell(0, 6, txt = date, align = 'R', new_x = "LMARGIN", new_y = "NEXT")
            self.set_font(self.font, '', 12)
            for detail in info.get('detail'):
                self.set_x(self.get_x() + 5)
                self.multi_cell(0, 6, txt = ('\u00b7 '+detail), align = 'L', new_y = "NEXT", new_x = "LMARGIN")
        self.ln(2)

    def education(self, education):
        header = 'Education'
        self.section_header(header)
        
        for degree in education:
            self.set_font(self.font, 'B', 12)
            #self.set_x(15)
            self.cell(0, 6, degree, new_x = "LMARGIN", new_y = "NEXT", align = 'L')
            self.set_font(self.font, '', 12)
            #self.set_x(15)
            self.cell(0, 6, education.get(degree), new_x = "LMARGIN", new_y = "NEXT", align = 'L')
            self.ln(1.5)

        self.ln(2)
    
    def fill_resume(self, name, address, skills, w_exp, edu, p_exp = None):
        self.add_page()
        self.head(name, address)
        if p_exp: 
            self.proj_exp(p_exp)
        self.work_exp(w_exp)
        self.skills(skills)
        self.education(edu)

class template_basic_2(FPDF):
    '''
        Default Colors: 
            Headers (Blue) : 66, 81, 245 
            Texts (Grey) : 39, 39, 46
        
        Input format is the same as the previous one, but with the subtle change of adding skills to the project
        __________________ Old Data Format _________________________________
        projects ={
            project name : {
                'date' : string (month year), 
                'detail' : list,
                'skills' : string
            } 
        }


    '''
    
    def head(self, name, address, font = 'Helvetica'):
        self.font = font
        self.set_font(self.font, 'B', 20)
            
        # Calculate width of title and position
        w = self.get_string_width(name) + 6
        self.set_x((210 - w) / 2)
        
        # Title
        self.set_text_color(66, 81, 245)
        self.cell(w, 7, txt = name, align = 'C', new_y = 'NEXT')
        self.set_font(self.font, 'I', 11)
        self.ln(0.5)
        w = self.get_string_width(address) + 6
        self.set_x((210 - w) / 2)
        
        ## Subsection Font
        self.set_text_color(39, 39, 46)
        self.cell(w, 5, address, align = 'C', new_y = "NEXT", new_x = "LMARGIN")
        
        ## Divider
        x = self.get_x()
        y = self.get_y()
        self.line(x, y+2, 195, y+2)
        self.ln(6)
        
    def section_header(self, header):
        self.set_font(self.font, 'B', 16)
        # Background color
        self.set_fill_color(255, 255, 255)
        self.set_text_color(66, 81, 245)
        
        # Title
        self.cell(0, 6, header, align = 'L', new_x = "LMARGIN", new_y = "NEXT")
        x = self.get_x()
        y = self.get_y()
        self.line(x, y, 200, y)
        self.ln(1)
        self.set_text_color(39, 39, 46)

    def skills(self, skills): 
        header = 'Skills'
        self.section_header(header)
        for skill in skills:
            self.set_font(self.font, 'B', 12)
            #self.set_x(15)
            
            self.cell(0, 6, skill, align = 'L', new_x = "END")
            self.set_font(self.font, 'I', 12)
            #w = self.get_string_width(skill)
            #self.set_x(w + 12)
            self.multi_cell(0, 6, skills.get(skill), new_x = "LMARGIN", new_y = "NEXT", align = 'L')
        self.ln(2)
        
    def work_exp(self, w_exp):
        header = 'Professional Experience'
        self.section_header(header)
        
        for company in w_exp:
            info = w_exp.get(company)
            date_location = info.get('date') + ', ' + info.get('location')
            title = info.get('title')
            self.set_font(self.font, 'B', 12)
            
            self.cell(0, 6, title, align = 'L', new_y = "NEXT", new_x="LMARGIN")
            self.cell(0, 6, company, align = 'L')
            self.set_font(self.font, 'I', 12)
            self.cell(0, 6, txt = date_location, align = 'R', new_x = "LMARGIN", new_y = "NEXT")
            self.set_font(self.font, '', 12)
            for detail in info.get('detail'):
                self.set_x(self.get_x() + 5)
                self.multi_cell(0, 6, txt = ('\u00b7 '+detail), align = 'L', new_y = "NEXT", new_x = "LMARGIN")
            
        self.ln(2)

    def proj_exp(self, p_exp):
        header = 'Relevant Projects'
        self.section_header(header)

        for project in p_exp:
            info = p_exp.get(project)
            date = info.get('date')
            self.set_font(self.font, 'B', 12)

            self.cell(0, 6, project, align = 'L', new_x = "END") # Project Title
            self.set_font(self.font, 'I', 10)
            skills = '(Skills: ' + info.get('skills') + ')'
            self.cell(0, 6, skills, align = 'L')
            self.set_font(self.font, 'I', 12)
            self.cell(0, 6, txt = date, align = 'R', new_x = "LMARGIN", new_y = "NEXT")
            self.set_font(self.font, '', 12)

            for detail in info.get('detail'):
                self.set_x(self.get_x() + 5)
                self.multi_cell(0, 6, txt = ('\u00b7 '+detail), align = 'L', new_y = "NEXT", new_x = "LMARGIN")
        self.ln(2)

    def education(self, education):
        header = 'Education'
        self.section_header(header)
        
        for degree in education:
            self.set_font(self.font, 'B', 12)
            #self.set_x(15)
            self.cell(0, 6, degree, new_x = "LMARGIN", new_y = "NEXT", align = 'L')
            self.set_font(self.font, '', 12)
            #self.set_x(15)
            self.cell(0, 6, education.get(degree), new_x = "LMARGIN", new_y = "NEXT", align = 'L')
            self.ln(1.5)

        self.ln(2)
    
    def fill_resume(self, name, address, skills, w_exp, edu, p_exp = None):
        self.add_page()
        self.head(name, address)
        if p_exp: 
            self.proj_exp(p_exp)
        self.work_exp(w_exp)
        self.skills(skills)
        self.education(edu)

if __name__=="__main__":
    name = 'Raymond Yung'
    address = 'Philadelphia, PA, 19121 | 516.469.0726 | Raymond.Yung@drexel.edu | https://rayyungdev.github.io'
    skills = {'Programming Languages:': 'Python, Javascript, Matlab, Powershell, C++', 'Software & Tools:' : 'Git, Powershell, Pytorch'}

    ## Let's assume that work experience & projects are list of lists
    exp = {
        'Health Partner Plans' : {'location' : 'Philadelphia, PA', 'title' : 'Privacy and Security Intern', 'date' : 'April 2019 - December 2019', 'detail' : ['Worked with company governance software to manage data access', 'Automated daily reports with Powershell to save manpower', 'Cooperated with IT Staff to promote cybersecurity and role governance within company']}
    }

    edu = {
        'Masters of Science in Electrical Engineering' : 'Drexel University, Philadelphia PA, Completed June 2022, GPA: 3.68',
        'Bachelors of Science in Electrical Engineering' : 'Drexel University, Philadelphia PA, Completed June 2020, GPA: 3.00'
    }

    p_exp = {
        'Resume Builder' : {'date' : 'July 2022 - August 2022', 'detail' : ['Purpose is to create my own resumes based off job intention', 'created a database that is updated with my current history']},
        'Interview Bot' : {'date' : 'July 2022 - Ongoing', 'detail' : ['Purpose is for potential recruiters to interview me', 'Created an interview database that consists of over 100 questions', 'Uses a model for Intent Classification to understand user intention']}
    }
    resume = template_1()
    resume.fill_resume(name, address, skills, exp, edu, p_exp)

    resume.output('template_1.pdf')