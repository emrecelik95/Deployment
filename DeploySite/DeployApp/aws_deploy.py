######  aws configuration #######
global userName
global password
global awsAccessKeyID
global awsSecretKeyID
global region
######  aws configuration #######


####### imports #########
import datetime as dt
import os
import boto3
import yaml
import os
import re
import zipfile
####### imports #########

global client


iam = boto3.resource('iam')
global user

CURRENT_DIR = os.getcwd()

def read(path, loader=None, binary_file=False):
    open_mode = 'rb' if binary_file else 'r'
    with open(path, mode=open_mode) as fh:
        if not loader:
            return fh.read()
        return loader(fh.read())

def readConfig (configFile='config.yaml'):
	pathToConfigFile = os.path.join(CURRENT_DIR,configFile)
	cfg = read(pathToConfigFile,loader = yaml.load)

	global userName
	global password
	global awsAccessKeyID
	global awsSecretKeyID
	global region
	
	userName=cfg.get('userName')
	password=cfg.get('password')
	awsAccessKeyID=cfg.get('awsAccessKeyID')
	awsSecretKeyID=cfg.get('awsSecretKeyID')
	region=cfg.get('region')	

	global user
	user = iam.User(userName)

	global client 
	client = get_client(
            'codedeploy', awsAccessKeyID, awsSecretKeyID, region,
    )

def get_client(client, aws_access_key_id, aws_secret_access_key, region=None):

    return boto3.client(
        client,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )


def getApplication(appName):
	return client.get_application(applicationName=appName)

def listAppRevisions(appName):
	return client.list_application_revisions(applicationName=appName)

def createApplication(appName):
	return client.create_application(applicationName=appName)

def listApplications():
	return client.list_applications()

def listDeployments():
	return client.list_deployments()

def listDeploymentGroups(appName):
	return client.list_deployment_groups(applicationName=appName)

def createDeploymentGroup(appName, depGroupName):#serviceRole = 'arn:aws:iam::586248617556:role/CodeDeployExample'):
	return client.create_deployment_group(applicationName = appName, 
										  deploymentGroupName = depGroupName, 
										  #serviceRoleArn = serviceRole,
										  ec2TagFilters=[
        {
            'Key': 'Name',
            'Value': 'AWS to Github Example',
            'Type': 'KEY_AND_VALUE'
        },
    ],
    serviceRoleArn = 'arn:aws:iam::586248617556:role/CodeDeployExample',
    deploymentStyle= {
        'deploymentType': 'IN_PLACE',
        'deploymentOption': 'WITHOUT_TRAFFIC_CONTROL'
    })

def createDeployment(appName, depGroupName,githubRepo, commitId):
	return client.create_deployment(deploymentGroupName = depGroupName, 
									applicationName = appName,
									deploymentConfigName = 'CodeDeployDefault.OneAtATime',
									revision={
										'revisionType': 'GitHub',
										'gitHubLocation': 
										{
								            'repository': githubRepo,
								            'commitId': commitId
							        	}
									}
								)

def stopDeployment(deploymentID):
	response = client.stop_deployment(deploymentId=deploymentID)
	return response

readConfig()



# -----------------------------------------------

def listDeploymentsIDForHTML():
	try:
		d = listDeployments()
		deploymentsIDList = d['deployments']
		result = ""
		for depID in deploymentsIDList:
			result += depID + "\n"

	except Exception as e:
		return e

	return result


def getApplicationForHTML(appName):
	result = ""
	
	try:
		d = getApplication(appName)
		ID = d['application']['applicationId']
		date = d['application']['createTime']
		result += "ApplicationID : "+ ID + "\n" + "Create Time : " + str (date)
	

	except Exception as e:
		return e
	
	return result

def listAppRevisionsForHTML(appName):
	revType = ""
	commitID = ""
	repo = ""
	try:
		d = listAppRevisions(appName)
		liste = d['revisions']

		for a in liste:
			revType += a['revisionType'] + "\n\n"
			commitID += a['gitHubLocation']['commitId'] + "\n\n" 
			repo += a['gitHubLocation']['repository'] + "\n\n"
	
	except Exception as e:
		return e
	
	return revType, commitID, repo


def createApplicationForHTML(appName):
	result = ""
	try:
		d = createApplication(appName)['applicationId']
		result += "Successful! , ApplicationID : " + d
	except Exception as e:
		return e

	return result


def listApplicationsForHTML():
	result = ""
	try:
		d = listApplications()['applications']
		for a in d:
			result += "- " + a + "\n"

	except Exception as e:
		return e

	return result


def listDeploymentGroupsForHTML(appName):
	result = ""
	try:
		d = listDeploymentGroups(appName)['deploymentGroups']
		for a in d:
			result += a + "\n\n"
	except Exception as e:
		return e

	return result



def createDeploymentForHTML(appName, depGroupName, githubRepo, commitId):
	result = ""
	try:
		d = createDeployment(appName, depGroupName,githubRepo, commitId)['deploymentId']
		result += "Successful! , Deployment ID : " + d + "\n"
	except Exception as e:
		return e

	return result


def createDeploymentGroupForHTML(appName, depGroupName):
	result = ""
	try:
		d = createDeploymentGroup(appName, depGroupName)['deploymentGroupId']
		result += "Successful! , " + "Deployment Group ID :" + str(d) + "\n"
	except Exception as e:
		return e

	return result







