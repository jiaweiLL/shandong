# coding=utf-8
import six

from collections import OrderedDict
from .proto.attr_value_pb2 import AttrValue
from .proto.graph_pb2 import GraphDef
from .proto.versions_pb2 import VersionDef
from .proto_graph import attr_value_proto, tensor_shape_proto, node_proto


def paddle_graph(fluid_program, verbose, **kwargs):
    """This function process a paddle.fluid.Program and produces
    a `GraphDef` proto and `RunMetadata` proto that can be logged to Tensorboard.

    :param fluid_program: The program to be parsed.
    :type fluid_program: paddle.fluid.Program
    :param verbose: whether to add input/output variables to the graph.
    :type verbose: bool
    :return:
    """
    list_of_nodes = parse(fluid_program, verbose)
    return GraphDef(node=list_of_nodes, versions=VersionDef(producer=22))


class ScopeOp(object):
    def __init__(self, operator, op_type_index):
        self.op = operator

        if operator.has_attr("op_namescope"):
            operator_name_scope = operator.attr("op_namescope")
        else:
            operator_name_scope = "/"
    
        self.op_type_index = op_type_index

        prefix_op_name = "Default" + operator_name_scope + \
                         operator.type + "_" + str(op_type_index) + "_"

        self.op_name = prefix_op_name[8:]
        self.input_name_list = OrderedDict()
        self.output_name_list = OrderedDict()
        self.op_attrs = {}


class VarNode(object):
    # Every var in the program has its unique name.
    def __init__(self, var_name, var):
        self.var_name = var_name
        self.var = var
        self.is_input = True
        self.is_output = True
        self.input_op_list = []
        self.input_scope = []
        self.var_attrs = {}
        self.var_shape_proto = None


def parse(fluid_program, verbose):
    """This function parses a fluid Program and produces a list of nodes
        and node stats for eventual conversion to TensorBoard protobuf format.

    :param fluid_program: The program to be parsed.
    :type fluid_program: paddle.fluid.Program
    :param verbose: whether to add input variables and output variables to the Graph.
    :type verbose: bool
    """
    nodes = []

    # Create the list of ScopeOp
    scope_list = []
    op_type_index = OrderedDict()
    for op in fluid_program.global_block().ops:
        if op.type in op_type_index.keys():
            op_type_index[op.type] += 1
        else:
            op_type_index[op.type] = 0

        scope_list.append(ScopeOp(op, op_type_index[op.type]))

    # whether to add the input/output variables
    if verbose:
        # Initialize the dictionary of VarNode
        var_node_dict = {}
        for var_name in fluid_program.global_block().vars:
            var = fluid_program.global_block().var(var_name)
            var_node = VarNode(var_name, var)
            var_node_dict[var_name] = var_node

        for scope in scope_list:
            for input_arg_name in scope.op.input_arg_names:
                var_node_dict[input_arg_name].is_output = False

            for output_arg_name in scope.op.output_arg_names:
                var_node_dict[output_arg_name].is_input = False
                var_node_dict[output_arg_name].input_op_list.append(scope.op_name)
                var_node_dict[output_arg_name].input_scope.append(scope)

        # Add the var.shape to the VarNode.attributes, and create the corresponding nodes
        for var_name, var_node in var_node_dict.items():
            if var_node.is_input or (var_node.is_output and ("tmp" not in var_node.var_name)):
                if str(var_node.var.type) == "VarType.LOD_TENSOR":
                    if var_node.var.shape is not None:
                        var_node.var_shape_proto = tensor_shape_proto(var_node.var.shape)
                        var_node.var_attrs["shape"] = AttrValue(shape=var_node.var_shape_proto)
                    var_node.var_attrs["dtype"] = attr_value_proto(var_node.var.dtype)

            # Input Variables
            if var_node.is_input:
                if var_node.var_shape_proto is not None:
                    var_node.var_attrs['_output_shapes'] = AttrValue(
                        list=AttrValue.ListValue(shape=[var_node.var_shape_proto]))

                nodes.append(node_proto(name=var_node.var_name,
                                        op="Const",
                                        attributes=var_node.var_attrs))

            # Output Variables
            if var_node.is_output and ("tmp" not in var_node.var_name):
                # modify the name of variable node
                if len(var_node.input_op_list) == 1:
                    input_op_name = var_node.input_op_list[0]
                    last_slash_place = input_op_name.rfind("/") + 1
                    var_node.var_name = input_op_name[0:last_slash_place] + var_node.var_name
                
                # Append the var node to the graph
                nodes.append(node_proto(name=var_node.var_name,
                                        op="Output Variables",
                                        input_args=var_node.input_op_list,
                                        attributes=var_node.var_attrs))
               
                # Add the shape to the Graph edge
                if var_node.var_shape_proto is not None:
                    for input_scope in var_node.input_scope:
                        input_scope.op_attrs['_output_shapes'] = AttrValue(
                            list=AttrValue.ListValue(shape=[var_node.var_shape_proto]))
                 
    # Find the relations between operator by comparing their input_arg_names and output_arg_names.    
    for scope in scope_list:
        for other_scope in scope_list:
            if other_scope != scope:
                for op_input_arg in scope.op.input_arg_names:
                    if op_input_arg in other_scope.op.output_arg_names:
                        # other_scope.op is the input of scope.op
                        if other_scope.op_name not in scope.input_name_list.keys():
                            scope.input_name_list[other_scope.op_name] = op_input_arg
                        
                        # scope.op is the output of other_scope.op
                        if scope.op_name not in other_scope.output_name_list.keys():
                            other_scope.output_name_list[scope.op_name] = op_input_arg

        # Get the attributes of this op
        for key, value in sorted(six.iteritems(scope.op.all_attrs())):
            if key not in ['op_role_var', 'op_namescope', 'op_callstack', 'sub_block']:
                op_attr_str = str(value)
                if op_attr_str != '':
                    scope.op_attrs[key] = attr_value_proto(value)

        if verbose:
            # Add the input variables to the Graph
            for input_arg_name in scope.op.input_arg_names:
                if var_node_dict[input_arg_name].is_input:
                    scope.input_name_list[input_arg_name] = input_arg_name

    # Obtain the shape of tensor in the edge
    for scope in scope_list:
        # Get the output tensor shape of this operator
        exit_flag = False
        op_output_shape = None
        for op_output_arg_name in scope.op.output_arg_names:
            for other_scope in scope_list:
                if op_output_arg_name in other_scope.input_name_list.values():
                    op_output_tensor = fluid_program.global_block().var(op_output_arg_name)
                    try:
                        op_output_shape = op_output_tensor.shape
                    except:
                        pass
                    
                    exit_flag = True
                    break
        
            if exit_flag:
                break
        
        if op_output_shape is not None:
            output_shape_proto = tensor_shape_proto(op_output_shape)
            scope.op_attrs['_output_shapes'] = AttrValue(list=AttrValue.ListValue(shape=[output_shape_proto]))
        
        # create nodes
        nodes.append(node_proto(name=scope.op_name,
                                op=scope.op.type,
                                input_args=list(scope.input_name_list.keys()),
                                attributes=scope.op_attrs))

    return nodes
