'''
Next Priority : Let's making something that will make our PDF
    We'll make it barebones to start with : 
        Let's have at most 5 sections:
            - Header, Skills, Work Experience, Relevant Projects, Education 
'''

from fpdf import FPDF

linespace = 6
class template_basic(FPDF):
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
                    'skills' : string, (optional)
                } 
            }

            skills = {
                skill_1 : string,
                skill_2 : string,
                skill_3 : string,..., 
                skill_n : string
            }
    '''
    def head(self, name, address):
        self.set_font(self.font, 'B', self.title_font_size)
            
        # Calculate width of title and position
        w = self.get_string_width(name) + 6
        self.set_x((210 - w) / 2)
        
        # Title
        self.set_text_color(66, 81, 245)
        self.cell(w, 7, txt = name, align = 'C', new_y = 'NEXT')

        
        ## Subsection Font

        self.set_text_color(39, 39, 46)
        self.ln(0.5)
        self.set_font(self.font, size = self.body_font_size)

        # if type(address) is str: 
        #     # w = self.get_string_width(address) + 6
        #     # self.set_x((210 - w) / 2)
        #     self.cell(0, 5, txt = address, align = 'C', new_y = "NEXT", new_x = "LMARGIN", markdown=True)
        if type(address) is list:
            bullet = ' **\u00b7** '
            address = bullet.join(address)
        self.cell(0, 5, txt = address, align = 'C', new_y = "NEXT", new_x = "LMARGIN", markdown=True)
        # elif type(address) is dict:
        #     for key in address:
        #         self.set_font(self.font, 'B', self.body_font_size)
        #         self.cell(0, )
        #         print(key)
        ## Divider
        # x = self.get_x()
        # y = self.get_y()
        # self.line(x, y+2, 195, y+2)
        # self.ln(2)
        
    def section_header(self, header):
        self.set_font(self.font, size = self.header_font_size)
        self.ln(1)
        # Background color
        self.set_fill_color(255, 255, 255)
        self.set_text_color(66, 81, 245)
        
        # Title
        self.cell(0, linespace, header, align = 'L', new_x = "LMARGIN", new_y = "NEXT", markdown=True)
        x = self.get_x()
        y = self.get_y()
        self.line(x, y, 200, y)
        self.ln(1)
        self.set_text_color(39, 39, 46)

    def skills(self, skills): 
        header = '**Skills**'
        self.section_header(header)
        for skill in skills:
            self.set_font(self.font, 'B', self.body_font_size)
            #self.set_x(15)
            
            self.cell(0, linespace, skill + ': ', align = 'L', new_x = "END")
            self.set_font(self.font, '', self.body_font_size)
            #w = self.get_string_width(skill)
            #self.set_x(w + 12)
            skill_string = ', '.join(skills.get(skill))
            self.multi_cell(0, linespace, skill_string, new_x = "LMARGIN", new_y = "NEXT", align = 'L')
        self.ln(1)
        
    def work_exp(self, w_exp):
        header = '**Professional Experience**'
        self.section_header(header)
        
        for company in w_exp:
            info = w_exp.get(company)
            date_location = info.get('location') + ', ' + info.get('date') 
            title = info.get('title')
            self.set_font(self.font, 'B', self.body_font_size)
            
            self.cell(0, linespace, title, align = 'L', new_y = "NEXT", new_x="LMARGIN")
            self.cell(0, linespace-1, company, align = 'L')
            self.set_font(self.font, size = self.body_font_size)
            self.cell(0, linespace-1, txt = date_location, align = 'R', new_x = "LMARGIN", new_y = "NEXT", markdown = True)
            self.set_font(self.font,size= self.body_font_size)
            for detail in info.get('detail'):
                self.set_x(self.get_x() + 5)
                self.multi_cell(0, linespace, txt = ('\u00b7 '+detail), align = 'L', new_y = "NEXT", new_x = "LMARGIN", markdown=True)
            self.ln(.5)

        self.ln(1)

    def proj_exp(self, p_exp):
        header = '**Relevant Projects**'
        self.section_header(header)

        for project in p_exp:
            info = p_exp.get(project)
            date = info.get('date')
            self.set_font(self.font, 'B', self.body_font_size)
            if date is None:
                date = ''
            self.cell(0, linespace, project, align = 'L', new_x = "END") # Project Title
            self.set_font(self.font, 'I', self.body_font_size-2)
            if info.get('skills'):
                skills = '(Skills: ' + info.get('skills') + ')'
                self.cell(0, linespace, skills, align = 'L')
            self.set_font(self.font, size = self.body_font_size)
            self.cell(0, linespace, txt = date, align = 'R', new_x = "LMARGIN", new_y = "NEXT", markdown = True)
            self.set_font(self.font, size = self.body_font_size)

            for detail in info.get('detail'):
                self.set_x(self.get_x() + 5)
                self.multi_cell(0, linespace, txt = ('\u00b7 '+detail), align = 'L', new_y = "NEXT", new_x = "LMARGIN", markdown=True)
            self.ln(.5)
        self.ln(1)

    def education(self, education):
        header = '**Education**'
        self.section_header(header)
        
        for degree in education:
            self.set_font(self.font, 'B', self.body_font_size)
            #self.set_x(15)
            self.cell(0, linespace, degree, new_x = "END", new_y = "NEXT", align = 'L')
            self.set_font(self.font, '', self.body_font_size)
            #self.set_x(15)
            degree_info = education.get(degree)
            address = degree_info.get('address')
            date = degree_info.get('completed')
            gpa = degree_info.get('GPA')
            self.cell(0, linespace, date + ' | '+ gpa, new_x = "LMARGIN", align = 'R')
            self.cell(0, linespace, address , new_x = "LMARGIN", new_y = "NEXT", align = 'L')

        self.ln(1)
    
    def fill_resume(self, name, address, skills, w_exp, edu, p_exp = None, header_font_size = 12, body_font_size = 10.5, title_font_size =20, font = 'Helvetica'):
        self.header_font_size = header_font_size
        self.body_font_size = body_font_size
        self.title_font_size = title_font_size
        self.font = font

        self.add_page()
        self.head(name, address)
        self.education(edu)
        self.skills(skills)
        if p_exp: 
            self.proj_exp(p_exp)
        self.work_exp(w_exp)
        
if __name__=="__main__":
    pass