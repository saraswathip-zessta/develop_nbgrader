from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pandas as pd
from nbgrader.api import Gradebook, MissingEntry
import boto3
scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)

# Create the connection to the database
def instructordatabase():
    with Gradebook('sqlite:///gradebook.db') as gb:
        grades = []

    # Loop over each assignment in the database
        for assignment in gb.assignments:

        # Loop over each student in the database
            for student in gb.students:

                # Create a dictionary that will store information about this student's
                # submitted assignment
                score = {}
                score['max_score'] = assignment.max_score
                score['student'] = student.id
                score['assignment'] = assignment.name

                # Try to find the submission in the database. If it doesn't exist, the
                # `MissingEntry` exception will be raised, which means the student
                # didn't submit anything, so we assign them a score of zero.
                try:
                    submission = gb.find_submission(assignment.name, student.id)
                except MissingEntry:
                    score['score'] = 0.0
                else:
                    score['score'] = submission.score

                grades.append(score)

        # Create a pandas dataframe with our grade information, and save it to disk
        grades = pd.DataFrame(grades).set_index(['student', 'assignment'])
        grades.to_csv('grades.csv')

        s3 = boto3.resource(
            service_name='s3',
            region_name='ap-south-1',
            aws_access_key_id='AKIA6ND6FDTKBRA2VNK7',
            aws_secret_access_key='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'
        )
        s3.Bucket('hcl-datalab').upload_file(Filename='grades.csv', Key='grades.csv')
# scheduler.add_job(instructordatabase, 'cron', hour=16,minute=12)
scheduler.add_job(instructordatabase, 'interval', minutes=2)
# instructordatabase()
