path='https://s3-eu-west-1.amazonaws.com/carnext-data-engineering-assignment/test_data/'
for num in range(1,2):
    filename = 'vehicle.csv000{0}_part_00.gz'.format(num)
    get_data_csv(path+filename,'/home/swati.singh/test_pipeline','/user/swati.singh/carnext-data-engineering-assignment/')
hadoop_dir = '/user/swati.singh/carnext-data-engineering-assignment/test_pipeline'
df=deduplicate_data(spark,hadoop_dir,True)


from demo.pipeline import Pipeline

pipeline = Pipeline()

@pipeline.task()
def get_raw_data(path: str) -> pd.DataFrame:
    raw_df = get_data(path)
    return raw_df

@pipeline.task(depends_on=get_raw_data)
def clean_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    dedup_df = deduplicate_data(raw_df)
    return dedup_df

@pipeline.task(depends_on=clean_data)
def get_metric(dedup_df: pd.DataFrame) -> pd.DataFrame:
    metric_df = generate_metric(dedup_df)
    return metric_df

@pipeline.task(depends_on=get_metric)
def save_metric(metric_df: pd.DataFrame) -> None:
    metric_df.to_csv('/demo/data/output.csv')