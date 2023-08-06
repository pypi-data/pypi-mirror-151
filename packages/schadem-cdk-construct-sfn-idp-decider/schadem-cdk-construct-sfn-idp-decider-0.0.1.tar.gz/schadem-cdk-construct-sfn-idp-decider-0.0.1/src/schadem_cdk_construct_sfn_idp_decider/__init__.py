'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_stepfunctions
import constructs


class IDPPOCDecider(
    aws_cdk.aws_stepfunctions.StateMachineFragment,
    metaclass=jsii.JSIIMeta,
    jsii_type="schadem-cdk-construct-sfn-idp-decider.IDPPOCDecider",
):
    def __init__(
        self,
        parent: constructs.Construct,
        id: builtins.str,
        props: "IDPPOCDeciderProps",
    ) -> None:
        '''
        :param parent: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [parent, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[aws_cdk.aws_stepfunctions.INextable]:
        '''The states to chain onto if this fragment is used.'''
        return typing.cast(typing.List[aws_cdk.aws_stepfunctions.INextable], jsii.get(self, "endStates"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    def start_state(self) -> aws_cdk.aws_stepfunctions.State:
        '''The start state of this state machine fragment.'''
        return typing.cast(aws_cdk.aws_stepfunctions.State, jsii.get(self, "startState"))


@jsii.interface(jsii_type="schadem-cdk-construct-sfn-idp-decider.IDPPOCDeciderProps")
class IDPPOCDeciderProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultClassification")
    def default_classification(self) -> typing.Optional[builtins.str]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaMemoryMB")
    def lambda_memory_mb(self) -> typing.Optional[jsii.Number]:
        '''memory of Lambda function (may need to increase for larger documents).'''
        ...


class _IDPPOCDeciderPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "schadem-cdk-construct-sfn-idp-decider.IDPPOCDeciderProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultClassification")
    def default_classification(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultClassification"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaMemoryMB")
    def lambda_memory_mb(self) -> typing.Optional[jsii.Number]:
        '''memory of Lambda function (may need to increase for larger documents).'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lambdaMemoryMB"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDPPOCDeciderProps).__jsii_proxy_class__ = lambda : _IDPPOCDeciderPropsProxy


__all__ = [
    "IDPPOCDecider",
    "IDPPOCDeciderProps",
]

publication.publish()
