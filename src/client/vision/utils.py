import os
from datetime import date

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
YML_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'ymls')


def get_latest_yml_path()->str:
    """가장 최근의 YML 파일의 경로를 가져온다.

    :returns str: 가장 최근의 YML 파일의 경로
    """
    if os.path.exists(YML_DIR_PATH) == False:
        os.mkdir(YML_DIR_PATH)
    dates = os.listdir(YML_DIR_PATH)
    dates.sort()
    if len(dates) > 0:
        return os.path.join(YML_DIR_PATH, "{}".format(dates[-1]))
    else:
        return ""



