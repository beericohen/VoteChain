import sys
import os
from streamlit.web import cli 

if __name__ == '__main__':
    # מוודא שהנתיב הנוכחי הוא התיקייה של הקובץ הזה (תיקיית הפרויקט)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # מגדיר ל-Streamlit איזה קובץ להריץ
    # שים לב: אנחנו מצביעים על הקובץ הפנימי בתוך app
    sys.argv = ["streamlit", "run", "app/main.py"]
    
    # מריץ את סטרימליט
    sys.exit(cli.main())