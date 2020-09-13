#Software team instructions

####TODO: include Anaconda install, venv creation, pip install, and basic Python tutorials
* Install Python 3.9 from Anaconda and create a virtual environment for this project, if not already done
* Install libraries using pip and *requirements.txt*
* Unless otherwise specified: Use Python (.py) files. MATLAB is ok for graphing/analytics, preferably you will learn some plotting library in python (See: matplotlib, seaborn, plotly, etc.)
* Try to adhere to PEP8. For an introduction see https://docs.python-guide.org/writing/style/
* Do **not** store large datasets in this repo. These files should be sent via Box and stored in a standard format between members, if necessary.

### Preferred libraries:
    * **pathlib** for filepath handling
    * **glob** for iterating over files
    * **wavy** for audio reading/writing
    * **numpy** for general math/data manipulation
    * **pytorch** for deep learning

##To contribute:
2 different folders will contain project code:
* *~/scr/* contains system implementation.
    1. Fork the directory to work locally
    2. Submit your code for review.
    ... I'll hopefully be fast about reviewing and merging your code, but if not we may switch to another method.
    ... If I don't get it reviewed within 24 hours of posting, please DM me over MS Teams
    3. Submit a description of your changes/additions and point to the file/line numbers of interest.
* *~/tests/* contains proof-of-concept type of code and demos
    * Preferably these are given in the form of a jupter notebook (.ipynb)

#Hardware team instructions
####TODO: choose hardware design softwares
* CAD software chosen:
* EDA software chosen:

##To contribute:
*~/cad/* contains the bill of materials and build log that are created throughout the project.
### If you are creating a new part, start at step 1. Otherwise, start at step 4.
    1. Create a folder in the *~/cad/* with the convention "00_00_Part_Name"
    ... First field is sub-assembly number. This is where the part is going to go.
    ... Be sure to include the leading 0's in the part number
    ... This also includes models downloaded from the internet
    2. Update the bill of materials in *~/cad/* with the sub-assembly, part number, part name, date created, link to part_log, and description
    ... See example in bill of materials for reference
    ... New subassembly proposals should be discussed during a meeting, or at least over the team chat
    3. Fork most recently uploaded version of the part
    4. Name file with the convention "00_00_31-08-2020" and work
    ... Fields: (sub-assembly number)_(part number)_**(day)_(month)**_(year)
    5. Post new file in *~/cad/##_##_Part_Name/*
    6. Document changes in the part log (posted in the BOM) with your name and upload time
    ... See example part in  *~/cad/00_00_Part_Example/* for reference
