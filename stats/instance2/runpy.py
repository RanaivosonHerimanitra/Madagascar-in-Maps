import page_filtering
import getContent
from subprocess import call
if __name__ == '__main__':
    while True:
        page_filtering.search_for_page()
        getContent.append_story_todf()
        call(["python", "getDates.py"])
        call(["python", "getLocation.py"])
