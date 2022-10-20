import json
import os

from tornado import web

from .base import BaseApiHandler, check_xsrf, check_notebook_dir
from ...api import MissingEntry, Gradebook
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pandas as pd
import boto3
from io import StringIO
scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)        
    
class CustomExportHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        with self.gradebook as gb:
            grades = []

    # Loop over each assignment in the database
            for assignment in gb.assignments:

        # Loop over each student in the database
                for student in gb.students:

                # Create a dictionary that will store information about this student's
                # submitted assignment
                    score = {}
                    score['Learner'] = student.id
                    score['Assignment'] = assignment.name
                    score['Max_Score'] = assignment.max_score

                # Try to find the submission in the database. If it doesn't exist, the
                # `MissingEntry` exception will be raised, which means the student
                # didn't submit anything, so we assign them a score of zero.
                    try:
                        submission = gb.find_submission(assignment.name, student.id)
                    except MissingEntry:
                        score['Score'] = 0.0
                    else:
                        score['Score'] = submission.score

                    grades.append(score)
            self.write(json.dumps(grades))

class StatusHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        self.write({"status": True})


class GradeCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        submission_id = self.get_argument("submission_id")
        try:
            notebook = self.gradebook.find_submission_notebook_by_id(submission_id)
        except MissingEntry:
            raise web.HTTPError(404)
        self.write(json.dumps([g.to_dict() for g in notebook.grades]))


class CommentCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        submission_id = self.get_argument("submission_id")
        try:
            notebook = self.gradebook.find_submission_notebook_by_id(submission_id)
        except MissingEntry:
            raise web.HTTPError(404)
        self.write(json.dumps([c.to_dict() for c in notebook.comments]))


class GradeHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, grade_id):
        try:
            grade = self.gradebook.find_grade_by_id(grade_id)
        except MissingEntry:
            raise web.HTTPError(404)
        self.write(json.dumps(grade.to_dict()))

    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def put(self, grade_id):
        try:
            grade = self.gradebook.find_grade_by_id(grade_id)
        except MissingEntry:
            raise web.HTTPError(404)

        data = self.get_json_body()
        grade.manual_score = data.get("manual_score", None)
        grade.extra_credit = data.get("extra_credit", None)
        if grade.manual_score is None and grade.auto_score is None:
            grade.needs_manual_grade = True
        else:
            grade.needs_manual_grade = False
        self.gradebook.db.commit()
        self.write(json.dumps(grade.to_dict()))


class CommentHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, grade_id):
        try:
            comment = self.gradebook.find_comment_by_id(grade_id)
        except MissingEntry:
            raise web.HTTPError(404)
        self.write(json.dumps(comment.to_dict()))

    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def put(self, grade_id):
        try:
            comment = self.gradebook.find_comment_by_id(grade_id)
        except MissingEntry:
            raise web.HTTPError(404)

        data = self.get_json_body()
        comment.manual_comment = data.get("manual_comment", None)
        self.gradebook.db.commit()
        self.write(json.dumps(comment.to_dict()))


class FlagSubmissionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, submission_id):
        try:
            submission = self.gradebook.find_submission_notebook_by_id(submission_id)
        except MissingEntry:
            raise web.HTTPError(404)

        submission.flagged = not submission.flagged
        self.gradebook.db.commit()
        self.write(json.dumps(submission.to_dict()))


class AssignmentCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        assignments = self.api.get_assignments()
        self.write(json.dumps(assignments))


class AssignmentHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, assignment_id):
        assignment = self.api.get_assignment(assignment_id)
        if assignment is None:
            raise web.HTTPError(404)
        self.write(json.dumps(assignment))

    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def put(self, assignment_id):
        data = self.get_json_body()
        duedate = data.get("duedate_notimezone", None)
        timezone = data.get("duedate_timezone", None)
        if duedate and timezone:
            duedate = duedate + " " + timezone
        assignment = {"duedate": duedate}
        assignment_id = assignment_id.strip()
        self.gradebook.update_or_create_assignment(assignment_id, **assignment)
        sourcedir = os.path.abspath(self.coursedir.format_path(self.coursedir.source_directory, '.', assignment_id))
        if not os.path.isdir(sourcedir):
            os.makedirs(sourcedir)
        self.write(json.dumps(self.api.get_assignment(assignment_id)))


class NotebookCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, assignment_id):
        notebooks = self.api.get_notebooks(assignment_id)
        self.write(json.dumps(notebooks))


class SubmissionCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, assignment_id):
        submissions = self.api.get_submissions(assignment_id)
        self.write(json.dumps(submissions))


class SubmissionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, assignment_id, student_id):
        submission = self.api.get_submission(assignment_id, student_id)
        if submission is None:
            raise web.HTTPError(404)
        self.write(json.dumps(submission))


class SubmittedNotebookCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, assignment_id, notebook_id):
        submissions = self.api.get_notebook_submissions(assignment_id, notebook_id)
        self.write(json.dumps(submissions))


class StudentCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        students = self.api.get_students()
        self.write(json.dumps(students))


class StudentHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, student_id):
        student = self.api.get_student(student_id)
        if student is None:
            raise web.HTTPError(404)
        self.write(json.dumps(student))

    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def put(self, student_id):
        data = self.get_json_body()
        student = {
            "last_name": data.get("last_name", None),
            "first_name": data.get("first_name", None),
            "email": data.get("email", None),
        }
        student_id = student_id.strip()
        self.gradebook.update_or_create_student(student_id, **student)
        self.write(json.dumps(self.api.get_student(student_id)))


class StudentSubmissionCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, student_id):
        submissions = self.api.get_student_submissions(student_id)
        self.write(json.dumps(submissions))


class StudentNotebookSubmissionCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, student_id, assignment_id):
        submissions = self.api.get_student_notebook_submissions(student_id, assignment_id)
        self.write(json.dumps(submissions))


class AssignHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id):
        self.write(json.dumps(self.api.generate_assignment(assignment_id)))


class UnReleaseHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id):
        self.write(json.dumps(self.api.unrelease(assignment_id)))


class ReleaseHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id):
        self.write(json.dumps(self.api.release_assignment(assignment_id)))


class CollectHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id):
        self.write(json.dumps(self.api.collect(assignment_id)))


class AutogradeHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id, student_id):
        self.write(json.dumps(self.api.autograde(assignment_id, student_id)))


class GenerateAllFeedbackHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id):
        self.write(json.dumps(self.api.generate_feedback(assignment_id)))


class ReleaseAllFeedbackHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id):
        self.write(json.dumps(self.api.release_feedback(assignment_id)))
#         with self.gradebook as gb:
#             grades = []
#             # Loop over each assignment in the database
#             print(assignment_id)
#             for assignment in gb.assignments:
#                 print(assignment)
#                 print(assignment.id)
#                 if assignment_id==assignment.id:
#                     # Loop over each student in the database
#                     for student in gb.students:
#                         # Create a dictionary that will store information about this student's
#                         # submitted assignment
#                         score = {}
#                         score['Learner'] = student.id
#                         score['Assignment'] = assignment.name
#                         score['Max_Score'] = assignment.max_score
#                         # Try to find the submission in the database. If it doesn't exist, the
#                         # `MissingEntry` exception will be raised, which means the student
#                         # didn't submit anything, so we assign them a score of zero.
#                         try:
#                             submission = gb.find_submission(assignment.name, student.id)
#                         except MissingEntry:
#                             score['Score'] = 0.0
#                         else:
#                             score['Score'] = submission.score

