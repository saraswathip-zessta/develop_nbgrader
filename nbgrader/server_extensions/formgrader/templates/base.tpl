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
    <link rel="stylesheet"
        href="{{ base_url }}/formgrader/static/components/datatables.net-bs/css/dataTables.bootstrap.min.css">
    <link rel="stylesheet" href="{{ base_url }}/formgrader/static/css/nbgrader.css">
    <script>
        var base_url = "{{ base_url }}";
    </script>
    <style>
        body {
            font-family: 'Poppins', sans-serif !important;
        }

        .jupyter-logo {
            height: 100px;
            width: 100px;
        }

        .col-md-2 {
            width: 12%;
        }

       .col-md-2.sidenav {
            border-radius: 1.5rem !important;
            background: #006BB6;
            width: 14%;
            margin-left: 0.5%;
            padding-top: 0;
            padding-left: 0px !important;
            padding-right: 0px !important;
        }

        svg {
            margin-right: 1%;
        }

        .page-header {
            border-bottom: none;
            padding-left: calc(4vw - 2rem);
        }

        .page-header:nth-of-type(2) {
            padding-left: 0px;
        }

       .table.table-hover {
            box-sizing: border-box;
            border: 0.2rem solid #5FBEF0;
        }

        .nav-stacked li a {
            border-radius: 0px !important;
        }

        .nav-stacked>li>a:hover {
            background-color: #035B99
        }
        
        .nav-stacked>li:nth-last-of-type(1)>a {
            border-bottom-left-radius: 1rem !important;
            border-bottom-right-radius: 1rem !important;
            color: #FFFFFF;
            font-size: 2rem;
            display: flex;
            flex-direction: row;
            justify-content: flex-start;
            align-items: center;
            gap: 1rem;
        }

      .nav-stacked>li:nth-of-type(1)>a {
            border-top-left-radius: 1rem !important;
            border-top-right-radius: 1rem !important;
            color: #FFFFFF;
            font-size: 2rem;
            display: flex;
            flex-direction: row;
            justify-content: flex-start;
            align-items: center;
            gap: 1rem;
        }

      .career-logo {
            width: calc(10vw - 2rem);
            height: 5rem;
        }

        .col-sm-6:nth-of-type(1) {
            display: none;
        }

        .dataTables_filter {
            text-align: left !important;
        }

        .form-control.input-sm {
            border-color: #5FBEF0;
        }

        label {
            font-weight: 900 !important;
            font-size: 1.8rem;
            color: #035B99;
        }

        .col-sm-12 {
            width: 100%;
            margin-top: 1%;
        }

        thead>tr {
            background: #D2EDFB;
        }

        th,
        td {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            text-align: center;
        }

        th {
            font-weight: 600;
        }

        th::after {
            color: #006BB6;
        }

        h1 {
            font-family: 'Poppins' sans-serif !important;
            font-weight: 900;
        }
        @media (max-width: 2560px) {
 		.col-md-2.sidenav {
			width: 11%;
		}
		.career-logo {
		    width: calc(11vw - 2rem);
		    height: 7rem;
		}
		
	}
	@media (max-width: 2304px){
.col-md-2.sidenav {
    width: 12%;
}
}

@media (max-width: 2112px){
.col-md-2.sidenav {
    width: 13%;
}
}

@media (max-width: 1949px){
.col-md-2.sidenav {
    width: 14%;
}
.career-logo {
    width: calc(10vw - 2rem);
    height: 5rem;
}
}
@media (max-width: 1810px){
.col-md-2.sidenav {
    width: 15%;
}
}
@media (max-width: 1700px){
.career-logo {
    height: 4rem;
}
}
@media (max-width: 1689px){
.nav-stacked>li:nth-of-type(1)>a,.nav-stacked>li:nth-last-of-type(1)>a  {
    font-size: 1.8rem;
    }}
    @media (max-width: 1560px){
.nav-stacked>li:nth-of-type(1)>a, .nav-stacked>li:nth-last-of-type(1)>a {
    font-size: 1.6rem;
}}
@media (max-width: 1432px){
.nav-stacked>li:nth-of-type(1)>a, .nav-stacked>li:nth-last-of-type(1)>a {
    font-size: 1.4rem;
}}
@media (max-width: 1303px){
.nav-stacked>li:nth-of-type(1)>a, .nav-stacked>li:nth-last-of-type(1)>a {
    font-size: 1.2rem;
}
}
@media (max-width: 1186px){
.col-md-2.sidenav {
    width: 13%;
}
.nav-stacked>li:nth-of-type(1)>a, .nav-stacked>li:nth-last-of-type(1)>a {
    font-size: 0.97rem;
}
.career-logo {
    height: 3rem;
}


}
@media (max-width: 1183px){
.col-md-2.sidenav {
    width: 14%;
}}
    </style>
    {%- block head -%}
    {%- endblock -%}
</head>

<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2" '>
        <div class="page-header">
        <img src="https://datalab-static-images.s3.ap-south-1.amazonaws.com/career_shaper_logo.png" class='
                career-logo' />
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
            <ul class="nav nav-pills nav-stacked">
                {%- block sidebar -%}
                <li role="presentation"><a href="{{ base_url }}/formgrader/manage_assignments">Manage Assignments</a>
                </li>
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
