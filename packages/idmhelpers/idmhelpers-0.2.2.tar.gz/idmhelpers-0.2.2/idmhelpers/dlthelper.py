# Delta Live Metadata framework
# Using the framework
#
# from idmhelper.dlthelper import TaskBuilder
# TH=TaskBuilder(spark=spark,storage="abfss://container@account.dfs.core.windows.net/im/mylocation")
# # define the pipeline array of tasks
# TaskBuilder.generate(pipeline)
#

import dlt
from pyspark.sql.functions import collect_list, struct


def createNestedFrame(df1, name, keycolumns=[], partitionkeys=[]):
    newcolumns = []
    newcolumns.extend(keycolumns)
    newcolumns.append(name)

    # Do not put key joining columns into nested structures
    nonkeycolumns = list(set(df1.columns)-set(keycolumns)-set(partitionkeys))

    df = df1.withColumn(name, struct(nonkeycolumns)).select(newcolumns)
    df = df.groupby(keycolumns).agg(collect_list(name).alias(name))
    return df


class TaskBuilder:

    storage = None
    spark = None

    def __init__(self, spark, storage):
        self.spark = spark
        self.storage = storage

    def generate(self, pipeline):
        for task in pipeline:
            self.generateTask(**task)

    def generateTask(self, name, sql, type="dlt-view", comment="", temporary=True,
                     nested=None, spark_conf=None, table_properties=None, path=None,
                     partition_cols=None, schema=None):
        kwargs = {}
        # Define a Live Table
        if type == "dlt-table":
            # Create Keyword Args for dlt.table
            if path == None:
                if self.storage != None:
                    path = f'{self.storage}/{name}'
            if path != None:
                kwargs.update({'path': path})
            if schema != None:
                kwargs.update({'schema': schema})
            if spark_conf != None:
                kwargs.update({'spark_conf': spark_conf})
            if table_properties != None:
                kwargs.update({'table_properties': table_properties})
            if partition_cols != None:
                kwargs.update({'partition_cols': partition_cols})
            kwargs.update({'name': name})
            kwargs.update({'comment': f"SQL:{name}:{comment}"})
            kwargs.update({'temporary': temporary})

            @dlt.table(**kwargs)
            def define_dlt_table():
                print(f'Live table: {name} ({comment}) {path})')
                df = self.spark.sql(sql)
                return df
        # Define a Live View
        if type == "dlt-view":
            @dlt.view(
                name=f"{name}",
                comment=f"SQL:{name}:{comment}"
            )
            def define_dlt_table():
                print(f'Live view: {name} ({comment})')
                df = self.spark.sql(sql)
                return df
        # Create a nested table - which folds sale line items into a table with a order,lineitem array.
        if type == "dlt-nest":
            if nested == None:
                raise Exception(
                    f'{name} uses dlt-nest but is missing the nested attribute.')

            @dlt.view(
                name=f"{name}",
                comment=f"SQL:Nested:{name}:{comment}"
            )
            def define_nested_table():
                print(f'Live view: {name} ({comment})')
                df = self.spark.sql(sql)
                df_n = createNestedFrame(
                    df, nested['name'], nested['keycolumns'], nested['partitionkeys'])
                return df_n
