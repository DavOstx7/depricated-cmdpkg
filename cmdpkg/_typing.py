from typing import Union, List, Dict, Any, BinaryIO

CMDPrimitiveT = Union[str, List[str]]
EnvironmentT = Dict[str, str]
KwargsT = Dict[str, Any]
ProcessInputOutputT = Union[BinaryIO, int]
