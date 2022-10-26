{%- extends 'base.tpl' -%}
{%- block head -%}
<script>
var url_prefix = "{{ url_prefix }}";
</script>
<script src="{{ base_url }}/formgrader/static/js/manage_assignments.js"></script>
<style>
.instruction-head{
  font-weight:600;
  font-family:'Poppins';
}
.panel-body,.panel-group{
  border-top:20px !important;
  background-color:#FFFFFF;
}
.footer {
    margin-left: 15.5vw;
    margin-top: 2vw;
    border-radius: 20px;
    background-color: #5FBEF0;
    height: 3.5vh;
    width: 11vw;
    padding-top: 0.7vh;
}
.footer:hover{
  background-color:#006BB6;
}
.glyphicon-plus {
    color: #FFFFFF;
    margin-left: 1vw;
    margin-right: 0.5vw;
}
.add-assignment{
  border-radius:20px;
  color:#FFFFFF;
  font-weight:600;
  font-size: 1.5vh;
}
.add-assignment:hover{
  text-decoration: none;
  color:#FFFFFF;
}
.panel-default{
  border-color:#5FBEF0; 
  border-radius:20px !important;
}
.panel-heading,.panel-body{
  background-color:#FFFFFF !important;
  border-radius:20px !important; 
}
.panel-title{
  display:flex;
  justify-content:space-between;
}
.modal-content{
  border-radius:20px;
}
.align-middle{
  text-align:left !important;
  font-size:15px;
  font-weight:600;
}
table.form-table > tbody > tr > td {
    text-align: left !important;
    border-top:none;
}
table.form-table > tbody > tr > td>input{
  border: none; 
  border:solid 1px #5FBEF0;
  border-radius:1px;
}
.modal-footer{
  border-top:none;
  text-align:center;
}
.btn-primary {
  color: #fff;
  background-color: #5FBEF0;
  border-radius: 20px;
  width: 100px;
  border: none;
  font-weight: 600;
}
.btn-danger {
  color: #5FBEF0;
  background-color: #ffffff;
  border-color: #5FBEF0;
  border-radius: 20px;
  width: 100px;
}
.modal-title{
  font-size: 20px;
  font-weight: bolder;
}
#save_student_button,#save_course_button{
    position: absolute;
    background: #5FBEF0;
    border-radius: 41vh;
    border-color: #5FBEF0;
    margin: 4vh 0vw 0vh 7vw;
    font-family: 'Poppins';
    font-style: normal;
    font-size: 2vh;
    line-height: 2vh;
    color: white;
    border-block: unset;
    width:6vw;
    height: 4vh;
    border-width: 0.1vw !important;
    border-style: hidden;
}
#cancel_button{
    justify-content: center;
    background: white;
    border-radius: 41vh;
    border-color: #5FBEF0;
    margin: 4vh 0vw 0vh 14vw;
    font-family: 'Poppins';
    font-style: normal;
    font-size: 2vh;
    line-height: 2vh;
    color: #5FBEF0;
    width:6vw;
    height: 4vh;
    position: absolute;
    border-width: 0.1vw !important;
    border-style: double;
}
.select-div::after {
    content: url("https://ik.imagekit.io/iwwbj9so6/Vector_9_c4obhy8x5.png?ik-sdk-version=javascript-1.4.3&updatedAt=1660643960909");
}
.select-div {
	position: relative; 
}
.select-div::after {
    position: absolute;
    top: 3.8vh;
    right: 8vw;
}
.select{
    appearance:none;
    margin: 3vh 0vh 0vh 0vh;
    width: 13vw;height: 3.5vh;
    background: #FFFFFF;
    border: 0.1vw solid #5FBEF0;
    border-radius: 8vh;
    font-family: 'Poppins';
    font-style: normal;
    font-size: 2vh;
    padding: 0vh 0vw 0vh 0.9vw;
}
</style>
{%- endblock -%}

