"""Test for miscellaneous utilities."""


import jsonschema
import pytest

from dnadna.nets import Network
from dnadna.utils import jsonschema as _jsonschema
from dnadna.utils.config import (ConfigError, Config, ConfigMixIn,
        ConfigValidator, load_dict, save_dict)


# This example comes from a portion of the param-set.yml schema and provides
# a few non-trivial constructs to test against
PARAM_SET_EXAMPLE_SCHEMA = {
    'oneOf': [
        {
            'properties': {
                'type': {'const': 'regression'},
                'log_transform': {
                    'type': 'boolean',
                    'default': False
                }
            },
            'required': ['type'],
            'additionalProperties': False
        },
        {
            'properties': {
                'type': {'const': 'classification'},
                'classes': {'type': 'integer'},
                # Add one property that has a default and is valid for a
                # classification schema
                'loss_weight': {
                    'type': 'integer',
                    'default': 1
                }
            },
            'required': ['type', 'classes'],
            'additionalProperties': False
        }
    ]
}


def test_save_load_dict_from_unknown(tmp_path):
    """
    Test that loading a dict from an unsupported serialization format
    raises a `NotImplementedError`.
    """

    filename = tmp_path / 'test.xml'

    with pytest.raises(NotImplementedError) as exc:
        save_dict({}, filename)

    assert 'no known serializer for the given filename:' in str(exc.value)
    assert not filename.exists()

    filename.touch()
    with pytest.raises(NotImplementedError) as exc:
        load_dict(filename)

    assert 'no known deserializer for the given filename:' in str(exc.value)


@pytest.mark.parametrize('filename', ['test.json', 'test.yml'])
def test_save_load_dict_from_supported(tmp_path, filename):
    """
    Test saving a JSON-compatible data structure and loading it in different
    supported formats.
    """

    filename = tmp_path / filename
    save_dict({}, filename)
    assert load_dict(filename) == {}


def test_config_validation():
    """Tests for valid and invalid Config dicts."""

    invalid1 = {'a': 1, 'b': 2, ('c', 'd'): 3}

    with pytest.raises(ConfigError) as exc:
        Config(invalid1).validate()
    assert str(exc.value) == (
            "error in config: invalid key ('c', 'd'); config keys must be "
            "strings")

    invalid2 = {'a': 1, 'b': 2, 'c': {'d': {('e', 'f'): 3}}}

    with pytest.raises(ConfigError) as exc:
        Config(invalid2).validate()
    assert str(exc.value) == (
            "error in config at 'c.d': invalid key ('e', 'f'); "
            "config keys must be strings")


def test_config_validation_defaults_on_one_of():
    """
    Test assignment of default values while evaluating an object against
    sub-schemas in a JSON Schema ``oneOf`` directive.

    Regression test of a bug where, if a sub-schema in a ``oneOf`` contains
    defaults for some properties, it assigns those defaults to the instance
    even if the instance does not match that sub-schema.
    """

    validator = ConfigValidator(PARAM_SET_EXAMPLE_SCHEMA)
    instance = {'type': 'classification', 'classes': 2}

    # The instance should match the second sub-schema in the oneOf directive
    assert validator.validate(instance) is None

    # The bug is that log_transform=True was being assigned to the instance
    # from the first sub-schema, even though it doesn't match that sub-schema
    assert 'log_transform' not in instance
    assert 'loss_weight' in instance and instance['loss_weight'] == 1


