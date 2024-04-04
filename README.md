# Meraki Scanning API Forwarder to Splunk HEC
## Overview
The purpose of this project is to provide a way to forward Meraki Scanning API data to Splunk's HTTP Event Collector (HEC). 
Provided is a Flask server Python script that provides the required implementation for the Meraki Scanning API integration.

## Architecture Components
Note that Meraki requires an HTTPS endpoint to send the scanning data to, HTTP will not work.
- Domain Name (using Route53 would be easiest, but any domain name provider will work)
  - configure a subdomain to point to the Application Load Balancer domain name
- Application Load Balancer (ALB)
  - configured with HTTPS listener
      - which is configured with a certificate associated with the custom domain name
      - which forwards traffic to the target group
- Target Group of EC2s
    - running the Flask server
    - recommended at least 2 instances for high availability
- Elastic Beanstalk can be used to provision most of these resources
  - See: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
- EB configuration can be used to also store environmental variables, such as the Splunk HEC token.
- Splunk HEC
    - enabled & token generated

## Environment Variables used by the Flask server
- `MERAKI_VALIDATOR` - The validator string that Meraki generates and expects the GET endpoint to return
- `MERAKI_SECRET` - The shared secret string that Meraki will include in JSON request body of requests to the server
Template
```
SPLUNK_HEC_URL=https://xyz.splunkcloud.com:443
SPLUNK_HEC_TOKEN=abc123-abc123-abc123
MERAKI_VALIDATOR=some-validator-string
MERAKI_SECRET=secret-goes-here
```

## Things to note
- `.platform/nginx/conf.d/upload_size.conf` contains a custom nginx config which configure the memory used for request bodies.
  - configure this as needed, as by default nginx limits to 1MB
  - https://repost.aws/knowledge-center/elastic-beanstalk-nginx-configuration

## References
- https://developer.cisco.com/meraki/scanning-api/overview/#receiver-endpoints
- Sample server implementation (without HEC integration) https://github.com/dexterlabora/cmxreceiver-python
- https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.html
- https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html
- https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/UsetheHTTPEventCollector

