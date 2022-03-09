from pyspark.sql import SparkSession, DataFrame
from pathlib import Path
from pyspark.sql import types as T

spark = (
    SparkSession.builder
    .appName('tst')
    #.master("k8s://https://api.okd.dev.hamiltonbm.com:6443")
    .config("spark.kubernetes.namespace", "giorgi-kandelaki")
    #.config("spark.kubernetes.authenticate.submission.oauthToken", "")
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

def get_losses_csv(spark: SparkSession, snapshot_dir: Path) -> DataFrame:
    """Reads losess.csv data file located in snapshot_dir and returns spark Dataframe.

    :param spark: SparkSession object.
    :param snapshot_dir: snapshot directory from airflow XCOM where losses files are located.

    :return Dataframe: returns Spark Dataframe.
    """
    schema = (
        T.StructType()
        .add("Iteration", T.LongType(), True)
        .add("EventSetTypeId", T.LongType(), True)
        .add("Day", T.LongType(), True)
        .add("EventID", T.LongType(), True)
        .add("EventSetID", T.LongType(), True)
        .add("TagID", T.LongType(), True)
        .add("Layer", T.FloatType(), True)
        .add("RIP", T.FloatType(), True)
        .add("RIB", T.FloatType(), True)
        .add("LayerId", T.LongType(), True)
        .add("Premium", T.FloatType(), True)
        .add("Tax", T.FloatType(), True)
        .add("Brokerage", T.FloatType(), True)
        .add("NetLayer", T.FloatType(), True)
        .add("Phantom", T.IntegerType(), True)
        .add("Subject", T.FloatType(), True)
        .add("BindingId", T.LongType(), True)
    )

    losses = (
        spark.read.format("csv")
        .option("header", True)
        .option("mode", "FAILFAST")
        .schema(schema)
        .load(str(snapshot_dir / "losses/*.csv"))
    )

    return losses.withColumnRenamed("LayerId", "LayerID").withColumnRenamed(
        "EventSetTypeId", "RegionID"
    )

path = Path('/mnt/cifs/modelsql01_srv_risk_snapshots_test/HamiltonCapitalPartners_AIG_2019_01_20210420_134502') #this we need if we are going to mount wfs to kubernetes

data = get_losses_csv(spark, path)

data.show()

spark.stop()