def test_config_validation_defaults_nested_in_one_of():
    """
    Test that if a subschema in a ``oneOf`` directive fails validation, any
    default values in that subschema are *not* applied to the original
    instance.

    Regression test.
    """

    instance = {'name': 'b', 'params': {}}

    # This contains several sub-schemas only one of which can be valid,
    # depending on the value of the 'name' property.
    # Only the default values from the matching schema (in this case 'b')
    # should be added to the instance.  For example, we should not expect
    # to see {'params': {'c': 'c', 'd': 'd'}} because those default params
    # only come from the {'name': 'a'} schema.
    schema = {
        'type': 'object',
        'oneOf': [{
            'properties': {
                'name': {'enum': ['a']},
                'params': {'properties': {
                    'c': {'default': 'c'},
                    'd': {'default': 'd'}
                }}},
            'required': ['name']
        }, {
            'properties': {
                'name': {'enum': ['b']},
                'b': {'default': 2},
                'params': {'properties': {'e': {'default': 'e'}}}
            },
            'required': ['name']
        }, {
            'properties': {
                'name': {'enum': ['c']},
                'params': {'properties': {'f': {'default': 'f'}}}
            },
            'required': ['name']
        }]
    }

    validator = ConfigValidator(schema)
    validator.validate(instance)
    assert instance == {'name': 'b', 'b': 2, 'params': {'e': 'e'}}


def test_config_validation_reference_resolver(tmp_path, monkeypatch):
    """
    Test resolving references within schemas.

    Tese resolving fragment references (i.e. #/definitions within a schema) and
    references between schemas within the same local directory, as in the case
    of ``dnadna/schemas``.
    """

    schema_a = {
        'type': 'object',
        'properties': {
            'foo': {'$ref': 'b.yml'},
            'bar': {'$ref': '#/definitions/bar'}
        },
        'definitions': {
            'bar': {
                'type': 'string',
                'const': 'bar'
            }
        },
        'additionalProperties': False
    }

    schema_b = {
        'type': 'object',
        'properties': {
            'baz': {
                'type': 'string',
                'const': 'baz'
            },
            'qux': {'$ref': '#/definitions/qux'}
        },
        'definitions': {
            'qux': {
                'type': 'string',
                'const': 'qux'
            }
        },
        'additionalProperties': False
    }

    save_dict(schema_a, tmp_path / 'a.yml')
    save_dict(schema_b, tmp_path / 'b.yml')

    # right now there is no good way but to monkey-patch this
    monkeypatch.setattr(_jsonschema, 'SCHEMA_DIRS', [tmp_path])
    validator = Config._schema_validator_for(schema_a)

    example_good = {
        'foo': {
            'baz': 'baz',
            'qux': 'qux'
        },
        'bar': 'bar'
    }
    assert validator.validate(example_good) is None

    example_bad = {'foo': 1, 'bar': 'bar'}
    with pytest.raises(ConfigError) as exc:
        validator.validate(example_bad)

    assert isinstance(exc.value.__context__, jsonschema.ValidationError)

    example_bad = {
        'foo': {
            'baz': 'baz',
            'qux': 1
        },
        'bar': 'bar'
    }
    with pytest.raises(ConfigError) as exc:
        validator.validate(example_bad)

    assert isinstance(exc.value.__context__, jsonschema.ValidationError)


def test_config_inherit(tmp_path):
    """Basic test of config file inheritence."""

    parent_config = {'a': 1, 'b': 2, 'c': {
        'd': 4, 'e': 5, 'f': {'h': 8, 'i': 9}}}
    parent_c_config = {'d': 6}
    child_config = {'inherit': 'parent.json', 'b': 7,
                    'c': {'inherit': 'parent_c.json', 'g': 8}}

    save_dict(parent_config, tmp_path / 'parent.json')
    save_dict(parent_c_config, tmp_path / 'parent_c.json')
    save_dict(child_config, tmp_path / 'child.json')

    # When the 'child.json' config file, it should inherit part of its 'c' dict
    # from 'parent_c.json', and part of its top-level from 'parent.json'
    c = Config.from_file(tmp_path / 'child.json')
    assert c == {'a': 1, 'b': 7, 'c': {
        'd': 6, 'e': 5, 'f': {'h': 8, 'i': 9}, 'g': 8}}
    assert c.filename == (tmp_path / 'child.json')

    # Test inheritence of the filename attribute
    # Although 'c' is ultimately composed from many sources, it first appears
    # in child.json, so that's where it inherits its filename from:
    assert c['c'].filename == (tmp_path / 'child.json')
    # However c['c']['f'] is a dict from parent.json, so that should be its
    # filename
    assert c['c']['f'].filename == (tmp_path / 'parent.json')


