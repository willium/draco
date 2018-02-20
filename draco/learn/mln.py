import os
import sys

from pprint import pprint

from draco.spec import *
from draco.learn.helper import *
from draco.run import run

def absolute_path(p: str) -> str:
    return os.path.join(os.path.dirname(__file__), p)

def load_data(input_dir, format="compassql"):
    """ load compassql data
        Args: 
            input_dir: the directory containing a set of json compassql specs
            format: one of "compassql" and "vegalite"
        Returns:
            a dictionary containing name and the Task object representing the spec
    """
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    result = {}
    for fname in files:
        if ("rank-by-feature_histogram.json" in fname) or ("1d-T.json" in fname) or ("2d-QxT.json" in fname):
            continue
        with open(fname, 'r') as f:
            content = json.load(f)
            content["data"]["url"] = os.path.join(input_dir, content["data"]["url"])
            if format == "compassql":
                spec = Task.from_cql(content, ".")
            elif format == "vegalite":
                spec = Task.from_vegalite(content)
            result[os.path.basename(fname)] = spec
    return result


def load_pairs(compassql_data_dir):
    """  """
    partial_specs = load_data(os.path.join(compassql_data_dir, "input"), "compassql")
    compassql_outs = load_data(os.path.join(compassql_data_dir, "output"), "vegalite")
    result = {}
    for k in partial_specs:
        result[k] = (partial_specs[k], compassql_outs[k])
    return result

def discriminative_learning(train_data, initial_weights, learning_rate=0.01, max_iter=30):
    """ discriminative learning for mln """
    t = 0
    while t < max_iter:
        for k in train_data:
            partial_spec, full_spec = train_data[k][0], train_data[k][1]
            draco_rec = run(partial_spec, silence_warnings=True)
            # the solution generated by vis rec solution
            print(draco_rec.to_vegalite_json())
        break

if __name__ == '__main__':
    train_data = load_pairs(absolute_path("../../data/compassql_examples"))
    weights = discriminative_learning(train_data, current_weights())