#                         grades.append(score)
#             grades=[{'Max_Score': 12.0, 'Learner': 'sravanthilearner', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner':'learner1-datalab', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'amarnathr', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'rohitkumark', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'shyamb', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'ambikan', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'learner2-datalab', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'learner3-datalab', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'learner4-datalab', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'learner5-datalab', 'Assignment': 'Anagram', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'sravanthilearner', 'Assignment': 'Anagram1', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'learner1-datalab', 'Assignment': 'Anagram1', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'amarnathr', 'Assignment': 'Anagram1', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'rohitkumark', 'Assignment': 'Anagram1', 'Score':0.0}, {'Max_Score': 12.0, 'Learner': 'shyamb', 'Assignment': 'Anagram1', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'ambikan', 'Assignment': 'Anagram1', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'learner2-datalab', 'Assignment': 'Anagram1', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'learner3-datalab', 'Assignment': 'Anagram1', 'Score': 0.0}, {'Max_Score':12.0, 'Learner': 'learner4-datalab', 'Assignment': 'Anagram1', 'Score': 0.0}, {'Max_Score': 12.0, 'Learner': 'learner5-datalab', 'Assignment': 'Anagram1', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'sravanthilearner', 'Assignment': 'LR', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner1-datalab', 'Assignment': 'LR', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'amarnathr', 'Assignment': 'LR', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'rohitkumark', 'Assignment': 'LR', 'Score':0.0}, {'Max_Score': 0.0, 'Learner': 'shyamb', 'Assignment': 'LR', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'ambikan', 'Assignment': 'LR', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner2-datalab', 'Assignment': 'LR', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner3-datalab', 'Assignment': 'LR', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner4-datalab', 'Assignment': 'LR', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner5-datalab', 'Assignment': 'LR', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'sravanthilearner', 'Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score': 3.0,'Learner': 'learner1-datalab', 'Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'amarnathr','Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'rohitkumark', 'Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'shyamb', 'Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score':3.0, 'Learner': 'ambikan', 'Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner2-datalab', 'Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner3-datalab', 'Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner4-datalab', 'Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner5-datalab', 'Assignment': 'LinearReggresion', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'sravanthilearner', 'Assignment': 'LinearReggresion-1', 'Score': 7.0}, {'Max_Score': 7.0, 'Learner': 'learner1-datalab', 'Assignment': 'LinearReggresion-1', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'amarnathr', 'Assignment': 'LinearReggresion-1', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'rohitkumark', 'Assignment': 'LinearReggresion-1', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'shyamb', 'Assignment': 'LinearReggresion-1', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'ambikan', 'Assignment': 'LinearReggresion-1', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner2-datalab', 'Assignment': 'LinearReggresion-1', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner3-datalab', 'Assignment': 'LinearReggresion-1', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner4-datalab', 'Assignment': 'LinearReggresion-1', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner5-datalab', 'Assignment': 'LinearReggresion-1', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'sravanthilearner', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner1-datalab', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'amarnathr', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'rohitkumark', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'shyamb', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'ambikan', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner2-datalab', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner3-datalab', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner4-datalab', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner5-datalab', 'Assignment': 'LinearRegression', 'Score': 0.0}, {'Max_Score': 4.0, 'Learner': 'sravanthilearner','Assignment': 'LinearRegressionExample', 'Score': 2.0}, {'Max_Score': 4.0, 'Learner': 'learner1-datalab', 'Assignment': 'LinearRegressionExample', 'Score': 0.0}, {'Max_Score': 4.0, 'Learner': 'amarnathr', 'Assignment': 'LinearRegressionExample','Score': 0.0}, {'Max_Score': 4.0, 'Learner': 'rohitkumark', 'Assignment': 'LinearRegressionExample', 'Score': 0.0}, {'Max_Score': 4.0, 'Learner': 'shyamb', 'Assignment': 'LinearRegressionExample', 'Score': 0.0}, {'Max_Score': 4.0, 'Learner': 'ambikan', 'Assignment': 'LinearRegressionExample', 'Score': 0.0}, {'Max_Score': 4.0, 'Learner': 'learner2-datalab', 'Assignment': 'LinearRegressionExample', 'Score': 0.0}, {'Max_Score': 4.0, 'Learner': 'learner3-datalab', 'Assignment': 'LinearRegressionExample', 'Score': 0.0}, {'Max_Score': 4.0, 'Learner': 'learner4-datalab', 'Assignment': 'LinearRegressionExample', 'Score': 0.0}, {'Max_Score': 4.0, 'Learner': 'learner5-datalab', 'Assignment': 'LinearRegressionExample', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'sravanthilearner', 'Assignment': 'Plots', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner1-datalab', 'Assignment': 'Plots', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'amarnathr', 'Assignment': 'Plots', 'Score':0.0}, {'Max_Score': 0.0, 'Learner': 'rohitkumark', 'Assignment': 'Plots', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'shyamb', 'Assignment': 'Plots', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'ambikan', 'Assignment': 'Plots', 'Score': 0.0},{'Max_Score': 0.0, 'Learner': 'learner2-datalab', 'Assignment': 'Plots', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner3-datalab', 'Assignment': 'Plots', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner4-datalab', 'Assignment': 'Plots', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner5-datalab', 'Assignment': 'Plots', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'sravanthilearner', 'Assignment': 'Python', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner1-datalab', 'Assignment': 'Python', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'amarnathr', 'Assignment': 'Python', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'rohitkumark', 'Assignment': 'Python', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'shyamb', 'Assignment': 'Python', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'ambikan', 'Assignment': 'Python', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner2-datalab', 'Assignment': 'Python', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner3-datalab', 'Assignment': 'Python', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner4-datalab', 'Assignment': 'Python','Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner5-datalab', 'Assignment': 'Python', 'Score': 0.0}, {'Max_Score': 3.0,'Learner': 'sravanthilearner', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner1-datalab', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'amarnathr', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'rohitkumark', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'shyamb', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'ambikan', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner2-datalab', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score':3.0, 'Learner': 'learner3-datalab', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner4-datalab', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner5-datalab', 'Assignment': 'Statistics', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'sravanthilearner', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner1-datalab', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'amarnathr', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'rohitkumark', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'shyamb', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner':'ambikan', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner2-datalab', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner3-datalab', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner4-datalab', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner5-datalab', 'Assignment': 'Test Aug 9', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'sravanthilearner', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner1-datalab', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'amarnathr', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'rohitkumark', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'shyamb', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'ambikan', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner2-datalab', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner3-datalab', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner4-datalab', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner5-datalab', 'Assignment': 'Test2', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'sravanthilearner', 'Assignment': 'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner1-datalab', 'Assignment': 'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'amarnathr', 'Assignment': 'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'rohitkumark', 'Assignment': 'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'shyamb', 'Assignment': 'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'ambikan', 'Assignment': 'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner2-datalab', 'Assignment': 'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner3-datalab', 'Assignment': 'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner4-datalab', 'Assignment': 'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner5-datalab', 'Assignment':'test', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'sravanthilearner', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner1-datalab', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'amarnathr', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'rohitkumark', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'shyamb', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'ambikan', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner2-datalab', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner3-datalab', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner4-datalab', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner5-datalab', 'Assignment': 'testaug12', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'sravanthilearner', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner1-datalab', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'amarnathr', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'rohitkumark', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'shyamb', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'ambikan', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner2-datalab', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner3-datalab', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner4-datalab', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner5-datalab', 'Assignment': 'Test 10', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'sravanthilearner', 'Assignment':'PythonBasics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner1-datalab', 'Assignment': 'PythonBasics', 'Score': 1.0}, {'Max_Score': 3.0, 'Learner': 'amarnathr', 'Assignment': 'PythonBasics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'rohitkumark', 'Assignment': 'PythonBasics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'shyamb', 'Assignment': 'PythonBasics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'ambikan', 'Assignment': 'PythonBasics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner2-datalab', 'Assignment': 'PythonBasics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner3-datalab', 'Assignment': 'PythonBasics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner4-datalab', 'Assignment': 'PythonBasics', 'Score': 0.0}, {'Max_Score': 3.0, 'Learner': 'learner5-datalab', 'Assignment': 'PythonBasics', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'sravanthilearner', 'Assignment': 'Basic_Python', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner1-datalab', 'Assignment': 'Basic_Python', 'Score': 7.0}, {'Max_Score': 7.0, 'Learner': 'amarnathr', 'Assignment': 'Basic_Python', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'rohitkumark', 'Assignment': 'Basic_Python', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'shyamb', 'Assignment': 'Basic_Python', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'ambikan', 'Assignment': 'Basic_Python', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner2-datalab', 'Assignment': 'Basic_Python', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner3-datalab', 'Assignment': 'Basic_Python', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner4-datalab', 'Assignment': 'Basic_Python', 'Score': 0.0}, {'Max_Score': 7.0, 'Learner': 'learner5-datalab', 'Assignment': 'Basic_Python', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'sravanthilearner', 'Assignment': 'nnnnn', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner1-datalab', 'Assignment': 'nnnnn', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'amarnathr', 'Assignment': 'nnnnn', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'rohitkumark', 'Assignment': 'nnnnn', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'shyamb', 'Assignment': 'nnnnn', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'ambikan', 'Assignment': 'nnnnn', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner2-datalab', 'Assignment': 'nnnnn', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner3-datalab', 'Assignment': 'nnnnn', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner4-datalab', 'Assignment': 'nnnnn', 'Score': 0.0}, {'Max_Score': 0.0, 'Learner': 'learner5-datalab', 'Assignment': 'nnnnn', 'Score': 0.0}]
#         # Create a pandas dataframe with our grade information, and save it to s3 bucket
#             grades = pd.DataFrame(grades).set_index(['Learner', 'Assignment'])
# #             csv_buffer = StringIO()
# #             grades.to_csv(csv_buffer)
#             grades.to_csv('grades.csv')
#             s3 = boto3.resource(
#                 service_name='s3',
#                 region_name='ap-south-1',
#                 aws_access_key_id='AKIA6ND6FDTKBRA2VNK7',
#                 aws_secret_access_key='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'
#             )
#             s3.Bucket('hcl-datalab').upload_file(Filename='grades.csv', Key='grades.csv')       


class GenerateFeedbackHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id, student_id):
        self.write(json.dumps(self.api.generate_feedback(assignment_id, student_id)))


class ReleaseFeedbackHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id, student_id):
        self.write(json.dumps(self.api.release_feedback(assignment_id, student_id)))


default_handlers = [
    (r"/formgrader/api/status", StatusHandler),
    (r"/formgrader/api/customexport",CustomExportHandler),

    (r"/formgrader/api/assignments", AssignmentCollectionHandler),
    (r"/formgrader/api/assignment/([^/]+)", AssignmentHandler),
    (r"/formgrader/api/assignment/([^/]+)/assign", AssignHandler),
    (r"/formgrader/api/assignment/([^/]+)/unrelease", UnReleaseHandler),
    (r"/formgrader/api/assignment/([^/]+)/release", ReleaseHandler),
    (r"/formgrader/api/assignment/([^/]+)/collect", CollectHandler),
    (r"/formgrader/api/assignment/([^/]+)/generate_feedback", GenerateAllFeedbackHandler),
    (r"/formgrader/api/assignment/([^/]+)/release_feedback", ReleaseAllFeedbackHandler),
    (r"/formgrader/api/assignment/([^/]+)/([^/]+)/generate_feedback", GenerateFeedbackHandler),
    (r"/formgrader/api/assignment/([^/]+)/([^/]+)/release_feedback", ReleaseFeedbackHandler),

    (r"/formgrader/api/notebooks/([^/]+)", NotebookCollectionHandler),

    (r"/formgrader/api/submissions/([^/]+)", SubmissionCollectionHandler),
    (r"/formgrader/api/submission/([^/]+)/([^/]+)", SubmissionHandler),
    (r"/formgrader/api/submission/([^/]+)/([^/]+)/autograde", AutogradeHandler),

    (r"/formgrader/api/submitted_notebooks/([^/]+)/([^/]+)", SubmittedNotebookCollectionHandler),
    (r"/formgrader/api/submitted_notebook/([^/]+)/flag", FlagSubmissionHandler),

    (r"/formgrader/api/grades", GradeCollectionHandler),
    (r"/formgrader/api/grade/([^/]+)", GradeHandler),

    (r"/formgrader/api/comments", CommentCollectionHandler),
    (r"/formgrader/api/comment/([^/]+)", CommentHandler),

    (r"/formgrader/api/students", StudentCollectionHandler),
    (r"/formgrader/api/student/([^/]+)", StudentHandler),

    (r"/formgrader/api/student_submissions/([^/]+)", StudentSubmissionCollectionHandler),
    (r"/formgrader/api/student_notebook_submissions/([^/]+)/([^/]+)", StudentNotebookSubmissionCollectionHandler),
]