def test_config_resolve_filename_from_inherited_prop(tmp_path):
    """
    Regression test for
    https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/94
    """

    dir_a = tmp_path / 'a'
    dir_a.mkdir()
    dir_b = tmp_path / 'b'
    dir_b.mkdir()

    parent_config = {'path_a': 'a.txt'}
    child_config = {
        'data': {
            'inherit': '../a/parent.json',
            'path_b': 'b.txt'
        }
    }
    save_dict(parent_config, dir_a / 'parent.json')
    save_dict(child_config, dir_b / 'child.json')

    schema = {
        'properties': {
            'data': {
                'properties': {
                    'path_a': {'type': 'string', 'format': 'filename'},
                    'path_b': {'type': 'string', 'format': 'filename'}
                }
            }
        }
    }

    config = Config.from_file(dir_b / 'child.json', schema=schema,
                              validate=True)
    assert config['data']['path_a'] == str(dir_a / 'a.txt')
    assert config['data']['path_b'] == str(dir_b / 'b.txt')


def test_config_resolve_filename_from_deeply_inherited_prop(tmp_path):
    """
    This is like the previous test
    `test_config_resolve_filename_from_deeply_inherited_prop` but for a case
    where there are multiple layers of configuration nesting and merging.

    In particular, this simulates the case of the current format of the
    training config file, which inherits its "dataset" property from the
    preprocessing config file, which in turn inherits the contents of its
    "dataset" property from a dataset config file.

    The files generated by this test simulate a simplified version of the same
    structure, which reproduces the bug, first identified in
    https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/118

    To make the test clearer, I've named the files and data structures more
    similarly to those from the real file formats.
    """

    dataset_dir = tmp_path / 'dataset'
    dataset_dir.mkdir()
    model_dir = tmp_path / 'model'
    model_dir.mkdir()

    dataset_config = {'data_root': '.', 'scenario_params_path': 'params.csv'}
    dataset_schema = {
        'properties': {
            'data_root': {'type': 'string', 'format': 'filename'},
            'scenario_params_path': {'type': 'string', 'format': 'filename'}
        }
    }

    preprocessing_training_schema = {'properties': {'dataset': dataset_schema}}

    preprocessing_config = {
        'dataset': {'inherit': '../dataset/dataset_config.yml'}
    }

    training_config = {
        'dataset': {'scenario_params_path': 'preprocessed_params.csv'},
        'inherit': 'preprocessing_config.yml'
    }

    save_dict(dataset_config, dataset_dir / 'dataset_config.yml')
    save_dict(preprocessing_config, model_dir / 'preprocessing_config.yml')
    save_dict(training_config, model_dir / 'training_config.yml')

    # Now read the training config and ensure that preprocessing_config.yml is
    # under model/ (since it's overridden in the training config), but
    # data_root is dataset/
    config = Config.from_file(model_dir / 'training_config.yml', validate=True,
                              schema=preprocessing_training_schema)

    assert (config['dataset']['scenario_params_path'] ==
            str(model_dir / 'preprocessed_params.csv'))
    assert config['dataset']['data_root'] == str(dataset_dir)


