from domain.JobInfo import JobInfo
import json
if __name__ == '__main__':
  job =  JobInfo()
  job.set_age(14)
  job.set_jobName("张三")
  job.set_companyName("小米公司")
  job.set_jobDes("这是一家很好的公司")
  job.set_codeName("4-5年")
  job.set_jobCity("武汉")
  job.set_jobRequire("精通Java")
  job.set_jobSalary(9000)
  job.set_jobEdu("本科毕业")
  job1 = JobInfo()
  job1.set_age(14)
  job1.set_jobName("李四")
  job1.set_companyName("华为公司")
  job1.set_jobDes("中国牛逼的大公司")
  job1.set_codeName("4-5年")
  job1.set_jobCity("深圳")
  job1.set_jobRequire("精通C++")
  job1.set_jobSalary(800000)
  job1.set_jobEdu("本科毕业")

  # 将对象字典化
  str = json.dumps(job1.__dict__,ensure_ascii=False)
  print(str)
  list = []
  # 逐个将字典化后的对象添加到列表中去
  list.append(job1.__dict__)
  list.append(job.__dict__)

  # 将对象列表格式化
  jsonStr = json.dumps(list,ensure_ascii=False)
  print(jsonStr)