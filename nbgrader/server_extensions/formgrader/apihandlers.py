import json
import os
from nbgrader.utils import get_username
from tornado import web
import psycopg2
from pathlib import Path
from .base import BaseApiHandler, check_xsrf, check_notebook_dir
from ...api import MissingEntry, Gradebook
from pytz import utc
import pandas as pd
import boto3
import datetime
from io import StringIO  
import requests

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

#       Custom code to push the grades to grading_data table in Hub database

        release_feedback_api_response=self.api.release_feedback(assignment_id)
        success=release_feedback_api_response['success']
        trainer_username=get_username()
        if(success):
            self.write(json.dumps(release_feedback_api_response))
            with self.gradebook as gb:
                grades = []
                # Loop over each assignment in the database
                for assignment in gb.assignments:
                    if assignment_id==assignment.name:
                        # Loop over each student in the database
                        for student in gb.students:
                            # Create a dictionary that will store information about this student's
                            # submitted assignment
                            score = {}
                            score['Course_Name'] = assignment.course_id
                            score['Trainer'] =  trainer_username
                            score['Learner'] = student.id
                            score['Assignment'] = assignment.name
                            score['Max_Score'] = assignment.max_score
                            score['Date_Time'] = datetime.datetime.now()
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
#                 connect to hub database and push the data to grading_data table
                connection = psycopg2.connect(database="jupyterhub", user="admin", password="hub@123", host="postgresql-dev.jhub.svc.cluster.local", port=5432)
                cur = connection.cursor()
                cur.executemany(""" INSERT INTO 
  grading_data(trainer_username,course_name,assignment_name,learner_username,assignment_max_score,learner_score,released_time_stamp)
                                      VALUES
                                      (%(Trainer)s,%(Course_Name)s,%(Assignment)s,%(Learner)s,%(Max_Score)s, %(Score)s, %(Date_Time)s) """, grades)
                connection.commit()
                cur.close()
        else:
            self.write(json.dumps(release_feedback_api_response))
            
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
#         self.write(json.dumps(self.api.release_feedback(assignment_id, student_id)))

#         Custom code to push the grades to grading_data table in Hub database

        release_feedback_api_response=self.api.release_feedback(assignment_id, student_id)
        success=release_feedback_api_response['success']
        trainer_username=get_username()
        if(success):
            self.write(json.dumps(release_feedback_api_response))
            with self.gradebook as gb:
                grades = []
                # Loop over each assignment in the database
                for assignment in gb.assignments:
                    if assignment_id==assignment.name:
                        # Loop over each student in the database and check for the atching student id:
                        for student in gb.students:
                            if student.id == student_id:
                            # Create a dictionary that will store information about this student's
                            # submitted assignment
                                score = {}
                                score['Course_Name'] = assignment.course_id
                                score['Trainer'] =  trainer_username
                                score['Learner'] = student.id
                                score['Assignment'] = assignment.name
                                score['Max_Score'] = assignment.max_score
                                score['Date_Time'] = datetime.datetime.now()
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
                # connect to hub database and push the data to grading_data table
                connection = psycopg2.connect(database="jupyterhub", user="admin", password="hub@123", host="postgresql-dev.jhub.svc.cluster.local", port=5432)
                cur = connection.cursor()
                cur.executemany(""" INSERT INTO 
  grading_data(trainer_username,course_name,assignment_name,learner_username,assignment_max_score,learner_score,released_time_stamp)
                                      VALUES
                                      (%(Trainer)s,%(Course_Name)s,%(Assignment)s,%(Learner)s,%(Max_Score)s, %(Score)s, %(Date_Time)s) """, grades)
                connection.commit()
                cur.close()  
        else:
            self.write(json.dumps(release_feedback_api_response))
            
            
# Custom API Handlers

# API Handler for switching course for an instructor in Manage Assignments Tab.            
class ChangeCourseHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self,courseName):
        try:
            isCourseDirectory=Path("/home/jovyan/"+courseName).is_dir()
            if not isCourseDirectory:
                path = os.path.join("/home/jovyan", courseName)
                os.mkdir(path)
            configFile=Path("/home/jovyan/nbgrader_config.py")
            if not configFile.is_file():
                configFile=open("/home/jovyan/nbgrader_config.py", "x")
            else:
                configFile=open("/home/jovyan/nbgrader_config.py",'w')
            configFile.write("c = get_config()")
            configFile.write("\n")
            configFile.write("c.CourseDirectory.root = '/home/jovyan/"+courseName+"'")
            configFile.write("\n")
            configFile.write("c.CourseDirectory.course_id='"+courseName+"'")
            configFile.close()
            userName=get_username()
            hubHeaders={
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'Authorization': 'token 1199d73de2bc4d37900e19c6539833e4'
                }
#             serverUrl='https://data-labs.hcl-edtech.com/hub/api/users/'+userName+'/server'
#             stopServerResponse = requests.delete(serverUrl, headers=hubHeaders)
#             if(stopServerResponse.status_code==204):
#                 startServerResponse=requests.post(serverUrl,headers=hubHeaders)
            self.write(json.dumps({'success':True,'userName':userName,'course':courseName}))
        except:
            self.write(json.dumps({'success':False})) 
            
# Custom API Handler for exporting grading data to a CSV for a particular course assignments submissions.  
class CustomExportHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        try:
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
                        score['Course_Name']=assignment.course_id

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
        except:
            pass

default_handlers = [
    (r"/formgrader/api/status", StatusHandler),
    (r"/formgrader/api/customexport",CustomExportHandler),
    (r"/formgrader/api/changecourse/([^/]+)",ChangeCourseHandler),
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
