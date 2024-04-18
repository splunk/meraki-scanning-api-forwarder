# Meraki Scanning API Forwarder to Splunk HEC
## Overview
The Elastic Beanstalk / Python Flask project is to provide a way to forward Meraki Scanning API data to Splunk's HTTP Event Collector (HEC). 
The provided Flask server Python script provides the required implementation for the Meraki Scanning API integration.

## Architecture Components
The following gives a recommended AWS architecture for deploying this project.
This code could also be deployed with another cloud provider that offers similar services.

Note that Meraki Scanning API integration requires an HTTPS endpoint to send the scanning data to, HTTP will not work.
- Application Load Balancer (ALB)
  - configured with HTTPS listener
      - which is configured with a certificate associated with the custom domain name
      - which forwards traffic to the target group
- Target Group of EC2s
    - running the Flask server (`application.py`)
    - recommended at least 2 instances for high-availability
- Elastic Beanstalk can be used to provision the EC2s & ALB
  - See: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
  - The advantage of EB is that the resulting EC2s are preconfigured to use nginx as a reverse proxy to the Flask server
  - EB configuration can also be used to also store the environmental variables required, as listed below.
- Domain Name (using Route53 would be easiest, but any domain name provider will work)
  - configure a subdomain to point to the Application Load Balancer domain name
- Splunk HEC
    - enabled & token generated

## Environment Variables used by the Flask server
- `MERAKI_VALIDATOR` - The validator string that Meraki generates and expects the GET endpoint to return
- `MERAKI_SECRET` - The shared secret string that Meraki will include in JSON request body of requests to the server
- `SPLUNK_HEC_URL` - The URL of the Splunk HEC endpoint
- `SPLUNK_HEC_TOKEN` - The Splunk HEC token

Template
```
SPLUNK_HEC_URL=https://xyz.splunkcloud.com:443
SPLUNK_HEC_TOKEN=abc123-abc123-abc123
MERAKI_VALIDATOR=some-validator-string
MERAKI_SECRET=secret-goes-here
```

## Configure the Meraki environment
https://developer.cisco.com/meraki/scanning-api/enable-scanning-api/#enable-location-api

Update the Meraki configuration to use the HTTPS endpoint of the Application Load Balancer.

API version 3 should be enabled.


## Things to note
 `.platform/nginx/conf.d/upload_size.conf` contains a custom nginx config which configure the memory used for request bodies.
 - configure this as needed, as by default nginx limits to 1MB
 - https://repost.aws/knowledge-center/elastic-beanstalk-nginx-configuration

## Security Considerations
- Configure the ALB to only accept traffic from the Cisco Meraki IP ranges (ask Cisco support for this)

## References
- https://developer.cisco.com/meraki/scanning-api/overview/#receiver-endpoints
- Sample server implementation (without HEC integration) https://github.com/dexterlabora/cmxreceiver-python
- https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.html
- https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html#environments-cfg-softwaresettings-console
- https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html
- https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-api-gateway.html
- https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/UsetheHTTPEventCollector
