# Base config for users, spiders should not hardcode any string
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Will be used to create the table name
USER = "some_user"

# Should be the same of all websites
EMAIL = "some_email@gmail.com"

# Should be the same for all websites, should be like ''
PASSWORD = "should_be_like_lachezebi00C"

# Full path of your CV
CV_PATH = "/path/to/your/cv"

# Full path of your letter of motivation
MOTIVATION_PATH = "/path/to/your/motivation/letter"

# Keywords used to grab job offers
KEYWORDS = ["Django", "Python", "Web developer"]







