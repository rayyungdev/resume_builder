# resume_builder
  Remember what it was like to go job hunting for the first time? You know how they told you to "tailor your resume to the position"?  
  Well, this project was meant to do just that! I created this to "simplify" the process. Basically, this requires 4 csvs: 
  - basic_info.csv: 
    - database that contains your: name, edu_1, edu_2, address
   - experience.csv:  
    - a database of all of your jobs & projects that you've worked on, including the tags that identify them
   - skills.csv:  
    - contains your skills and how you want to sort them  
      - in my case I have Programming Languages, Software & Skills, and Technical Skills  
   - languages.csv: 
    - (not yet implemented) specify the different libraries / technologie per diferent programming languages  
 
 ## What's in this directory?
  - templates.py 
    - Contains my resume templates  
      - Only has 1 template. Hopefully we'll have more built in the future  
  - builder.py  
    - This is the bulk of the operations where we pull the necessary information from our csvs.  
    - Currently only works with csvs, but I would like to create another method that uses YAML instead  
  - main.py
    - Currently in the works, but I plan to have this run in the terminal. 
  
 ## How to run:  
 Eventually, you'll be able to run this through main.py, but for now, check out what I'm doing in builder.py.  
 You will need your 4 csvs located in the same directory along with template.py
 Make sure you specify the keys and the filename.  
 inputs:  
  - max_experience and max_skills are meant to help you in case you're going over 1 page. 
