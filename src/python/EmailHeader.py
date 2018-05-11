class EmailHeader:
	messageID = ""
	date = ""
	from_ = []
	to = []
	subject = ""
	cc = []
	mime_version = ""
	content_type = ""
	content_transfer_encoding = ""
	bcc = []

	def get_messageID(self):
		return self.messageID

	def set_messageID(self,messageID):
		self.messageID = messageID

	def get_date(self):
		return self.date

	def set_date(self,date):
		self.date = date

	def get_from(self):
		return self.from_

	def set_from(self,from_):
		self.from_ = from_

	def get_to(self):
		return self.to

	def set_to(self,to):
		self.to = to

	def get_subject(self):
		return self.subject

	def set_subject(self,subject):
		self.subject = subject

	def get_cc(self):
		return self.cc

	def set_cc(self,cc):
		self.cc = cc

	def get_mime_version(self,mime_version):
		return self.mime_version

	def set_mime_version(self,mime_version):
		self.mime_version = mime_version

	def get_content_type(self):
		return self.content_type

	def set_content_type(self,content_type):
		self.content_type = content_type

	def get_content_transfer_encoding(self):
		return self.content_transfer_encoding

	def set_content_transfer_encoding(self,content_transfer_encoding):
		self.content_transfer_encoding = content_transfer_encoding

	def get_bcc(self):
		return self.bcc

	def set_bcc(self,bcc):
		self.bcc = bcc		



