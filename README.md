Dash Button Multi-Tool
=======
<br>
This script allows you to listen for ARP requests for older Dash buttons and do
stuff. By doing stuff I mean run commands, make web requests, etc. 

Installation
------------
Not going to spend alot of time here. This script is super hacky, so edit as
you see fit. Goal was to have it trigger once - which means there's a 60 second
threshold since there may be multiple ARP requests per button press.  So if you
want something to go on/off quickly, then you shouldn't be using a Dash button. 

For SmartThings integration, you need to make use of
[OpenDash](https://github.com/open-dash) - which is completely unrelated to
Dash buttons, but this essentially exposes all of your devices to have
endpoints you can remotely call. 

Assuming you want to do SmartThings, install OpenDash, add the devices you want
to use, then query your new OpenDash installation and to get your device ids to
do stuff against.

<code> 
$ curl https://graph.api.smartthings.com:443/api/smartapps/installations/00ac0059-935c-48e8-8973-xxxxxxxx/devices?access_token=xxxxxxxxxxxxxxxxxxxx
    {
        "id": "e75a3ef6-7a79-4ef5-993b-xxxxxxxxxxxxx",
        "name": "Z-Wave Metering Switch",
        "displayName": "Rope Light Outside"
    },
    {
        "id": "88bc9887-aeac-488b-9259-xxxxxxxxxxxx",
        "name": "Honeywell TCC 8000/9000 Thermostat",
        "displayName": "DOWNSTAIRS"
    },
    {
        "id": "b0a24cbc-0aec-4cb0-bbea-xxxxxxxxxxxxxx",
        "name": "Honeywell TCC 8000/9000 Thermostat",
        "displayName": "UPSTAIRS"
    }
</code>

You get the idea.  Otherwise, if you're calling IFTTT URL's or running
commands, you should be able to do that pretty easy. 


Bugs/Contact Info
-----------------
Bug me on Twitter at [@brianwilson](http://twitter.com/brianwilson) or email me [here](http://cronological.com/comment.php?ref=bubba).

