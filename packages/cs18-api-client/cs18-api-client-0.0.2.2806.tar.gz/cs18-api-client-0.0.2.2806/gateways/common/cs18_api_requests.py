"""
Container for Request object used in cs18-api-client
"""
from abc import ABCMeta
from enum import Enum
from typing import List, Optional

from gateways.common.cs18_api_classes import SpaceTerraformModuleInput
from gateways.common.cs18_api_classes import SpaceHelmChartComputeService
from gateways.common.cs18_api_classes import SpaceHelmChartInput
from gateways.common.cs18_api_classes import SpaceHelmChartOutput


class ProductionEnvironment(Enum):
    BLUE = 'blue'
    GREEN = 'green'


class DebuggingServiceValue(Enum):
    ON = 'on'
    OFF = 'off'


class SpaceCloudAccountSubnetsRequest:
    def __init__(self, gateway_subnet: str = None,
                 management_subnet: str = None,
                 application_subnets: List[str] = None):
        self.gateway_subnet = gateway_subnet
        self.management_subnet = management_subnet
        self.application_subnets = application_subnets


class SpaceCloudAccountInfraSetRequest:
    def __init__(self,
                 region: str,
                 virtual_network: str,
                 subnets: SpaceCloudAccountSubnetsRequest):
        self.region = region
        self.virtual_network = virtual_network
        self.subnets = subnets


class SpaceCloudAccountInfraSettingsRequest:
    def __init__(self,
                 internet_facing: bool,
                 existing_infra: bool,
                 existing_infra_sets: List[SpaceCloudAccountInfraSetRequest] = None):
        self.internet_facing = internet_facing
        self.existing_infra = existing_infra
        self.existing_infra_sets = existing_infra_sets


