
# IA responsable con Amazon SageMaker Clarify 
Clarify es una característica de SageMaker que ofrece herramientas para obtener información valiosa sobre nuestros modelos con el objetivo de mejorar su calidad mediante la detección de sesgos durante la preparación de los datos y después del entrenamiento, también proporciona informes de explicación de modelos para que las partes interesadas puedan ver cómo y por qué los modelos realizan predicciones con el fin de mejorar la calidad del modelo y respaldar iniciativas de IA responsable. Al día de hoy cuenta con:
- Detección de sesgos
- Explicabilidad del modelo
- Evaluación de modelos
- Monitoreo de modelos

Sin más, aquí la parte el ejemplo de como podemos utilizar Amazon SageMaker Clarify con un par de líneas de código.

## 💻 Requerimientos
- Credenciales AWS

## 📝 Paso a paso

### Paso 1: Cargar data en S3.

1.1 Carga el archivo train_data en un bucket en s3 

*Nota:* asegurate cambiar el nombre del bucket en el notebook.

### Paso 2: Ejecutar Notebook

2.1 Entra SageMaker y abre tu instancia de Jupyter

2.2 Carga el archivo y ejecuta el paso a paso

*Nota:* asegurate que el rol de tu instancia tenga acceso al bucket de s3 creado.

### Paso 3: Revisar los reportes

3.1 Al final de la ejecución te brindará la ubicación de los reportes generados (sesgos y explicabilidad). 

## 📚 Documentación

Artículo completo en [DEV.to](https://dev.to/bgalicia/ia-responsable-con-amazon-sagemaker-clarify-mhc "Ver detalles.").