def test_config_overrides(tmp_path):
    """
    Test that the override! feature in configs works

    This is same as the example given in the documentation in
    docs/configuration.rst under "Overriding without merging"

    See https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/135
    """

    default_config = {
        'dataset_splits': {
            'training': 0.7,
            'validation': 0.3
        },
        'learned_params': {
            'param1': {'type': 'regression', 'log_transform': True},
            'param2': {'type': 'classification', 'classes': 2}
        }
    }

    preprocessing_config = {
        'inherit': 'default.yaml',
        'learned_params!': {
            'param_A': {'type': 'regression'},
            'param_B': {'type': 'regression'}
        }
    }

    # What we should expect after merging is that we get the learned_params!
    # section from preprocessing.yaml
    expected = dict(default_config)
    expected.update({
        'learned_params': preprocessing_config['learned_params!']
    })

    save_dict(default_config, tmp_path / 'default.yaml')
    save_dict(preprocessing_config, tmp_path / 'preprocessing.yaml')

    c = Config.from_file(tmp_path / 'preprocessing.yaml')
    assert c.dict() == expected


def test_config_mixin_early_setattr():
    """
    Regression test for a bug where setting an instance attribute on a
    ``ConfigMixIn`` instance before the ``config`` attribute itself has been
    assigned resulted in a ``RecursionError``.
    """

    class MyConfigMixIn(ConfigMixIn):
        def __init__(self, config):
            self.x = 1
            super().__init__(config)
            self.y = 2

    my_config_mixin = MyConfigMixIn({'y': 1})
    assert my_config_mixin.x == 1
    assert 'x' not in my_config_mixin.config
    assert my_config_mixin.y == 2
    assert 'y' in my_config_mixin.config and my_config_mixin.config['y'] == 2


def test_find_errormsg_for_combined_schemas():
    """
    Regression test for a bug found in development of !49.

    The ``ConfigValidatorMixin._find_applicable_errormsg`` method crashes when
    validation fails on a schema containing multiple schemas combined with
    ``oneOf``, ``anyOf``, etc.
    """

    validator = ConfigValidator({
        'properties': {
            'learned_params': {
                'additionalProperties': PARAM_SET_EXAMPLE_SCHEMA
            }
        }
    })

    assert validator.validate({
        'learned_params': {'foo': {'type': 'regression'}}}) is None
    assert validator.validate({
        'learned_params': {
            'bar': {'type': 'classification', 'classes': 2}
        }}) is None

    with pytest.raises(ConfigError) as exc:
        validator.validate({
                'learned_params': {
                    'bar': {'type': 'classification'}
                }})

    assert str(exc.value) == (
            "error in config at 'learned_params.bar': "
            "'classes' is a required property")


def test_defaults_on_malformed_instance():
    """
    Regression test for a bug found in development of !49.

    In some cases a sub-schema can contain a 'default', but if the property
    being checked in that sub-schema does not have a dict value the
    defaults resolver in ``validate_config_properties`` can crash if iterating
    over all errors.
    """

    schema = {
        'additionalProperties': {
            'type': 'object',
            'properties': {
                'foo': {
                    'type': 'string',
                    'default': 'yes'
                }
            }
        }
    }

    validator = ConfigValidator(schema)
    # previously this would throw
    # TypeError: 'str' object does not support item assignment because no
    # errors occur when validating foo.properties even though foo.type !=
    # 'object'
    with pytest.raises(ConfigError) as exc:
        validator.validate({'foo': 'bar'})

    assert str(exc.value) == (
            "error in config at 'foo': 'bar' is not of type 'object'")


def test_python_module_format():
    """
    Tests ``format: python-module`` for string values in schemas.
    """

    schema = {
        'type': 'string',
        'format': 'python-module'
    }

    validator = ConfigValidator(schema)
    validator.validate('dnadna')
    with pytest.raises(ConfigError) as exc:
        validator.validate('DefinitelyNotAPythonModule!')

    assert str(exc.value) == (
            "error in config: 'DefinitelyNotAPythonModule!' is not a "
            "'python-module'")


def test_unknown_network_name_in_config():
    """
    Test that there is a useful error message when a config contains an invalid
    network name.
    """

    schema = Network.get_schema()
    config = Config({
        'name': 'does_not_exist',
        'params': {}
    })
    with pytest.raises(ConfigError) as exc:
        config.validate(schema)

    assert str(exc.value).startswith(
        "error in config at 'name': must be one of cnn/CNN")
