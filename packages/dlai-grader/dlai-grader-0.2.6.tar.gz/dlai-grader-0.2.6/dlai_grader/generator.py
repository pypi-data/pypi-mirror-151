import os
from .templates import load_templates

def write_file(filename, template):
    with open(filename, 'w') as f:
        f.write(template)


def init():
    
    dockerfile, makefile, conf = load_templates()
    write_file("./Dockerfile", dockerfile)
    write_file("./Makefile", makefile)
    write_file("./.conf", conf)
    write_file("./requirements.txt", "dlai-grader")
    write_file("./grader.py", "")
    write_file("./entry.py", "")
    os.makedirs("data")
    os.makedirs("learner")
    os.makedirs("mount")
    os.makedirs("solution")
    os.makedirs("submission")
