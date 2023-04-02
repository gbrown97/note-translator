from util import S3Storage
sobj = S3Storage("test_user")

#   TASK 1
a = "Welcome to Note Translator Web Application"
sobj.uploadTxt(a, 'testFile.txt')

#   TASK 2
textData, fileName = sobj.loadTxt('testFile.txt')
print(textData.read())
print(fileName)

#   TASK 3
print(sobj.listFiles())

#   TASK 4
url = sobj.create_presigned_url('testFile.txt')
print(url)

#   TASK 5
sobj.renameFile("testFile.txt", "testFileRenamed.txt")


#   TASK 6 
sobj.deleteFile("testFileRenamed.txt")
