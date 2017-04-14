# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Jobs, db_connect, create_jobs_table
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, log
from smtplib import SMTPAuthenticationError
import os


class JobsPipeline(object):

    """job pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_jobs_table(engine)
        self.Session = sessionmaker(bind=engine)

        # To redefine spider_closed method:
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        """Save deals in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()
        job = Jobs(**item)

        try:
            session.add(job)
            session.commit()
            log.msg('-> Adding new entry : %s !' % job.name, level=log.INFO)
            if job.email is not None:
                #self.send_mail_offer(item)
                job.processed = True
                session.commit()

        except IntegrityError:
            session.rollback()
            q = session.query(Jobs).filter_by(url=item['url']).first()
            if q and (q.processed is False) and (item['email'] is not None):
                log.msg('-> Duplicate entry found : %s not processed !' % item['name'], level=log.INFO)

                # Tryping to send again the mail
                #self.send_mail_offer(item)

                # Update processing
                session.query(Jobs).filter(Jobs.url == item["url"]).update({'processed': True})
                session.commit()
                session.close()

        except SMTPAuthenticationError:
            log.msg('Something wrong with Gmail server !' % job.name, level=log.INFO)
            session.rollback()
            raise

        finally:
            session.close()
        return item

    def send_mail_user(self, item):
        from comm.email_utils import EmailConnection, Email

        name = ''
        email = ''
        password = ''
        mail_server = 'smtp.gmail.com:587'
        to_email = ''
        to_name = ''
        subject = item["name"]
        message = item["url"]

        print 'Connecting...'
        server = EmailConnection(mail_server, email, password)
        print 'Preparing the email...'
        email = Email(from_='"%s" <%s>' % (name, email), #you can pass only email
                      to='"%s" <%s>' % (to_name, to_email), #you can pass only email
                      subject=subject, message=message, attachments=None)
        print 'Sending...'
        server.send(email)
        print 'Disconnecting...'
        server.close()
        print 'Done!'

    def send_mail_offer(self, item):
        from comm.email_utils import EmailConnection, Email

        name = 'O'
        email = ''
        password = ''
        mail_server = 'smtp.gmail.com:587'
        to_email = item["email"]
        to_name = ''
        subject = "Candidature pour " + item["name"]
        message = Motivation

        my_cv = '.pdf'
        file_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(file_path, 'data', my_cv)

        log.msg('Connecting to server...', level=log.INFO)
        server = EmailConnection(mail_server, email, password)
        log.msg('Preparing the email...', level=log.INFO)
        email = Email(from_='"%s" <%s>' % (name, email), #you can pass only email
                      to='"%s" <%s>' % (to_name, to_email), #you can pass only email
                      subject=subject, message=message, attachments=file_path)
        log.msg('Sending...', level=log.INFO)
        server.send(email)
        log.msg('Disconnecting...', level=log.INFO)
        server.close()
        log.msg('Done!', level=log.INFO)

    def spider_closed(self, spider):
        log.msg('%s spider finished !' % spider.name, level=log.INFO)