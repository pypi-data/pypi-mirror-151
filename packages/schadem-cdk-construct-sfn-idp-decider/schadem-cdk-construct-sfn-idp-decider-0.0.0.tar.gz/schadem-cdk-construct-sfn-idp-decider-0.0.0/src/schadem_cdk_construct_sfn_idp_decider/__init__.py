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
    @jsii.member(jsii_name="s3OutputBucket")
    def s3_output_bucket(self) -> builtins.str:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="s3OutputPrefix")
    def s3_output_prefix(self) -> builtins.str:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultClassification")
    def default_classification(self) -> typing.Optional[builtins.str]:
        ...


class _IDPPOCDeciderPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "schadem-cdk-construct-sfn-idp-decider.IDPPOCDeciderProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="s3OutputBucket")
    def s3_output_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3OutputBucket"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="s3OutputPrefix")
    def s3_output_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3OutputPrefix"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultClassification")
    def default_classification(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultClassification"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDPPOCDeciderProps).__jsii_proxy_class__ = lambda : _IDPPOCDeciderPropsProxy


__all__ = [
    "IDPPOCDecider",
    "IDPPOCDeciderProps",
]

publication.publish()
