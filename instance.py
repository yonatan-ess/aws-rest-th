#from connect import send
import os
import time
import xmltodict


class Instance:
	name=None
	key=None
	#dns_name=None
	dns_type=None
	public_dns=None
	instance_id=None
	env="PROD" ##
	role="WEB" ##
	image_id="ami-d3c022bc"
	instance_type="t2.micro"
	hosted_zone_id = "Z21OQMG1B2VN8O"
	instance_status=0
	number_of_instance=1	


	def runInstance(self, temp):
		payload  = "Action=RunInstances"
		payload += "&DryRun=true" ##Debug
		payload += "&ImageId=" + self.image_id
		payload += "&InstanceType=" + self.instance_type
		payload += "&MaxCount=1&MinCount=1"
		#r=send(payload)
		#instance_output=xmltodict.parse(r)
		#self.instance_id=instance_output['RunInstancesResponse']['instancesSet']['item']['instanceId']
		#self.checkInstance()
		#self.createTags()
		#self.createDNS(temp)
		self.name += str(temp)
		print self.name + "\n"
			
		

	def checkInstance(self):
		payload  = "Action=DescribeInstanceStatus"
		payload += "&InstanceId.1=" + self.instance_id ###Search for this one
		print self.instance_status
		while self.instance_status != "16" :
			
			time.sleep(3)
			r=send(payload)
			get_status=xmltodict.parse(r)
			try:
				self.instance_status=get_status['DescribeInstanceStatusResponse']['instanceStatusSet']['item']['instanceState']['code']
			except: 
				continue
	
	def createTags(self):
		payload  = "Action=CreateTags" 
		payload += "&ResourceId.1=" + self.instance_id
		payload += "&Tag.1.Key=Name" 
		payload += "&Tag.1.Value=" + self.name
		payload += "&Tag.2.Key=ENV" 
		payload += "&Tag.2.Value=" + self.env
		payload += "&Tag.3.Key=ROLE" 
		payload += "&Tag.3.Value=" + self.role
		r=send(payload)

	def createDNS(self,temp):
		import boto3		
		access_key = os.environ.get('AWS_ACCESS_KEY_ID')
		secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
		client = boto3.client('route53', aws_access_key_id=access_key , aws_secret_access_key=secret_key)
			
		cname = self.name + "." +  self.role + "." + self.env + "." + "testzz.com."

		response = client.change_resource_record_sets(
		    HostedZoneId = self.hosted_zone_id,
		    ChangeBatch={
		        'Comment': 'comment',
		        'Changes': [
		            {
		                'Action': 'CREATE',
		                'ResourceRecordSet': {
		                    'Name': cname,
		                    'Region': 'eu-central-1',
		                    'Type': 'CNAME',
		                    'SetIdentifier': 'my_a_record',
				    'TTL': 900,
		                    'ResourceRecords': [
		                        {
		                            'Value': 'www.penguin-it.co.il' #needs to be self.public_dns
		                        },
		                        ],
		                    }
		            },
		            ]
		    }
		)
