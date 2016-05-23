import sys, os, base64, datetime, hashlib, hmac, urllib
import requests # pip install requests



method = 'GET'
service = 'ec2'
host = 'ec2.eu-central-1.amazonaws.com'
region = 'eu-central-1'
endpoint = 'https://ec2.eu-central-1.amazonaws.com'

access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

if access_key is None or secret_key is None:
    print 'No access key is available.'
    sys.exit()


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning



def send(payload):

   t = datetime.datetime.utcnow()
   amz_date = t.strftime('%Y%m%dT%H%M%SZ') # Format date as YYYYMMDD'T'HHMMSS'Z'
   datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope


   canonical_uri = '/' 

   canonical_headers = 'host:' + host + '\n'
   signed_headers = 'host'

   algorithm = 'AWS4-HMAC-SHA256'
   credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'

   #canonical_querystring = 'Action=RunInstances&DryRun=true&ImageId=ami-d3c022bc&InstanceType=t2.micro&MaxCount=1&MinCount=1'
   canonical_querystring = payload
   canonical_querystring += '&Version=2013-10-15'
   canonical_querystring += '&X-Amz-Algorithm=AWS4-HMAC-SHA256'
   canonical_querystring += '&X-Amz-Credential=' + urllib.quote_plus(access_key + '/' + credential_scope)
   canonical_querystring += '&X-Amz-Date=' + amz_date
   canonical_querystring += '&X-Amz-Expires=30'
   canonical_querystring += '&X-Amz-SignedHeaders=' + signed_headers

   payload_hash = hashlib.sha256('').hexdigest()

   canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash


   string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()


   signing_key = getSignatureKey(secret_key, datestamp, region, service)

   signature = hmac.new(signing_key, (string_to_sign).encode("utf-8"), hashlib.sha256).hexdigest()


   canonical_querystring += '&X-Amz-Signature=' + signature


   request_url = endpoint + "?" + canonical_querystring

   #print '\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++'
   #print 'Request URL = ' + request_url
   r = requests.get(request_url)

   #print '\nRESPONSE++++++++++++++++++++++++++++++++++++'
   #print 'Response code: %d\n' % r.status_code
   return r.text
