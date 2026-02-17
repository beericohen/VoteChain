import os
import sys
# מפנה לתיקייה הראשית של הפרויקט כדי שספינקס ימצא את הקוד
sys.path.insert(0, os.path.abspath('../../'))

project = 'Secure Voting System'
copyright = '2026, Demo Team'
author = 'Demo Team'
release = '2.0'

# רשימת התוספים הנדרשים
extensions = [
    'sphinx.ext.autodoc',       # יצירת תיעוד אוטומטי מהקוד
    'sphinx.ext.napoleon',      # תמיכה בסגנון כתיבה של Google/NumPy
    'sphinx.ext.viewcode',      # קישור לקוד המקור
    'sphinx.ext.autosectionlabel', # אפשרות לקשר לכותרות
    'sphinx_rtd_theme',         # ערכת הנושא היפה
]

# הגדרת ערכת הנושא
html_theme = 'sphinx_rtd_theme'

# הגדרות נוספות לתצוגה
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
}