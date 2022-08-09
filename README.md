# New Update : Accept yaml file inputs
  - See ./data/templates/sample.yaml or my./data/data.yaml to see how to set up

# resume_builder
  Remember what it was like to go job hunting for the first time? You know how they told you to "tailor your resume to the position"?  
  Well, this project was meant to do just that! I created this to "simplify" the process. Basically, this requires 3 csvs: 
  - basic_info.csv: 
    - database that contains your: name, edu_1, edu_2, address
   - experience.csv:  
    - a database of all of your jobs & projects that you've worked on, including the tags that identify them
   - skills.csv:  
    - contains your skills and how you want to sort them  
      - in my case I have Programming Languages, Software & Skills, and Technical Skills  
    # OR 
    - Have a yaml that follows the same key arguments as shown in ./data/templates/sample.yaml

 ## What's in this directory?
  - templates.py 
    - Contains my resume templates  
      - Only has 1 template. Hopefully we'll have more built in the future  
  - builder.py  
    - This is the bulk of the operations where we pull the necessary information from our csvs.  
    - bulk of the calculations are done in builder class. 

  - main.py
    - Use this to run in terminal
  
 ## How to run:  
 Follow the templates in ./data/template
  - if using CSV:
    -requires 3 csvs labeled experience, skills, basic_info

 inputs:  
 - start by running : `python main.py -i path/to/yaml.yaml or path/to/csv1-3.csv -k [search keys] -t template_type(basic only)`

## Future Updates
  - Implement Unsupervised Classification Models
    - I want to improve how I choose which experiences to be put on resumes based off of key search terms, so that search terms with the highest score will appear on the resume. 
      - Currently looking at the skill2vec model (based off of word2vec), proposed b Duyet Le, follow his repository here:
        - https://github.com/duyet/skill2vec 