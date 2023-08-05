# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rnotify', 'rnotify.lib']

package_data = \
{'': ['*']}

install_requires = \
['click-config-file>=0.6.0,<0.7.0',
 'click>=8.1.2,<9.0.0',
 'discord-webhook>=0.15.0,<0.16.0',
 'notifiers>=1.3.3,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'pymsteams>=0.2.1,<0.3.0',
 'python-daemon>=2.3.0,<3.0.0',
 'validators>=0.18.2,<0.19.0',
 'watchdog>=2.1.7,<3.0.0',
 'watchfiles>=0.13,<0.14']

entry_points = \
{'console_scripts': ['rn = rnotify.main:cli', 'rnotify = rnotify.main:cli']}

setup_kwargs = {
    'name': 'rnotify',
    'version': '0.1.3',
    'description': 'Tracking system changes on Unix hosts and letting you know about it.',
    'long_description': "\n# rnotify\n\n\n### Table of Contents\n\n- [About](#about)\n- [Installation](#installation)\n- [Usage](#usage)\n\n---\n\n## About\n\nOperators use several tools to perform internal security assessments. These tools can be difficult to track remotely and have output that is time sensitive. The tool rnotify tries to solve this problem. Some example use cases are listed below:\n\n- Monitor hashcat process and notify when cracking job is completed \n- Monitor folder for hashes captured using Responder\n- Monitor and notify on computer account creation when using mitm6 and ntlmrelayx\n- Notify when password spraying job completes\n\nFollowing a change to the monitoried object, the tool can then notify using a webhook for the following communication platforms:\n\n* Slack\n* MS Teams\n* Discord\n\n### Installation\n\nThe project can be installed using pipx: \n\n```\npipx install rnotify \n```\n\n## Usage\n\nThe tool is only useable on Unix based operating systems. The utility can be called using the command `rnotify` or `rn` and can monitor:\n\n* File changes\n* New files added to a folder\n* Process exit (PID)\n\n```\nUsage: rn [OPTIONS] COMMAND [ARGS]...\n\n  Notify on arbitrary filesystem events and process state changes.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  file    Notify on file changes\n  folder  Notify on directory changes\n  pid     Notify on process changes\n```\n\nAll modules require the specificiation of the following options:\n\n* Webhook URL used for notifications\n* Notification provider associated with the provided webhook\n* Target to monitor (file, folder, pid)\n\nAll modules optionally allow the specification of the following options:\n\n* Daemonization of the utility to run rnotify in the background\n* Sleep interval used by tool when checking for changes\n* Configuration file in the format shown below\n\n```\nwebhook = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'\ntarget = '/tmp/screen.log'\nnotifier = 'slack'\ncreate_daemon = 'True'\n```\n\n### File Monitoring\n\nFile changes can be monitored using the `file` subcommand:\n\n```\nUsage: rn file [OPTIONS] TARGET\n\n  Notify on file changes\n\nOptions:\n  -w, --webhook TEXT              Webhook URL  [required]\n  -n, --notifier [teams|slack|discord]\n                                  Notification provider.  [required]\n  -f, --filter TEXT               Filter changes by string.\n  -s, --sleep INTEGER             Sleep time between checks  [default: 5]\n  -d, --daemon                    Daemonize the utility\n  --config FILE                   Read configuration from FILE.\n  -h, --help                      Show this message and exit.\n ```\n Changes to logfiles can be filtered using the `-f` flag.\n \n### Folder Monitoring\n\nFolder changes can be monitored using the `folder` subcommand:\n\n```\nUsage: rn folder [OPTIONS] TARGET\n\n  Notify on directory changes\n\nOptions:\n  -w, --webhook TEXT              Webhook URL  [required]\n  -d, --daemon                    Daemonize the utility\n  -n, --notifier [teams|slack|discord]\n                                  Notification provider.  [required]\n  -s, --sleep INTEGER             Sleep time between checks  [default: 5]\n  --config FILE                   Read configuration from FILE.\n  -h, --help                      Show this message and exit.\n ```\n \n### PID Monitoring\n\nProcess exits can be monitored using the `pid` subcommand:\n \n```\nUsage: rn pid [OPTIONS] TARGET\n\n  Notify on process changes\n\nOptions:\n  -w, --webhook TEXT              Webhook URL  [required]\n  -n, --notifier [teams|slack|discord]\n                                  Notification provider.  [required]\n  -s, --sleep INTEGER             Sleep time between checks  [default: 5]\n  -d, --daemon                    Daemonize the utility\n  --config FILE                   Read configuration from FILE.\n  -h, --help                      Show this message and exit.\n```\n\n### Usage examples\n\nWatch Responder logs folder in the foreground:\n\n```\nrn folder /opt/Responder/logs -w https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX -n slack\n```\n\nWatch for hashcat process to stop in the background:\n\n```\nrn pid 54782 -w https://hooks.teams.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX -n teams -d\n```\n\nWatch for changes to gnu screen log with a filter in the foreground:\n\n```\nrn file /top/screen.log -f Account -w https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX -n slack \n```\n\n",
    'author': 'Nicholas A',
    'author_email': 'nicholasanastasirepair@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/puzzlpeaches/rnotify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