{%- block title -%}
 <style>
  h1{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
  #exportButton{
    width: 9vw;
    border-radius: 2vw;
    border: none;
    margin-right: -19vw;
    background-color: #D2EDFB;
    font-size: 1vw;
    font-weight: 100;
    padding: 0.5vw 1vw 0.5vw 1vw;
  }
  table{
    border-radius:10px;  
  }
  .modal {
  display: none;
  position: fixed;
  z-index: 2; 
  padding-top: 100px;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto; 
  background-color: rgba(0,0,0,0.4); 
}
.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 30%;
  border-radius: 15px;
  height: 30vh;
}
.close {
  color: #000000;
  float: right;
  font-size: 28px;
  font-weight: bold;
}
.close:hover,
.close:focus {
  color: #FF0000;
  text-decoration: none;
  cursor: pointer;
}
  .column-flex{
    display:flex;
    flex-direction: column;
  }
  .row-flex{
    display:flex;
  }
 </style>
  Manage Assignments
    <button id='changeCourseButton'>Change Course</button>
    <div id="changeCourseModal" class="modal">
    	<div class="modal-content">
        	<span class="close">&times;</span>
        	<div class="column-flex">
            <div class="row-flex select-div">
				      <div>
					      <label for="course">Select course</label>
				      </div>
				      <div>
					      <select class="select" id="course-list" name="course" >
						      <option>Course name</option>
					       </select>
				      </div>
            </div>
          	<div class="row-flex">
         		  <div>
			    		  <button type="button" id="change_course_button">Change</button>
		    		  </div>
              <div>
			    		  <button type="button" id="cancel_button">Cancel</button>
		    		  </div>
            </div>
      		</div>
    	</div>
     </div>
{%- endblock -%}

