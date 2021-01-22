<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="Girish, from Bootstrap Template">
    <meta name="generator" content="Hugo 0.79.0">
    <title>Ethernet Database</title>

    <link rel="canonical" href="https://getbootstrap.com/docs/5.0/examples/dashboard/">

    

    <!-- Bootstrap core CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">


    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>

    
    <!-- Custom styles for this template -->
    <link href="dashboard.css" rel="stylesheet">
  </head>
  <body>
    
<header class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow">
  <a class="navbar-brand col-md-3 col-lg-2 me-0 px-3" href="#">Eth Database</a>
  <button class="navbar-toggler position-absolute d-md-none collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
    
    <!--
    <form action="/query" method="GET">
      <input type="text" size="100" maxlength="100" name="task">
     <input type="submit" name="save" value="save">
     </form>
    -->
    <form action="/query" method="GET">
      <input class="form-control form-control-dark w-100" size="200" type="text" name="qstring" placeholder="SQL Query" aria-label="Search">
    
    <!--
    <ul class="navbar-nav px-3">
      <li class="nav-item text-nowrap">
        <a class="nav-link" href="#" name="execute">Execute</a>
        <input type="submit" name="execute" value="Execute"> 
      </li>
    </ul>
    -->
    </form>
    
</header>

<div class="container-fluid">
  <div class="row">
    <nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
      <div class="position-sticky pt-3">
        <ul class="nav flex-column">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#">
              <span data-feather="home"></span>
              
            </a>
          </li>
          
        </ul>

        
      </div>
    </nav>

    <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 class="h2">Results</h1>
        
      </div>

      %import sqlite3 as sq3
      %if len(rows) != 0 and isinstance(rows[0], sq3.OperationalError):
        {{rows[0]}}
      %else:
      <div class="table-responsive">
        <table class="table table-striped table-sm">
          <thead>
            <tr>
              %if len(rows) != 0:
                <th>#</th>
                %for index in range(len(rows[0])):
                  <th>{{index+1}}</th>
                %end
              %end  
            </tr>
          </thead>
          <tbody>
            %idx = 1
            %for row in rows:
            <tr>
              <td>{{idx}}</td>
              %for col in row:
                <td>{{col}}</td>
              %end
              %idx = idx + 1
            </tr>
            %end
            
          </tbody>
        </table>
      </div>
      %end

    </main>
  </div>
</div>


    

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>

  </body>
</html>
