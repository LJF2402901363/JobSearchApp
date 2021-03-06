class JobInfo:
    def __init__(self):
        self.__jobName = ""
        self.__jobSalary = ""
        self.__jobCity = ""
        self.__jobEdu = ""
        self.__jobExperienceTime = ""
        self.__jobDes = ""
        self.__companyName = ""
        self.__codeName = ""
        self.__age = ""
        self.__jobUrl = ""
    @property
    def jobSalary(self):
        return self.__jobSalary

    @property
    def codeName(self):
        return self.__codeName
    @property
    def companyName(self):
        return self.__companyName
    @property
    def jobName(self):
        return self.__jobName
    @property
    def jobEdu(self):
        return self.__jobEdu
    @property
    def jobCity(self):

        return self.__jobCity
    @property
    def jobExperienceTime(self):
        return self.__jobExperienceTime
    @property
    def jobDes(self):
        return self.__jobDes

    @property
    def jobUrl(self):
        return self.__jobUrl
    @property
    def age(self):
        return self.__age
    def set_jobName(self,jobName):
        self.__jobName = jobName
    def set_jobSalary(self,jobSalary):
        self.__jobSalary = jobSalary
    def set_jobCity(self,jobCity):
        self.__jobCity = jobCity
    def set_jobEdu(self,jobEdu):
        self.__jobEdu = jobEdu

    def set_jobExperienceTime(self,jobExperienceTime):
        self.__jobExperienceTime = jobExperienceTime
    def set_jobDes(self,jobDes):
        self.__jobDes = jobDes
    def set_companyName(self, companyName):
        self.__companyName = companyName
    def set_codeName(self, codeName):
        self.__codeName = codeName
    def set_age(self, age):
        self.__age = age
    def set_jobUrl(self, jobUrl):
        self.__jobUrl = jobUrl
    def printJobInfo(self):
        print("[jobName:"+self.jobName+",jobSalary:"+self.jobSalary+",age:"+self.age+",jobCode:"+self.codeName+",jobCity:"+self.jobCity+",jobEdu:"+self.jobEdu+",jobExperienceTime:"+self.jobExperienceTime+",jobDes:"+self.jobDes+"]")