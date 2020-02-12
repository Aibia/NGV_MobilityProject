import os
from datetime import date

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
YML_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'ymls')


def get_latest_yml_path():
    if os.path.exists(YML_DIR_PATH) == False:
        os.mkdir(YML_DIR_PATH)
    dates = os.listdir(YML_DIR_PATH)
    dates.sort()
    if len(dates) > 0:
        return os.path.join(YML_DIR_PATH, "{}".format(dates[-1]))
    else:
        return ""



