

def get_full_typename(o):

    instance_name = o.__class__.__module__ + "." + o.__class__.__name__
    if instance_name in ["builtins.module", "__builtin__.module"]:
        return o.__name__
    else:
        return instance_name


def is_type_torch_tensor(typename):
    return typename.startswith("torch.") and (
            "Tensor" in typename or "Variable" in typename
    )