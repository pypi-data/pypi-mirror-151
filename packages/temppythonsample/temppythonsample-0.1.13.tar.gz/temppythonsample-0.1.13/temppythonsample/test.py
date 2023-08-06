import os
import makana

# # source_directory = './temppythonsample'
# # print('Source directory for the step is {}.'.format(os.path.realpath(source_directory)))

# Get Projects
# projects = makana.Makana.getProjects()

# Get BaseImages
# baseImages = makana.Makana.getBaseImages()

# # Create Pipeline
# pipeline = makana.Makana.createPipeline("Text Sentiment Pipeline Sample", 2, 1)

# # Get DataStores
# # dataStores = makana.Makana.getDataStores()

# # Create SourceData Step
# sourceDataStep = makana.Makana.createSourceDataStep("Source Data", "workspaceblobstore", "sentiment/Sentiment.csv")

# # Pre Process Step
# cleanText = makana.Makana.CreatePythonScriptStep("Pre Process", "Y:\Makana-Scripts\pre-process.py",
#                                                 "python=3.7.9","azureml-defaults,tensorflow==2.5.0,pandas,scikit-learn,pyarrow,feather-format", "--read-from-file:{source_data_output};--save-to-file-path:{pre_process_output}")

# # Create Model
# createModel = makana.Makana.CreatePythonScriptStep("Create Model", "Y:\Makana-Scripts\create-model.py",
#                                                 "python=3.7.9","azureml-defaults,tensorflow==2.5.0,pandas,scikit-learn,pyarrow,feather-format", "--input1-dataframe-directory:{pre_process_output};--output-dataframe-directory:{create_model_output}")

# # Data Transfer

# dataTransfer = makana.Makana.createDataTransferStep("Data Transfer", "workspaceblobstore", "/sentiment")

# # Save Pipeline

# pipeline = makana.Makana.savePipeline()

# Run Pipeline 

runPipeline = makana.Makana.runPipeline(4)
