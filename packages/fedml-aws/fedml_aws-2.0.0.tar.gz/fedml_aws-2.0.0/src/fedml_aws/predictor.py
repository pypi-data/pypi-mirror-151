from six import BytesIO, StringIO
import numpy as np
import json
import csv
import importlib
import os

def convert_npy_to_numpy(input_data):
    stream = BytesIO(input_data)
    return np.load(stream, allow_pickle=True)

def convert_csv_to_numpy(input_data, dtype=None):
    try:
        stream = StringIO(input_data)
        reader = csv.reader(stream, delimiter=",", quotechar='"', doublequote=True, strict=True)
        array = np.array([row for row in reader]).squeeze()
        array = array.astype(dtype)
        return array
    except ValueError as e:
        if dtype is not None:
            print("Error while writing numpy array: {}. dtype is: {}".format(e, dtype))
            return -1
    except Exception as e:
        print("Error while decoding csv: {}".format(e))

def convert_json_to_numpy(input_data, dtype=None):
    data = json.loads(input_data)
    return np.array(data, dtype=dtype)

def convert_array_to_npy(input_data):
    buffer = BytesIO()
    np.save(buffer, input_data)
    return buffer.getvalue()

def convert_array_to_csv(input_data):
    array = np.array(input_data)
    if len(array.shape) == 1:
        array = np.reshape(array, (array.shape[0], 1))
    try:
        stream = StringIO()
        writer = csv.writer(stream, lineterminator="\n", delimiter=",", quotechar='"', doublequote=True, strict=True)
        writer.writerows(array)
        return stream.getvalue()
    except csv.Error as e:
        print("Error while decoding csv: {}".format(e))

def convert_array_to_json(input_data):
    def default(_input_data):
        if hasattr(_input_data, "tolist"):
            return _input_data.tolist()
        return json.JSONEncoder().default(_input_data)
    return json.dumps(input_data, default=default)

def default_model_fn(model_dir):
    raise NotImplementedError('model_fn is a required function for your training script.')

def default_input_fn(input_data, content_type):
    np_array = decode(input_data, content_type)
    if content_type == "application/json" or content_type == "text/csv":
        return np_array.astype(np.float32)
    else:
        return np_array
    
def default_predict_fn(data, model):
    return model.predict(data)

def default_output_fn(prediction, accept):
    try:
        if accept == "application/x-npy":
            return convert_array_to_npy(prediction)
        elif accept == "text/csv":
            return convert_array_to_csv(prediction)
        elif accept == "application/json":
            return convert_array_to_json(prediction)
        else:
            raise TypeError('The accept passed is not supported.')
    except TypeError:
        raise

def decode(input_data, content_type):
    try:
        if content_type == "application/x-npy":
            return convert_npy_to_numpy(input_data)
        elif content_type == "text/csv":
            return convert_csv_to_numpy(input_data)
        elif content_type == "application/json":
            return convert_json_to_numpy(input_data)
        else:
            raise TypeError('The content type passed is not supported.')
    except TypeError:
        raise
    
class Predictor:
    def __init__(self, user_module):
        user_module = importlib.import_module('.'+user_module, 'source')
        model_fn = getattr(user_module, 'model_fn', default_model_fn)
        input_fn = getattr(user_module, 'input_fn', default_input_fn)
        predict_fn = getattr(user_module, 'predict_fn', default_predict_fn)
        output_fn = getattr(user_module, 'output_fn', default_output_fn)

        self._setup_functions(model_fn=model_fn, input_fn=input_fn, predict_fn=predict_fn,
                                       output_fn=output_fn)
        
    
            
    def _setup_functions(self, model_fn=None, input_fn=None, predict_fn=None, output_fn=None):
        if model_fn is not None:
            self._model_fn = model_fn
        else:
            self._model_fn = default_model_fn
            
        if input_fn is not None:
            self._input_fn = input_fn
        else:
            self._input_fn = default_input_fn
            
        if predict_fn is not None:
            self._predict_fn = predict_fn
        else:
            self._predict_fn = default_predict_fn
            
        if output_fn is not None:
            self._output_fn = output_fn
        else:
            self._output_fn = default_output_fn
            
    def get_model_fn(self):
        return self._model_fn
    
    def get_input_fn(self):
        return self._input_fn
    
    def get_predict_fn(self):
        return self._predict_fn
    
    def get_output_fn(self):
        return self._output_fn