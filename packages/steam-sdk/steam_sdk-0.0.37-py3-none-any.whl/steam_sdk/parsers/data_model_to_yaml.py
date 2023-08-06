import ruamel.yaml

from steam_sdk.data.DataModelMagnet import DataModelMagnet
from steam_sdk.data.DataConductor import Conductor
from steam_sdk.utils.yaml_as_dict import yaml_as_dict

def data_model_to_yaml(data_model: DataModelMagnet, name_file: str):
    """
        Write a DataModelMagnet object to yaml with pre-set format used across STEAM yaml files.
        In particular:
        - keys order is preserved
        - lists are written in a single row
    """

    # Helper functions
    def flist(x):
        retval = ruamel.yaml.comments.CommentedSeq(x)
        retval.fa.set_flow_style()  # fa -> format attribute
        return retval

    def recursive_f(data_dict, list_expections=['Conductors']):
        for key, value in data_dict.items():
            if isinstance(value, list) and (not key in list_expections):
                data_dict[key] = flist(value)
            elif isinstance(value, dict):
                data_dict[key] = recursive_f(value)
        return data_dict


    # Convert the DataModelMagnet object to a dictionary
    data_dict = data_model.dict()

    # Write lists in a single row
    data_dict = recursive_f(data_dict)

    # for key_1, value_1 in data_dict.items():
    #     if isinstance(value_1, list) and key_1 is not 'Conductors':
    #         data_dict[key_1] = flist(value_1)  # level 1
    #     if isinstance(value_1, dict):
    #         for key_2, value_2 in value_1.items():
    #             if isinstance(value_2, list):
    #                 data_dict[key_1][key_2] = flist(value_2)  # level 2
    #             if isinstance(value_2, dict):
    #                 for key_3, value_3 in value_2.items():
    #                     if isinstance(value_3, list):
    #                         data_dict[key_1][key_2][key_3] = flist(value_3)  # level 3

    #NEW:
    yaml = ruamel.yaml.YAML()
    yaml.default_flow_style = False
    yaml.emitter.alt_null = 'Null'

    def my_represent_none(self, data):
        return self.represent_scalar('tag:yaml.org,2002:null', 'null')
    yaml.representer.add_representer(type(None), my_represent_none)

    with open(name_file, 'w') as yaml_file:
        # data_dict = data.dict()
        # data_dict['Power_Supply']['I_control_LUT'] = flist([0, 0])  # changed to test capability to write a list in one row
        # data_dict['CoilWindings']['electrical_pairs']['group_together'] = flist([[1, 2], [3, 4]])  # changed to test capability to write a list of lists in one row
        yaml.dump(data_dict, yaml_file)
        #yaml.dump(data.dict(), yaml_file, default_flow_style= False, sort_keys=False)