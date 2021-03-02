# Bugtracker-REST-API
A simple, minimal bug tracker REST API made using Django and Django REST Framework.

## What is it?

A simple bug tracking REST API made using Django and Django REST Framework. You can use this as a backend for your bug tracking software which you are building. 
This is a kind of bug tracking system which can be used inside an organization or can be hosted on your own. A user can initially register an account and can start creating projects. Each issue may fall under a project.

<img src="https://i.ibb.co/gRnQG6Q/new-1.png" width="50%" />

You can have so many collaborators to a project. And you can assign a particular issue to a single Assignee.

## Features

This backend REST API has the following features:
  
  ### User Management
  
  There are two types of users - Admin, and Staff. All the account registered through the API will be by default "Staff" accounts. If you need to make an "Admin" account, then you can use the Django Special Command.
  Admin has all the power to control and manage the whole app where the Staff has a limited but all needed powers.
  
  To use the bug tracker, the user will need to **Register** an account. If he does so, he will get an **Authorization Token** in return. 
  If he/she already have an account, then they can do **Login** instead. 
  
  ### Project
  
  Once an user account is made, then the user will be able to create **Projects**. Every **Issue** is filed under a Project. So before creating an Issue you need a project.
  
  A project is a representation of your current project you are working on. You can create a project and can file issues under that project. Once a project is made, you are the admin of that project. You can now add collaborators so that more people who have "active" accounts can work on that project.  All the collaborators of the project will be able to do:

    - Add and remove issue(s).
    - Can edit the project name etc.

  Only the person who made the project has the power to delete/update the project and he/she is the one who has the power to add/remove collaborator(s).
  
  ## Issue 
  
  An issue consists of a title (must need), description, link, key, assignee, status, priority, reporter, created_at, due_date, and a related project. An issue is a representation of the real-world problems you encounter in your current project. An issue must be a part of a project.

  The admin/collaborators of the project can create an issue in that project. The person who created that issue can assign it to an "Assignee" from within the collaborators list or leave it "Unassigned". An issue can be updated/deleted only by the person who created it and the person to whom the issue is assigned to. Others can just view the issue.
  
## API Endpoints and HTTP methods

Admin panel - http://localhost:8000/admin/

Other Endpoints (supported HTTP Methods & URLS):
  
  ```
  - GET  - http://localhost:8000/api/v1/users/me/
  - GET  - http://localhost:8000/api/v1/users/all/
  - POST - http://localhost:8000/api/v1/users/login/
  - POST - http://localhost:8000/api/v1/users/register/
  - GET  - http://localhost:8000/api/v1/users/logout/
  
  - GET, POST         - http://localhost:8000/api/v1/projects/
  - GET, PUT, DELETE  - http://localhost:8000/api/v1/projects/:key/
  - GET, POST         - http://localhost:8000/api/v1/projects/:key/issues/ 
  - GET, PUT, DELETE  - http://localhost:8000/api/v1/projects/:key/issues/:issue_key/ 
  - GET, PUT          - http://localhost:8000/api/v1/projects/:key/collaborators/ 
  ```



