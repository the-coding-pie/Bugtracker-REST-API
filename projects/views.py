from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProjectSerializer, ProjectCreateSerializer
from rest_framework import serializers
from .models import Project
from users.serializers import UserSerializer
from users.models import User
from issues.serializers import IssueSerializer, IssueCreateSerializer
from issues.models import Issue

# projects

# All projects
# GET, POST /api/v1/projects/
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def projects(request):
    try:
        if request.method == 'GET':
            # combines both the queries and eliminates the duplicates.
            projects = (request.user.projects.all() | request.user.project_set.all()).distinct()
            return Response({
                'projects': ProjectSerializer(projects, many=True, context={"request": request}).data
            }, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            # create a project
            serializer = ProjectCreateSerializer(data=request.data)
            if serializer.is_valid():
                project = serializer.save(lead=request.user)
                return Response({
                    "project": ProjectSerializer(Project.objects.get(key=project.key), context={"request": request}).data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({
            'detail': 'Oops, something went wrong.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# A project
# GET, PUT, DELETE /api/v1/projects/<slug:key>/
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def project(request, key):
    try:
        project = Project.objects.get(key=key)
        collaborators_list = project.collaborators.all()

        if request.user == project.lead or request.user in collaborators_list:
            if request.method == 'GET':
                # check if he has the rights
                return Response(
                    ProjectSerializer(project, context={"request": request}).data, status=status.HTTP_200_OK)
            elif request.method == 'PUT':
                serializer = ProjectCreateSerializer(project, data=request.data)
                if serializer.is_valid():
                    project = serializer.save()
                    
                    return Response(
                        ProjectSerializer(Project.objects.get(key=project.key), context={"request": request}).data, status=status.HTTP_200_OK
                    )
                return Response({
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            elif request.method == 'DELETE':
                if request.user == project.lead:
                    project.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response({
                    'detail': 'You are not allowed to do that.'
                }, status=status.HTTP_403_FORBIDDEN)
        raise Project.DoesNotExist
        
    except Project.DoesNotExist:
        return Response({
            'detail': 'Project not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({
            'detail': 'Oops, something went wrong.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


# issues

# All issues
# GET, POST /api/v1/projects/<slug:key>/issues/
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def issues(request, key):
    try:
        project = Project.objects.get(key=key)
        collaborators_list = project.collaborators.all()

        if request.user == project.lead or request.user in collaborators_list:
            if request.method == 'GET':
                # check if he has the rights
                return Response({
                    "project": project.key,
                    "issues": IssueSerializer(project.issues.all(), many=True, context={"request": request}).data
                }, status=status.HTTP_200_OK)
            elif request.method == 'POST':
                # create a project
                serializer = IssueCreateSerializer(data=request.data)
                if serializer.is_valid():
                    assignee = User.objects.filter(username=request.data.get('assignee'))
                    if (assignee) and (assignee[0] == project.lead or assignee[0] in collaborators_list):
                        issue = serializer.save(reporter=request.user, project=project)
                    else:
                        issue = serializer.save(reporter=request.user, project=project, assignee=None)
                    return Response({
                        "project": project.key,
                        "issue": IssueSerializer(issue, context={"request": request}).data
                    }, status=status.HTTP_201_CREATED)
                return Response({
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        raise Project.DoesNotExist
        
    except Project.DoesNotExist:
        return Response({
            'detail': 'Project not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({
            'detail': 'Oops, something went wrong.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

# A issue
# GET, PUT, DELETE /api/v1/projects/<slug:key>/issues/<slug:issue_key>/
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def issue(request, key, issue_key):
    try:
        project = Project.objects.get(key=key)
        collaborators_list = project.collaborators.all()

        if request.user == project.lead or request.user in collaborators_list:
            issue = Issue.objects.get(project=project, key=issue_key)

            if request.method == 'GET':
                # check if he has the rights
                # no role
                role = "N"
                if request.user == project.lead or request.user == issue.reporter:
                    # God mode
                    role = "G"
                elif request.user == issue.assignee:
                    # Human mode
                    role = "H"
                return Response({
                    "issue": IssueSerializer(issue, context={"request": request}).data,
                    "role": role
                }, status=status.HTTP_200_OK)
            # update, delete -> project owner, reporter, minor update by assignee
            elif request.method == 'PUT':
                if request.user == project.lead or request.user == issue.reporter or request.user == issue.assignee:
                    # update assignee -> project owner, reporter -> can 
                    # assignee -> only update minor parts
                    serializer = IssueCreateSerializer(issue, data=request.data)
                    if serializer.is_valid():
                        assignee = User.objects.filter(username=request.data.get('assignee'))
                        if (assignee) and (request.user == project.lead or request.user == issue.reporter) and (assignee[0] == project.lead or assignee[0] in collaborators_list):
                            issue = serializer.save()
                        else:
                            issue = serializer.save(assignee=issue.assignee)

                        # check if he has the rights
                        # no role
                        role = "N"
                        if request.user == project.lead or request.user == issue.reporter:
                            # God mode
                            role = "G"
                        elif request.user == issue.assignee:
                            # Human mode
                            role = "H"
                        return Response({
                            "issue": IssueSerializer(Issue.objects.get(key=issue.key), context={"request": request}).data,
                            "role": role
                        }, status=status.HTTP_200_OK)
                    return Response({
                        'details': serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
                return Response({
                    'detail': 'You are not allowed to do that.'
                }, status=status.HTTP_403_FORBIDDEN)
            elif request.method == 'DELETE':
                if request.user == project.lead or request.user == issue.reporter:
                    # delete the issue
                    issue.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response({
                    'detail': 'You are not allowed to do that.'
                }, status=status.HTTP_403_FORBIDDEN)
        raise Project.DoesNotExist
        
    except Project.DoesNotExist:
        return Response({
            'detail': 'Project not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except Issue.DoesNotExist:
        return Response({
            'detail': 'Issue not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({
            'detail': 'Oops, something went wrong.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

# collaborators

# All collaborators
# GET, PUT /api/v1/projects/<slug:key>/collaborators/
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def collaborators(request, key):
    try:
        project = Project.objects.get(key=key)
        collaborators_list = project.collaborators.all()

        if request.method == 'GET':
            # project exists, so...
            # check if current user is the lead or an collaborator
            if request.user == project.lead or request.user in collaborators_list:
                return Response({
                    'collaborators': UserSerializer(collaborators_list, many=True, context={"request": request}).data
                }, status=status.HTTP_200_OK)
            # return 403 Forbidden
            return Response({
                'detail': 'You are not allowed to do that.'
            }, status=status.HTTP_403_FORBIDDEN)

        elif request.method == 'PUT':
            if request.user == project.lead:
                # he can add new people to the collaborators list
                if request.data.get('collaborators'):
                    usernames = request.data.get('collaborators')

                    # remove the lead from the list if exists
                    if request.user.username in usernames:
                        usernames.remove(request.user.username)

                    # remove duplicate usernames
                    if collaborators_list:
                        for collaborator in collaborators_list:
                            for name in usernames:
                                if name == collaborator.username:
                                    usernames.remove(name)
        
                    # fetch those pure new users, if exists
                    if usernames:
                        users = []
                        for name in usernames:
                            user = User.objects.filter(username=name, is_active=True)
                            if user:
                                users.append(user[0])
                        
                        # check if the list is empty or not
                        if users:
                            project.collaborators.add(*users)
                            return Response({
                                'detail': 'New collaborator(s) has been added!'
                            }, status=status.HTTP_201_CREATED)
                       
                        return Response({
                            'detail': 'Sorry Bad request or invalid user(s).'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    return Response({
                                'detail': 'Those user(s) already are a part of this project.'
                            }, status=status.HTTP_409_CONFLICT)
                return Response({
                    'collaborators': [
                        'This field is required and must be a list of usernames.'
                    ]
                }, status=status.HTTP_400_BAD_REQUEST)
            # return 403 Forbidden
            return Response({
                'detail': 'You are not allowed to do that.'
            }, status=status.HTTP_403_FORBIDDEN)
    except Project.DoesNotExist:
        return Response({
            'detail': 'Project not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({
            'detail': 'Oops, something went wrong.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        