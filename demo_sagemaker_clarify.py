# DEMO: Amazon SageMaker Clarify
import sagemaker
from sagemaker import get_execution_role
import boto3
import pandas as pd
from sagemaker import clarify
from sagemaker.image_uris import retrieve

# Configuración inicial
role = get_execution_role()
session = sagemaker.Session()
bucket = 'demo-clarify-ug-girls-chile'

# Rutas de los archivos con la data
train_data = 's3://{}/train_data.csv'.format(bucket)
test_data = 's3://{}/test_data.csv'.format(bucket)
baseline_file = 's3://{}/baseline_data.csv'.format(bucket)

# Generar contenedor para XGBoost
container = retrieve('xgboost', session.boto_region_name, version='latest')

# Configurar el estimator de XGBoost
xgb = sagemaker.estimator.Estimator(container,
                                    role, 
                                    instance_count=1, 
                                    instance_type='ml.m5.2xlarge',
                                    output_path='s3://{}/output'.format(bucket),
                                    sagemaker_session=session)

# Configurar los hiperparámetros
xgb.set_hyperparameters(objective='binary:logistic', num_round=100)

# Configurar datos de entrada para el entrenamiento
s3_input_train = sagemaker.inputs.TrainingInput(s3_data=train_data, content_type='csv')
s3_input_test = sagemaker.inputs.TrainingInput(s3_data=test_data, content_type='csv')

# Iniciar el entrenamiento del modelo
xgb.fit({'train': s3_input_train, 'validation': s3_input_test})

# Nombre del modelo
model_name = 'demo-model'

# Desplegar el modelo
xgb_model = xgb.create_model(name=model_name)

# Configurar las rutas de salida para los reportes de Clarify
bias_report_output_path = 's3://{}/clarify-bias'.format(bucket)
explainability_output_path = 's3://{}/clarify-explainability'.format(bucket)

# Configurar el análisis de sesgo
bias_config = clarify.BiasConfig(
    label_values_or_threshold=[1],
    facet_name='gender',
    facet_values_or_threshold=[1]
)

# Configurar el análisis de explicabilidad
shap_config = clarify.SHAPConfig(
    baseline=baseline_file, 
    num_samples=50,
    agg_method='mean_abs'
)

# Crear el procesador de Clarify
clarify_processor = clarify.SageMakerClarifyProcessor(role=role,
                                                      instance_count=1,
                                                      instance_type='ml.t3.medium',  # Cambiado a ml.c5.large
                                                      sagemaker_session=session)

# Ejecutar el job de análisis de sesgo
clarify_processor.run_pre_training_bias(
    data_config=clarify.DataConfig(
        s3_data_input_path=train_data,
        s3_output_path=bias_report_output_path,
        label='default',
        headers=['default', 'age', 'gender', 'income', 'loan_amount'],  # Incluye el encabezado
        dataset_type='text/csv'
    ),
    data_bias_config=bias_config
)

# Ejecutar el job de análisis de explicabilidad
clarify_processor.run_explainability(
    data_config=clarify.DataConfig(
        s3_data_input_path=test_data,
        s3_output_path=explainability_output_path,
        label='default',
        headers=['default', 'age', 'gender', 'income', 'loan_amount'],  # Incluye el encabezado
        dataset_type='text/csv'
    ),
    model_config=clarify.ModelConfig(
        model_name=model_name,
        instance_type='ml.t3.medium', 
        instance_count=1
    ),
    explainability_config=shap_config
)

# Imprimir localización de reportes generados
print(f'Reporte de sesgo ubicado en: {bias_report_output_path}')
print(f'Reporte de explicabilidad ubicado en: {explainability_output_path}')