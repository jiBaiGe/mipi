import os


def root_path():
    project_path = os.path.dirname(__file__).split("mipi")[0]
    root_path = os.path.join(project_path, "mipi")
    return root_path