import os
import os.path
import shutil
import time

def rootDir():
	path = os.getcwd()
	root = os.path.dirname(path)
	return root

def backup():
	
	rootdir = rootDir()

	bakdir = os.path.join(rootdir,"backup")
	
	nowTime = time.localtime()
	timeStr = str(nowTime.tm_year)+"-"+str(nowTime.tm_mon)+"-"+str(nowTime.tm_mday)+"-"+str(nowTime.tm_hour)+"-"+str(nowTime.tm_min)+"-"+str(nowTime.tm_sec)
	bakname = "dbbackup"+"-"+ timeStr +".sqlite3"
	
	bakfile = os.path.join(bakdir, bakname)

	dbfile = os.path.join(rootdir,"db.sqlite3")

	shutil.copyfile(dbfile,bakfile)

	bakfilesize = os.path.getsize(bakfile)/1024

	fileinfo = {'bakname':bakname,'bakfilesize':bakfilesize}
	
	print fileinfo['bakname'],fileinfo['bakfilesize']
def delete():
	rootdir = rootDir()
	bakdir = os.path.join(rootdir,"backup")
	bakfile = os.path.join(bakdir,"1.txt")
	os.remove(bakfile)
	print 'success!'


if __name__ =="__main__":
	delete()
	exit()