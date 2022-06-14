# ML_project_1
Machine learning project

creating conda envt

conda create -p venv python==3.7 -y

conda activate venv/

git add.
or
git add <filename>

'''
to ignore file we write .gitignore <filename>
'''


to check git status
'''

git status
'''

to check version

'''
git log

'''
git commit -m "message"

'''
git push origin

'''
git remote -v
build docker image
'''
docker build -t <image_name>:<tagname> .
'''
>Note Image name for docker must be in lowercase

To list docker image
'''
docker images
'''

Run docker image
'''
docker run -p 5000:5000 -e PORT=5000 40bbc85e8ee5
'''

To check running container in docker 
'''
docker ps
'''

To stop docker container
'''
docker stop <container_id>