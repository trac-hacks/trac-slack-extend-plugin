# trac-slack-extend-plugin

What is this ?
==============
This plugin is intended to implement part of plugins to connect with notifications in Slack. Below I will add each plugin  that is compatible. If you want you can open the **issue** and describe which plugin you want to be added.

Installation
============
To work correctly you need to download the following plugin and configure it: https://github.com/mandic-cloud/trac-slack-plugin

You must have installed `requests` -> `pip install requests`.

###How to Install trac-slack-extend plugin
1) `python setup.py bdist_egg` copy egg file in plugins directory of trac or install it from the administration.

2) restart your web server.

**!!! Note**: If you install a plugin that is included in the list, after installation please restart the web server. Then the plugin will work correctly.

Compatible plugins
=================
* [CodeComments](https://github.com/Kras4ooo/trac-code-comments-plugin "Code Comments") (My fixed version compatible with GIT)
