from troposphere import Join
from troposphere.dynamodb import Table

from serverless.aws.iam import IAMPreset, PolicyBuilder


class DynamoDBReader(IAMPreset):
    resource: Table

    def apply(self, policy_builder: PolicyBuilder, sid=None):
        policy_builder.allow(
            permissions=[
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan",
            ],
            resources=[
                self.resource.get_att("Arn").to_dict(),
                Join(delimiter="", values=[self.resource.get_att("Arn").to_dict(), "/index/*"]).to_dict(),
            ],
            sid=sid or self.resource.name + "Reader",
        )


class DynamoDBWriter(IAMPreset):
    def apply(self, policy_builder: PolicyBuilder, sid=None):
        policy_builder.allow(
            permissions=[
                "dynamodb:BatchWriteItem",
                "dynamodb:DeleteItem",
                "dynamodb:UpdateItem",
                "dynamodb:PutItem",
            ],
            resources=[self.resource.get_att("Arn").to_dict()],
            sid=sid or self.resource.name + "Writer",
        )


class DynamoDBWriteOnly(IAMPreset):
    def apply(self, policy_builder: PolicyBuilder, sid=None):
        policy_builder.allow(
            permissions=[
                "dynamodb:BatchWriteItem",
                "dynamodb:UpdateItem",
                "dynamodb:PutItem",
            ],
            resources=[self.resource.get_att("Arn").to_dict()],
            sid=sid or self.resource.name + "WriteOnly",
        )


class DynamoDBDelete(IAMPreset):
    def apply(self, policy_builder: PolicyBuilder, sid=None):
        policy_builder.allow(
            permissions=[
                "dynamodb:DeleteItem",
            ],
            resources=[self.resource.get_att("Arn").to_dict()],
            sid=sid or self.resource.name + "Delete",
        )


class DynamoDBFullAccess(IAMPreset):
    def apply(self, policy_builder: PolicyBuilder, sid=None):
        policy_builder.allow(
            permissions=[
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWriteItem",
                "dynamodb:DeleteItem",
                "dynamodb:UpdateItem",
                "dynamodb:PutItem",
            ],
            resources=[self.resource.get_att("Arn").to_dict()],
            sid=sid or self.resource.name + "FullAccess",
        )
