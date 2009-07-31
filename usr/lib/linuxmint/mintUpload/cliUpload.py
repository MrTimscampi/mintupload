#!/usr/bin/env python



try:
	from mintUploadCore import *
except:
	print "You do not have all the dependencies!"
	sys.exit(1)



# i18n
gettext.install("messages", "/usr/lib/linuxmint/mintUpload/locale")



def cliUpload(filenames, servicename=None):
	services = read_services()
	if not servicename:
		servicename = config['autoupload']['autoselect']
		if servicename == 'False':
			servicename = services[0]['name']
	for service in services:
		if service['name'] == servicename:
			from os.path import getsize
			for filename in filenames:
				# Check there is enough space on the service, ignore threading
				filesize = getsize(filename)
				checker = mintSpaceChecker(service, filesize)
				try:    proceed = checker.run()
				except: raise CustomError(_("Upload failed."))

				if proceed:
					# Upload
					uploader = mintUploader(service, filename)
					uploader.start()
				else:
					raise CustomError(_("Upload failed."))



if __name__ == "__main__":
	from sys import argv
	if '--service' in argv:
		sname_i = argv.index('--service') + 1
		servicename = argv[sname_i]
		filenames = argv[sname_i+1:]
	else:
		servicename = None
		filenames = argv[1:]
	cliUpload(filenames, servicename)