class UserSignupRequest:
    def __init__(self, first_name: str, last_name: str, password: str, secret: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.secret = secret

        # email is not part of the request, but it's needed to calculate display_first_name
        self.email = email

    @property
    def display_first_name(self):
        return self.first_name or self.email

    @property
    def display_last_name(self):
        return self.last_name


class CreateInvitationsRequest:
    def __init__(
            self,
            emails: [],
            account_role: str,
            reason: str,
            space_name: str,
            space_role: str,
    ):
        self.emails = emails
        self.account_role = account_role
        self.reason = reason
        self.space_name = space_name
        self.space_role = space_role


class CreateAccountRequest:
    def __init__(
            self,
            account_name: str,
            first_name: str,
            last_name: str,
            email: str,
            password: str,
            phone_number: str,
            company_name: str = None,
            utm_campaign: str = "",
    ):
        self.phone_number = phone_number
        self.password = password
        self.email = email
        self.last_name = last_name
        self.first_name = first_name
        self.account_name = account_name
        self.company_name = company_name
        self.utm_campaign = utm_campaign


class UpdateSpaceRequest:
    def __init__(self, name: str = None, color: str = None, icon: str = None):
        self.name = name
        self.color = color
        self.icon = icon


class AddK8SComputeServiceToSpaceRequest:
    def __init__(self, name: str, namespace: str, internet_facing: bool) -> None:
        self.name = name
        self.namespace = namespace
        self.internet_facing = internet_facing


class UpdateK8SComputeServiceInSpaceRequest:
    def __init__(self, namespace: str, internet_facing: bool) -> None:
        self.namespace = namespace
        self.internet_facing = internet_facing


class AwsCloudProviderSettingsModel:
    def __init__(self, sidecar_image_param_name: Optional[str]):
        self.sidecar_image_param_name = sidecar_image_param_name


class NewUserSurveyRequest:
    def __init__(self, roles: List[str] = None, primary_technologies: List[str] = None,
                 primary_platforms: List[str] = None) -> None:
        self.roles = roles if roles is not None else []
        self.primary_technologies = primary_technologies if primary_technologies is not None else []
        self.primary_platforms = primary_platforms if primary_platforms is not None else []


class TagRequest:
    def __init__(
            self,
            name: str,
            value: str,
            scope: str,
            possible_values: [],
            description: str,
    ):
        self.name = name
        self.value = value
        self.scope = scope
        self.possible_values = possible_values
        self.description = description


class TagOverrideRequest:
    def __init__(
            self,
            name: str,
            value: str,
    ):
        self.name = name
        self.value = value


class SpaceTerraformModuleRequestBase(metaclass=ABCMeta):
    def __init__(
            self,
            module_alias: str,
            description: Optional[str],
            cloud_account_name: str,
            compute_service_name: str,
            region: Optional[str],
            enable_logs: bool,
            inputs: Optional[List[SpaceTerraformModuleInput]]
    ):
        self.module_alias = module_alias
        self.description = description
        self.cloud_account_name = cloud_account_name
        self.compute_service_name = compute_service_name
        self.region = region
        self.enable_logs = enable_logs
        self.inputs = inputs


class AddSpaceTerraformModuleRequest(SpaceTerraformModuleRequestBase):
    def __init__(
            self,
            module_name: str,
            module_alias: str,
            description: Optional[str],
            cloud_account_name: str,
            compute_service_name: str,
            region: Optional[str],
            enable_logs: bool,
            inputs: Optional[List[SpaceTerraformModuleInput]]
    ):
        super().__init__(
            module_alias=module_alias,
            description=description,
            cloud_account_name=cloud_account_name,
            compute_service_name=compute_service_name,
            region=region,
            enable_logs=enable_logs,
            inputs=inputs
        )
        self.module_name = module_name


class UpdateSpaceTerraformModuleRequest(SpaceTerraformModuleRequestBase):
    def __init__(
            self,
            module_alias: Optional[str],
            description: Optional[str],
            cloud_account_name: str,
            compute_service_name: str,
            region: Optional[str],
            enable_logs: bool,
            inputs: Optional[List[SpaceTerraformModuleInput]]
    ):
        super().__init__(
            module_alias=module_alias,
            description=description,
            cloud_account_name=cloud_account_name,
            compute_service_name=compute_service_name,
            region=region,
            enable_logs=enable_logs,
            inputs=inputs
        )


class AddSpaceHelmChartRequest(metaclass=ABCMeta):
    def __init__(
            self,
            name: str,
            chart_root_path: str,
            compute_service: SpaceHelmChartComputeService,
            perform_helm_test: bool,
            enable_logs: bool,
            inputs: List[SpaceHelmChartInput],
            outputs: List[SpaceHelmChartOutput],
            description: Optional[str] = None,
            commands: Optional[List[str]] = None,
            override_values_yaml: Optional[str] = None,
            git_branch: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.compute_service = compute_service
        self.perform_helm_test = perform_helm_test
        self.chart_root_path = chart_root_path
        self.git_branch = git_branch
        self.enable_logs = enable_logs
        self.override_values_yaml = override_values_yaml
        self.inputs = inputs
        self.outputs = outputs
        self.commands = commands


class UpdateSpaceHelmChartRequest(metaclass=ABCMeta):
    def __init__(
            self,
            name: str,
            chart_root_path: str,
            compute_service: SpaceHelmChartComputeService,
            perform_helm_test: bool,
            enable_logs: bool,
            inputs: List[SpaceHelmChartInput],
            outputs: List[SpaceHelmChartOutput],
            description: Optional[str] = None,
            commands: Optional[List[str]] = None,
            override_values_yaml: Optional[str] = None,
            git_branch: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.compute_service = compute_service
        self.perform_helm_test = perform_helm_test
        self.chart_root_path = chart_root_path
        self.git_branch = git_branch
        self.enable_logs = enable_logs
        self.override_values_yaml = override_values_yaml
        self.inputs = inputs
        self.outputs = outputs
        self.commands = commands


class UpdatedBlueprint(metaclass=ABCMeta):
    def __init__(self, content: str):
        self.content = content
