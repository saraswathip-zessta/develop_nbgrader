<!doctype html>
<head>
  <title>nbgrader formgrade</title>
  <script src="{{ base_url }}/formgrader/static/components/jquery/jquery.min.js"></script>
  <script src="{{ base_url }}/formgrader/static/components/underscore/underscore-min.js"></script>
  <script src="{{ base_url }}/formgrader/static/components/backbone/backbone-min.js"></script>
  <script src="{{ base_url }}/formgrader/static/components/bootstrap/js/bootstrap.min.js"></script>
  <script src="{{ base_url }}/formgrader/static/components/datatables.net/js/jquery.dataTables.min.js"></script>
  <script src="{{ base_url }}/formgrader/static/components/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>
  <script src="{{ base_url }}/formgrader/static/js/backbone_xsrf.js"></script>
  <script src="{{ base_url }}/formgrader/static/js/utils.js"></script>
  <link rel="stylesheet" href="{{ base_url }}/formgrader/static/components/bootstrap/css/bootstrap.min.css" />
  <link rel="stylesheet" href="{{ base_url }}/formgrader/static/components/datatables.net-bs/css/dataTables.bootstrap.min.css">
  <link rel="stylesheet" href="{{ base_url }}/formgrader/static/css/nbgrader.css">
  <script>
    var base_url = "{{ base_url }}";
  </script>
  <style>
       body{
      font-family: 'Poppins', sans-serif !important;
    }
    .jupyter-logo {
      height: 100px;
      width: 100px;
    }
    .col-md-2{
      width:12%;
    }
    .col-md-2.sidenav{
      border-radius: 8px !important;
      background: #006BB6;
      width: 14%;
      margin-left: 0.5%;
      padding-top: 0px;
      padding-left: 0px !important;
      padding-right: 0px !important;
    }
    svg{
      margin-right:1%;
    }
    .page-header{
      border-bottom:none;
      padding-left: 50px;
    }
    .page-header:nth-of-type(2){
      padding-left:0px;
    }
    .table.table-hover{
      box-sizing: border-box; 
      border: 2px solid #5FBEF0;
    }
    .nav-stacked li a {
      border-radius: 0px !important;
    }
    .nav-stacked>li>a:hover{
      background-color:#035B99
    }
    .nav-stacked>li:nth-last-of-type(1)>a {
      border-bottom-left-radius: 8px !important;
      border-bottom-right-radius: 8px !important;
      color: #FFFFFF;
      font-size: 20px;
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      align-items: center;
      gap: 1rem;
    }
   .nav-stacked>li:nth-of-type(1)>a {
      border-top-left-radius: 8px !important;
      border-top-right-radius: 8px !important;
      color: #FFFFFF;
      font-size: 20px;
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      align-items: center;
      gap: 1rem;
     }
    .career-logo {
      width: 175px;
      height: 50px;
    }
    .col-sm-6:nth-of-type(1){
      display:none; 
    }
    .dataTables_filter{
      text-align:left !important;
    }
    .form-control.input-sm{
      border-radius: 8px;
      width: 250px !important;
      border-color:#5FBEF0;
    }
    label{
      font-weight: 900;
      font-size: 16px;
      color: #035B99;
    }
    .col-sm-12 {
      width: 100%;
      margin-top: 1%;
    }
    thead>tr{
      background:#D2EDFB;   
    }
    th,td{
      padding-left:20px !important;
      padding-right:20px !important;
      text-align:center;
    }
    th{
      font-weight:600;
    }
    th::after{
      color:#006BB6;
    }
    h1{
      font-family:'Poppins' sans-serif !important;
      font-weight:900;
    }
  </style>
  {%- block head -%}
  {%- endblock -%}
</head>
<body>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-2" '>
        <div class="page-header">
        <img src="https://ik.imagekit.io/iwwbj9so6/12bdc9b1-5f78-42fc-957a-6f7e8cf11c96__1__akaDA0tt-.png?ik-sdk-version=javascript-1.4.3&updatedAt=1667113214298" class='career-logo'/>  
        </div>
      </div>
      <div class="col-md-8">
        <div class="page-header">
          <h1>
          {%- block title -%}
          {%- endblock -%}
          </h1>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-2 sidenav">
        <ul class="nav nav-pills nav-stacked" >
          {%- block sidebar -%}
          <li role="presentation"><a href="{{ base_url }}/formgrader/manage_assignments">Manage Assignments</a></li>
          <li role="presentation"><a href="{{ base_url }}/formgrader/gradebook">Gradebook</a></li>
          {%- endblock -%}
        </ul>
      </div>
      <div class="col-md-10">
        {%- block body -%}
        {%- block breadcrumbs -%}
        {%- endblock -%}
        {%- block messages -%}
        {%- endblock -%}
        <table class="table table-hover">
          <thead>
            {%- block table_header -%}
            {%- endblock -%}
          </thead>
          <tbody id="main-table">
            {%- block table_body -%}
            {%- endblock -%}
          </tbody>
          <tfoot>
            {%- block table_footer -%}
            {%- endblock -%}
          </tfoot>
        </table>
        {%- endblock -%}
      </div>
    </div>
  </div>
  {%- block script -%}
  {%- endblock -%}
</body>
{%- block foot -%}
{%- endblock -%}