{%- block sidebar -%}
  <li role="presentation" class="active">
  <a href="{{ base_url }}/formgrader/manage_assignments">
  <svg width="20" height="17" viewBox="0 0 20 22" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M3.24796 20.4734C2.95681 21.2609 2.01306 21.6828 1.13963 21.425C0.266502 21.1625 -0.205477 20.3094 0.0856168 19.5266L6.75004 1.52563C7.04171 0.740007 7.98963 0.314851 8.85942 0.576882C9.73442 0.838913 10.2032 1.68829 9.91671 2.47438L3.24796 20.4734ZM13.6094 0.520632C14.5157 0.656569 15.1303 1.42954 14.9792 2.24657L11.6459 20.2484C11.4948 21.0641 10.6355 21.6172 9.724 21.4813C8.81775 21.3453 8.20317 20.5719 8.35421 19.7516L11.6875 1.75344C11.8386 0.936413 12.698 0.384225 13.6094 0.520632ZM18.3334 0.500007C19.2553 0.500007 20 1.17173 20 2.00001V20C20 20.8297 19.2553 21.5 18.3334 21.5C17.4115 21.5 16.6667 20.8297 16.6667 20V2.00001C16.6667 1.17173 17.4115 0.500007 18.3334 0.500007Z" fill="white"/>
  </svg>
  Manage Assignments
  </a>
  </li>
  <li role="presentation">
  <a href="{{ base_url }}/formgrader/gradebook">
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M0.566037 5.85703C0.450021 6.15938 0.548458 6.50039 0.787521 6.72187L2.30979 8.10703C2.27111 8.39883 2.25002 8.69766 2.25002 9C2.25002 9.30234 2.27111 9.60117 2.30979 9.89297L0.787521 11.2781C0.548458 11.4996 0.450021 11.8406 0.566037 12.143C0.720724 12.5613 0.907052 12.9656 1.11799 13.3488L1.28322 13.6336C1.51526 14.0203 1.77541 14.3859 2.06018 14.734C2.27111 14.9836 2.61213 15.0715 2.92151 14.973L4.87971 14.3473C5.3508 14.7094 5.90275 15.0117 6.42658 15.2438L6.86604 17.2512C6.93635 17.5676 7.18244 17.7926 7.50588 17.877C7.99104 17.9578 8.49025 18 9.03166 18C9.50978 18 10.009 17.9578 10.4942 17.877C10.8176 17.7926 11.0637 17.5676 11.134 17.2512L11.5735 15.2438C12.1289 15.0117 12.6492 14.7094 13.1203 14.3473L15.0771 14.973C15.3879 15.0715 15.7307 14.9836 15.9388 14.734C16.2239 14.3859 16.4841 14.0203 16.7161 13.6336L16.8806 13.3488C17.094 12.9656 17.2797 12.5613 17.4354 12.143C17.5493 11.8406 17.4533 11.4996 17.2122 11.2781L15.6913 9.89297C15.73 9.60117 15.75 9.30234 15.75 9C15.75 8.69766 15.73 8.39883 15.6913 8.10703L17.2122 6.72187C17.4533 6.50039 17.5493 6.16289 17.4354 5.85703C17.2797 5.43867 17.0937 5.03438 16.8806 4.65117L16.7165 4.36641C16.4841 3.97969 16.2239 3.61406 15.9388 3.26777C15.7307 3.01641 15.3879 2.92922 15.0771 3.02836L13.1203 3.65273C12.6492 3.28922 12.1289 2.98688 11.5735 2.7573L11.134 0.749883C11.0637 0.430664 10.8176 0.177187 10.4942 0.123398C10.009 0.0422227 9.50979 0 9.00002 0C8.49025 0 7.99104 0.0422227 7.50588 0.123398C7.18244 0.177187 6.93635 0.430664 6.86604 0.749883L6.42658 2.7573C5.90275 2.98688 5.3508 3.28922 4.87971 3.65273L2.92151 3.02836C2.61213 2.92922 2.27111 3.01641 2.06018 3.26777C1.77541 3.61406 1.51526 3.97969 1.28322 4.36641L1.11799 4.65117C0.907052 5.03438 0.720724 5.43867 0.566037 5.85703ZM9.00002 11.8125C7.44611 11.8125 6.18752 10.5539 6.18752 8.96836C6.18752 7.44609 7.44611 6.15586 9.00002 6.15586C10.5539 6.15586 11.8125 7.44609 11.8125 8.96836C11.8125 10.5539 10.5539 11.8125 9.00002 11.8125Z" fill="white"/>
</svg>
Manual Grading</a>
</li>
<!--
  <li role="presentation"><a href="{{ base_url }}/formgrader/manage_students">
  <svg width="20" height="17" viewBox="0 0 20 17" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M13.2362 4.99035L18.2257 5.69425C18.6389 5.7507 18.9862 6.0296 19.1181 6.41144C19.25 6.7966 19.1424 7.21496 18.8438 7.5005L15.2257 10.8939L16.0799 15.7614C16.1493 16.1599 15.9792 16.565 15.632 16.8007C15.2882 17.0364 14.8334 17.0663 14.4618 16.8771L10.0035 14.6027L5.54865 16.8771C5.17365 17.0663 4.71879 17.0364 4.37504 16.8007C4.03129 16.565 3.85768 16.1599 3.9306 15.7614L4.78476 10.8939L1.16601 7.5005C0.867054 7.21496 0.760804 6.7966 0.892054 6.41144C1.02296 6.0296 1.36914 5.7507 1.78546 5.69425L6.77087 4.99035L9.00698 0.596577C9.19101 0.230812 9.5799 -0.00138092 10.0035 -0.00138092C10.4306 -0.00138092 10.8195 0.230812 11.0035 0.596577L13.2362 4.99035Z" fill="white"/>
</svg>
Manage Students</a></li>
-->
{%- endblock -%}

