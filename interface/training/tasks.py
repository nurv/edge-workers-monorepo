import datetime
import json
import os
import os.path

from ludwig import visualize
import sys
from celery import shared_task
from ludwig.api import LudwigModel
from celery.utils.log import get_task_logger
from io import StringIO
from django.conf import settings
import tensorflow as tf
import pandas as pd
from django.utils import timezone

from tensorflowjs.converters import tf_saved_model_conversion_v2


logger = get_task_logger(__name__)

@shared_task
def train(id):
    from training.models import MLModelVersion
    model_version: MLModelVersion = MLModelVersion.objects.get(id=id)
    try:
        model_version.status = "training"
        model_version.save()
        testdata = StringIO(model_version.dataset.dataset.content)
        df = pd.read_csv(testdata)

        model_bucket = os.path.join(settings.ROOT_BUCKET, model_version.model.bucket or str(model_version.model.id))
        is_exist = os.path.exists(model_bucket)
        if not is_exist:
            os.makedirs(model_bucket)

        model_version_path = os.path.join(model_bucket, str(model_version.id))
        is_exist = os.path.exists(model_version_path)
        if not is_exist:
            os.makedirs(model_version_path)

        logger.info(df)
        config = model_version.model.get_config()
        model = LudwigModel(config)
        logger.info("Train")
        train_stats, _, model_dir = model.train(df, output_directory=model_version_path + "/results")

        logger.info("Save")
        model.save(model_version_path)
        model.save_savedmodel(model_version_path)

        logger.info("Evaluate")
        data = model.evaluate(dataset=df, output_directory=model_version_path + "/results")
        print(data)
        model_version.evaluation_result = str(data[0])
        model_version.save()
        logger.info("Validate")
        for key, _ in data[0].items():
            if key != "combined":
                visualize.learning_curves(
                    [train_stats],
                    key,
                    model_name="Model1",
                    output_directory=model_version_path + "/results",
                    file_format="png"
                )

        with open(os.path.join(model_version_path, 'mean'), 'w') as f:
            f.write(str(model_version.dataset.dataset.mean))

        with open(os.path.join(model_version_path, 'std'), 'w') as f:
            f.write(str(model_version.dataset.dataset.std))

        model_version.status = "optimizing"
        model_version.save()

        tf_saved_model_conversion_v2.convert_tf_saved_model(
            model_version_path, model_version_path,
            signature_def=None,
            saved_model_tags='serve',
            skip_op_check=False,
            control_flow_v2=True,
            strip_debug_ops=True)

        converter = tf.lite.TFLiteConverter.from_saved_model(model_version_path)
        converter.target_spec.supported_ops = [
            tf.lite.OpsSet.TFLITE_BUILTINS,  # enable TensorFlow Lite ops.
            tf.lite.OpsSet.SELECT_TF_OPS  # enable TensorFlow ops.
        ]
        tflite_model = converter.convert()

        with open(os.path.join(model_version_path, 'model.tflite'), 'wb') as f:
            f.write(tflite_model)

        model_version.status = "finished"
        model_version.trained = timezone.now()
        model_version.save()
    except Exception as e:
        logger.exception(str(e))
        model_version.status = "error"
        model_version.save()
