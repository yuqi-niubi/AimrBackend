"""
@author: chenxd
@software: PyCharm
@file: Fileoperate.py
@time: 2020/10/09 11:25
"""

from minio import Minio
from minio.error import ResponseError


class FileOperate(object):
	"""文件服务操作类"""
	def __init__(self):
		self.minioClient = Minio('192.168.10.211:9000', access_key='dxw', secret_key='dxwsoftqaz', secure=False)

		self._prefix = ""

	def __get_bucket(self, datasetid):
		"""
			datasetid 格式验证
			Args:
				datasetid 数据集ID
			Returns:
				完整的bucketname
		"""
		return self._prefix + str(datasetid)

	def remove_dataset(self, datasetid):
		"""
			物理删除某个文件夹
			Args:
				datasetid 数据集ID
		"""
		try:
			objects = self.minioClient.list_objects(self.__get_bucket(datasetid), 
				prefix=None,
				recursive=True)
			for obj in objects:
				self.minioClient.remove_object(self.__get_bucket(datasetid), obj.object_name)
			self.minioClient.remove_bucket(self.__get_bucket(datasetid))
		except ResponseError as err:
			print(err)

	def upload_singlefile(self, datasetid, path, file_data, size):
		'''单文件流数据上传
		Args:
			datasetid 数据集ID
			path 相对于根目录路径
			file_data 任何实现了io.RawIOBase的python对象
			size 文件大小
		'''

		try:
			self.minioClient.put_object(self.__get_bucket(datasetid), path,
					file_data, size)
		except ResponseError as err:
			print(err)

	def readfile(self, datasetid, object_name):
		'''基于对象名查找具体文件
		Args:
			datasetid 数据集ID
			object_name 具体对象名
		Returns:
			urllib3.response.HTTPResponse对象
		'''
		try:
			data = self.minioClient.get_object(self.__get_bucket(datasetid), 
				object_name)
			return data
		except ResponseError as err:
			print(err)

	def readfiles_generator(self, datasetid, recursive=True):
		'''获取文件夹下所有文件的迭代器
		Args:
			datasetid 数据集ID
			recursive 是否查找所有内容，包括子文件夹下
		Returns:
			所有对象的迭代器，对象类型为urllib3.response.HTTPResponse
		'''
		try:
			objects = self.read_catalog(datasetid, 
				recursive)
			for obj in objects:
				yield self.readfile(datasetid, obj.object_name) 
		except ResponseError as err:
			print(err)