{%- block messages -%}
<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
  <div class="panel panel-default">
    <div class="panel-heading" role="tab" id="headingOne">
      <h4 class="panel-title">
      <span class='instruction-head'>Instructions (click to expand)</span>
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
          <img src='https://ik.imagekit.io/iwwbj9so6/Vector_9_c4obhy8x5.png?ik-sdk-version=javascript-1.4.3&updatedAt=1660643960909'/>
        </a>
      </h4>
    </div>
    <div id="collapseOne" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingOne">
      <div class="panel-body">
        <ol>
          <li>To <b>create</b> an assignment, click the "Add new assignment..." button below.</li>
          <li>To <b>edit assignment files</b>, click on the name of an assignment.</li>
          <li>To <b>edit the assignment metadata</b>, click on the edit button.</li>
          <li>To <b>generate</b> the student version of an assignment, click on the generate button.</li>
          <li>To <b>preview</b> the student version of an assignment, click on the preview button.</li>
          <li><i>(JupyterHub only)</i> To <b>release</b> the assignment to students, click the release button.
          You can "unrelease" an assignment by clicking again, though note some students may have
          already accessed the assignment. <b>Note</b> that for the release button to become
          available, the <code>course_id</code> option must be set in <code>nbgrader_config.py</code>.
          For details, see <a href="http://nbgrader.readthedocs.io/en/stable/configuration/config_options.html">the documentation</a>.</li>
          <li><i>(JupyterHub only)</i> To <b>collect</b> assignments, click the collect button.</li>
          <li>To <b>autograde</b> submissions, click on the number of collected submissions. You must run
          the autograder on the submissions before you can manually grade them.</li>
        </ol>
      </div>
    </div>
  </div>
</div>
{% if windows %}
<div class="alert alert-warning" id="warning-windows">
Windows operating system detected. Please note that the "release" and "collect"
functionality will not be available.
</div>
{% elif exchange_missing %}
<div class="alert alert-warning" id="warning-exchange">
The exchange directory at <code>{{ exchange }}</code> does not exist and could
not be created. The "release" and "collect" functionality will not be available.
Please see the documentation on
<a href="http://nbgrader.readthedocs.io/en/stable/user_guide/managing_assignment_files.html#setting-up-the-exchange">Setting Up The Exchange</a>
for instructions.
</div>
{% elif not course_id %}
<div class="alert alert-warning" id="warning-course-id">
The course id has not been set in <code>nbgrader_config.py</code>. The "release"
and "collect" functionality will not be available. Please see the documentation on
<a href="http://nbgrader.readthedocs.io/en/stable/user_guide/managing_assignment_files.html#setting-up-the-exchange">Setting Up The Exchange</a>
for instructions.
</div>
{% endif %}
{%- endblock -%}

{%- block table_header -%}
<tr class='head-row'>
  <th>Name</th>
  <th class="text-center">Due Date</th>
  <th class="text-center">Status</th>
  <th class="text-center no-sort">Edit</th>
  <th class="text-center no-sort">Generate</th>
  <th class="text-center no-sort">Preview</th>
  <th class="text-center no-sort">Release</th>
  <th class="text-center no-sort">Collect</th>
  <th class="text-center"># Submissions</th>
  <th class="text-center no-sort">Generate Feedback</th>
  <th class="text-center no-sort">Release Feedback</th>
</tr>
{%- endblock -%}

{%- block table_body -%}
<tr>
  <td colspan="11">
    Loading, please wait...
  </td>
</tr>
{%- endblock -%}
{%block foot%}
<div class='footer'>
  <a href="#" onClick="createAssignmentModal();" class='add-assignment'><span class="glyphicon glyphicon-plus" aria-hidden="true"></span>Add new assignment</a>
</div>
{%endblock%}
{%- block script -%}
<script>
  const changeCourseButton = document.getElementById("changeCourseButton");
  const courseModal = document.getElementById("changeCourseModal");
  const closeSpan = document.getElementsByClassName("close")[0];
  const cancel=document.getElementById("cancel_button");
  changeCourseButton.onclick = function() {
    courseModal.style.display = "block";
  }
  cancel.onclick=function(){
    courseModal.style.display="none";	
  }
	closeSpan.onclick = function() {
    courseModal.style.display = "none";
  }
  window.onclick = function(event) {
    if (event.target == modal) {
      courseModal.style.display = "none";
    }
  }
</script>
  
{%- endblock -%}
