
# one_task.py

DOIT_CONFIG = {
    'default_tasks': ['build_docker_image']
    }

def task_build_docker_image():
    """Build the docker image"""
    return {
        'file_dep': ['SwissMeteoBot.py', 'Dockerfile', 'requirements.txt'],
        'actions': ['docker build -t "swissmeteobot" .'],
    }

def task_save_docker_image():
    """Build the docker image"""
    return {
        'targets': ['Image-SwissMeteoBot.tgz'],
        'actions': ['docker save swissmeteobot -o Image-SwissMeteoBot.tgz'],
        'task_dep': ['build_docker_image']
    }

def task_clean_image():
    """ remove docker image """
    return {
 #       'file_dep': ['Image-SwissMeteoBot.tgz'],
        'actions': ['del Image-SwissMeteoBot.tgz']
    }
