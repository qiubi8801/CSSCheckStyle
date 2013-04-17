#/usr/bin/python
#encoding=utf-8
import urllib
import os
import shutil

def realpath(a, b):
	return os.path.realpath(os.path.join(a, b))
debug = False

pluginUrl = 'https://raw.github.com/wangjeaf/ckstyle-pm/master/plugins/%s/%sindex.py'
cmdPluginUrl = 'https://raw.github.com/wangjeaf/ckstyle-pm/master/commands/%s/%sindex.py'
pluginRootDir = realpath(__file__, '../../userplugins/plugins')
cmdPluginRootDir = realpath(__file__, '../../userplugins/commands')

pluginWant = 'PluginClass'
cmdPluginWant = 'doCommand'

def getWhatIWant(pluginType):
	return pluginWant if pluginType == 'plugins' else cmdPluginWant

def fetchPlugin(name, version = ''):
	return fetch(name, version, pluginUrl, pluginRootDir, 'plugins')

def fetchCmdPlugin(name, version = ''):
	return fetch(name, version, cmdPluginUrl, cmdPluginRootDir, 'commands')

def removePlugin(name, version = ''):
	remove(name, version, pluginRootDir)

def removeCmdPlugin(name, version = ''):
	remove(name, version, cmdPluginRootDir)

def remove(name, version, root):
	version = ''
	pluginDir = realpath(root, './' + name)
	if not os.path.exists(pluginDir):
		return
	if version is not None and version != '':
		versionDir = realpath(pluginDir, './v' + replacedVer)
		if not os.path.exists(versionDir):
			return
		else:
			shutil.rmtree(versionDir)
	shutil.rmtree(pluginDir)
	print('[CKstyle OK] %s is removed from %s' % (name, root))
	print('[CKstyle OK] Uninstall successfully!')

def findPlugin(name):
	return find(name, pluginRootDir)

def findCmdPlugin(name):
	return find(name, cmdPluginRootDir)

def find(name, root):
	pluginDir = realpath(root, './' + name)
	if not os.path.exists(pluginDir):
		return False
	filePath = realpath(pluginDir, './index.py')
	if not os.path.exists(pluginDir):
		return False
	return True

def fetch(name, version, url, root, pluginType):
	# do not support version currently
	version = ''
	
	pluginDir = realpath(root, './' + name)
	replacedVer =  '' if version == '' else version.replace('.', '_')
	if not os.path.exists(pluginDir):
		os.mkdir(pluginDir)
		open(realpath(pluginDir, './__init__.py'), 'w').write('')

	versionDir = pluginDir

	if version is not None and version != '':
		versionDir = realpath(pluginDir, './v' + replacedVer)
		if not os.path.exists(versionDir):
			os.mkdir(versionDir)
			open(realpath(versionDir, './__init__.py'), 'w').write('')
	
	filePath = realpath(versionDir, './index.py')
	if debug or not os.path.exists(filePath):
		realUrl = url % (name, '' if version == '' else ('' + version + '/'))
		print('[CKstyle OK] Downloading %s%s from %s' % (name, version, realUrl))
		request = urllib.urlopen(realUrl)
		if request.getcode() != 200:
			print('[CKstyle ERROR] Can not download file, status code : ' + str(request.getcode()))
			return
		try:
			f = open(filePath, 'w')
			f.write(request.read())
			print('[CKstyle OK] %s%s Downloaded in %s' % (name, version, filePath))
			if pluginType == 'commands':
				print('\n[CKstyle OK] Download successfully!\n[CKstyle OK] Please type "ckstyle %s" to execute.' % name)
			#urllib.urlretrieve(realUrl, realUrl)
		except IOError as e:
			print(str(e))
	versionPath = '' if replacedVer == '' else '.v' + replacedVer

	whatIWant = getWhatIWant(pluginType)

	moduleName = "ckstyle.userplugins.%s.%s%s.index" % (pluginType, name, versionPath)
	try:
		plugin = __import__(moduleName, fromlist=[whatIWant])
	except ImportError as e:
		print(('[CKstyle ERROR] Can not import plugin %s : ' % name) + str(e))
		return

	filePath = realpath(versionDir, './index.pyc')
	if os.path.exists(filePath):
		os.remove(filePath)

	try:
		attr = getattr(plugin, whatIWant)
	except Exception:
		attr = None
	return attr

if __name__ == '__main__':
	print fetchPlugin('demo')
	print fetchPlugin('demo', '1.0')
	print fetchCmdPlugin('democmd')
	print fetchCmdPlugin('democmd', '1.0')
	print removePlugin('demo')
	print removePlugin('demo', '1.0')
	print removeCmdPlugin('demo')
	print removeCmdPlugin('democmd', '1.0')