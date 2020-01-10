"""
Duplicity backend using rclone, for Python3
Rclone is a powerful command line program to sync files and directories to and from various cloud storage providers.

File name: rclonebackend.py
Author: Francesco Magno
Updated for Python3: John Radley
Date created: 10/12/2016
Date updated: 2020-01-10
Licence: GPL-3.0
Original Repository: https://github.com/GilGalaad/duplicity-rclone
Updated Version Repository: https://github.com/jradxl/duplicity-rclone
Python Version: 3.7
"""

import os
import os.path

import duplicity.backend
from duplicity import log
from duplicity.errors import BackendException


class RcloneBackend(duplicity.backend.Backend):

	def __init__(self, parsed_url):
		duplicity.backend.Backend.__init__(self, parsed_url)
		self.rclone_cmd = u"rclone"
		self.parsed_url = parsed_url
		self.remote_path = self.parsed_url.path
		try:
			rc, o, e = self._subprocess(self.rclone_cmd + u" --version")
		except Exception:
			log.FatalError(u"rclone not found: please install rclone", log.ErrorCode.backend_error)

		if parsed_url.path.startswith(u"//"):
			self.remote_path = self.remote_path[2:].replace(u":/", u":", 1)

	def _get(self, remote_filename, local_path):
		sremf = remote_filename.decode(u"utf-8", errors=u"ignore")
		slocp = local_path.uc_name
		temp_dir = os.path.dirname(slocp)
		commandline = u"%s copy %s/%s %s" % (self.rclone_cmd, self.remote_path, sremf, temp_dir)
		rc, o, e = self._subprocess(commandline)
		if rc != 0:
			if os.path.isfile(os.path.join(temp_dir, sremf)):
				os.remove(os.path.join(temp_dir, sremf))
			raise BackendException(e.split(b'\n')[0])
		os.rename(os.path.join(temp_dir, sremf), slocp)

	def _put(self, source_path, remote_filename):
		ssrcp = source_path.uc_name
		sremf = remote_filename.decode("utf-8", errors="ignore")
		sremp = self.remote_path
		temp_dir = os.path.dirname(ssrcp)
		temp_filename = os.path.basename(ssrcp)
		os.rename(ssrcp, os.path.join(temp_dir, sremf))
		commandline = u"%s copy --include %s %s %s" % (self.rclone_cmd, sremf, temp_dir, sremp)
		rc, o, e = self._subprocess(commandline)
		if rc != 0:
			os.rename(os.path.join(temp_dir, sremf), ssrcp)
			raise BackendException(e.split(b'\n')[0])
		os.rename(os.path.join(temp_dir, sremf), ssrcp)

	def _list(self):
		filelist = []
		commandline = u"%s ls %s" % (self.rclone_cmd, self.remote_path)
		rc, o, e = self._subprocess(commandline)
		if rc != 0:
			if e.endswith(b"not found\n"):
				return filelist
			else:
				raise BackendException(e.split(b'\n')[0])
		if not o:
			return filelist
		lines = o.split(b'\n')
		for x in lines:
			if x:
				filelist.append(x.split()[-1])
		return filelist

	def _delete(self, remote_filename):
		sremf = remote_filename.decode("utf-8", errors="ignore")
		commandline = u"%s delete --drive-use-trash=false --include %s %s" % (self.rclone_cmd, sremf, self.remote_path)
		rc, o, e = self._subprocess(commandline)
		if rc != 0:
			raise BackendException(e.split(b'\n')[0])

	def _subprocess(self, commandline):
		import shlex
		from subprocess import Popen, PIPE
		log.Info(u"Executing subprocess: '%s'" % commandline)
		args = shlex.split(commandline)
		p = Popen(args, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
		return p.returncode, stdout, stderr


duplicity.backend.register_backend(u"rclone", RcloneBackend)

