from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName('tst')
    #.master("k8s://https://api.okd.dev.hamiltonbm.com:6443")
    .config("spark.kubernetes.namespace", "spark")
    .config("spark.submit.deployMode", "cluster")
    .config("spark.kubernetes.authenticate.driver.serviceAccountName", "spark")
    .config("spark.kubernetes.container.image", "itayb/spark:3.1.1-hadoop-3.2.0-aws")
    .config("spark.executor.instances", "2")
    .config("spark.executor.memory", "1g")
    .config("spark.executor.cores", "1")
    # .config("spark.driver.blockManager.port", "7777")
    # .config("spark.driver.port", "2222")
    # .config("spark.driver.bindAddress", "0.0.0.0")
    .getOrCreate()
)

data = [["java", "dbms", "python"], 
        ["OOPS", "SQL", "Machine Learning"]]
  
# giving column names of dataframe
columns = ["Subject 1", "Subject 2", "Subject 3"]
  
# creating a dataframe
dataframe = spark.createDataFrame(data, columns)
  
# show data frame
dataframe.show()

spark.stop()