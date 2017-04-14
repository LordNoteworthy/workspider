Automate Job Application ...

### Setup
- sudo apt-get install libffi-dev libssl-dev libxml2-dev libxslt1-dev libpq-dev
- sudo apt-get install postgresql postgresql-contrib
- git clone git@github.com:LordNoteworthy/workspider.git
- pip install -r requirements.txt


### Setup Database
- sudo -u postgres psql postgres
- CREATE USER workspider_user WITH PASSWORD 'workspider_pass';
- CREATE DATABASE workspider_db;
- GRANT ALL PRIVILEGES ON DATABASE workspider_db to workspider_user;
- \q


## Deploy the project using scrapyd-client
- Navigate to the root directory: workspider/scraper
- Start scrapyd
- Deploy with scrapyd-deploy
