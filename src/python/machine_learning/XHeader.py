class XHeader:
	xfrom = ["me"]
	xto = []
	xcc = []
	xbcc = []
	xfolder = ""
	xorigin = ""
	xfilename = ""

	def get_xfrom(self):
		return self.xfrom;

	def set_xfrom(self, xfrom):
		self.xfrom = xfrom;

	def get_xto(self):
		return self.xto

	def set_xto(self, xto):
		self.xto = xto

	def get_xcc(self):
		return self.xcc

	def set_xcc(self,xcc):
		self.xcc = xcc

	def get_xbcc(self):
		return self.xbcc

	def set_xbcc(self,xbcc):
		self.xbcc = xbcc

	def get_xfolder(self):
		return self.xfolder

	def set_xfolder(self,xfolder):
		self.xfolder = xfolder

	def get_xorigin(self):
		return self.xorigin

	def set_xorigin(self, xorigin):
		self.xorigin = xorigin

	def get_xfilename(self):
		return self.xfilename

	def set_xfilename(self,xfilename):
		self.xfilename = xfilename