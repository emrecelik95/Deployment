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
	status = ""
	if(req.method == "POST"):
		print(req.POST)
		properties = req.POST['properties']
		print(properties)
		method = properties['method']
		if (method == "create_job"):
			appName = properties['project_name']
			username = properties['github_login']
			out,status = createApplicationForHTML(appName)
			createDeploymentGroupForHTML(appName,username)
			response = JsonResponse({'description' : out, 'properties' : {'status' : status,'method' : method}})
			return response
		elif(method == "create_dep"):
			appName = properties['project_name']
			commitID = properties['commit_id']
			depGroupName = listDeploymentGroups(appName)['deploymentGroups']
			username = depGroupName
			repo = username + "/" + appName
			out,status = createDeploymentForHTML(appName,depGroupName,repo,commitID)
			response = JsonResponse({'description' : out,'properties':{'method' : method, 
																		'app_info' : {'app_name' : appName,
																					  'app_path' : '/home/ec2-user/apps/' + appName} ,
																	   'machine_info' : {'public_ip' : PUBLIC_IP,
																						 'pem_file' : pemFile,
																						 'usage' : 'chmod 400 imarkett.pem && ssh -i "imarkett.pem" ec2-user@ec2-52-39-172-96.us-west-2.compute.amazonaws.com'
																						  }}})
			print(response.content)
			return response