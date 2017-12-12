# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import *

from aws_deploy import *

from django.http import JsonResponse

import json

@csrf_protect
def index(request):

	return render(request, 'temp/index.html',{})

@csrf_protect
def createApp(request):
	val = ""
	if(request.method == "POST"):
		get_appName = request.POST["appName"]

		val = createApplicationForHTML(get_appName)

	return render(request, 'temp/createApp.html',{"htmlVal" : val})




@csrf_protect
def listApp(request):
	apps = listApplicationsForHTML()

	return render(request, 'temp/listApp.html',{  "listAppsHTML" : apps })




@csrf_protect
def listDeps(request):
	apps = listDeploymentsIDForHTML()

	return render(request, 'temp/listDep.html',{  "listDepsHTML" : apps })



@csrf_protect
def getApp(request):

	val = ""
	if(request.method == "POST"):
		val = request.POST["appName"]
	
		val = getApplicationForHTML(val)

	return render(request, 'temp/getApp.html',{  "getAppHTML" : val })

@csrf_protect
def listAppRevisions(request):
	revType = ""
	commitID = ""
	repo = ""
	appName = ""
	if(request.method == "POST"):
		appName = request.POST["appName"]
	
		revType, commitID, repo = listAppRevisionsForHTML(appName)

	return render(request, 'temp/listAppRev.html',{  "revTypeHTML" : revType , 
													 "commitIDHTML" : commitID, 
													 "repoHTML" : repo })


@csrf_protect
def listDepGroups(request):
	val = ""

	if(request.method == "POST"):
		val = request.POST["appName"]
	
		val = listDeploymentGroupsForHTML(val)

	return render(request, 'temp/listDepGroup.html',{  "listDepGroupsHTML" : val })



@csrf_protect
def createDep(request):
	apps = ""

	if(request.method == "POST"):
		get_text = request.POST["appName"]
		get_text2 = request.POST["depGroupName"]
		get_text3 = request.POST["githubRepo"]
		get_text4 = request.POST["commitID"]

		apps = createDeploymentForHTML(get_text,get_text2,get_text3,get_text4)

	return render(request, 'temp/createDep.html',{  "depHTML" : apps })


@csrf_protect
def createDepGroup(request):
	apps = ""

	if(request.method == "POST"):
		appName = request.POST["appName"]
		depGroupName = request.POST["depGroupName"]

		apps = createDeploymentGroupForHTML(appName,depGroupName)

	return render(request, 'temp/createDepGroup.html',{  "depGroupHTML" : apps })


@csrf_exempt
def request(req):
	response = ""
	if(req.method == "POST"):
		method = req.POST.get('method',False)
		if (method == "create_job"):
			appName = req.POST.get('project_name',False)
			print(appName)
			out = str(createApplicationForHTML(appName))
			createDeploymentGroupForHTML(appName,"depGroup1")
			print(out)
			response = JsonResponse({'msg':out})
			print(response.content)
			return response
		elif(method == "create_dep"):
			appName = req.POST.get('project_name',False)
			repo = req.POST.get('repo_name',False)
			commitID = req.POST.get('commit_id',False)
			out = str(createDeploymentForHTML(appName,"depGroup1",repo,commitID))
			response = JsonResponse({'msg':out})
			print(response.content)
			return response