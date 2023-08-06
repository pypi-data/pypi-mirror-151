from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING, Union, Dict

from vectice.api.json import (
    RunStatus,
    ArtifactType,
    StopRunInput,
    ArtifactVersion,
    ArtifactReferenceInput,
    RulesDatasetVersionInput,
    RulesModelVersionInput,
    RulesCodeVersionInput,
    RunInput,
    JobInput,
    StartRunInput,
)
from vectice.models import CodeVersion
from vectice.models import DatasetVersion
from vectice.models import ModelVersion
from .artifact_reference import ArtifactReference
from .attachment_container import AttachmentContainer
from .git_version import GitVersion
from .integration import AbstractIntegration

if TYPE_CHECKING:
    from vectice.models import Job


def __create_artifact_input__(item: ArtifactReference) -> ArtifactReferenceInput:
    result = ArtifactReferenceInput(item.artifact_type)
    if item.dataset is not None:
        result.dataset = __to_dataset_version_input__(item)
    elif item.model is not None:
        result.model = __to_model_version_input__(item)
    elif item.code is not None:
        result.code = __to_code_version_input__(item)
    return result


def __to_code_version_input__(artifact_reference: ArtifactReference) -> RulesCodeVersionInput:
    result = RulesCodeVersionInput()
    if isinstance(artifact_reference.code, int):
        result.parentId = artifact_reference.code
    else:
        result.parentName = str(artifact_reference.code)
    result.version = ArtifactVersion(version_id=artifact_reference.version_id)
    return result


def __to_dataset_version_input__(artifact_reference: ArtifactReference) -> RulesDatasetVersionInput:
    result = RulesDatasetVersionInput()
    if isinstance(artifact_reference.dataset, int):
        result.parentId = artifact_reference.dataset
    else:
        result.parentName = str(artifact_reference.dataset)
    if artifact_reference.version_id is not None:
        result.autoVersion = False
        result.version = ArtifactVersion(version_id=artifact_reference.version_id)
        return result
    if artifact_reference.version_name is not None:
        result.autoVersion = False
        result.version = ArtifactVersion(version_name=artifact_reference.version_name)
        return result
    if artifact_reference.version_number is not None:
        result.autoVersion = False
        result.version = ArtifactVersion(version_number=artifact_reference.version_number)
        return result
    if artifact_reference.version_strategy is not None:
        result.autoVersion = True
        return result
    raise RuntimeError(f"Missing version information for dataset {artifact_reference.dataset}")


def __to_model_version_input__(artifact_reference: ArtifactReference) -> RulesModelVersionInput:
    result = RulesModelVersionInput()
    if isinstance(artifact_reference.model, int):
        result.parentId = artifact_reference.model
    else:
        result.parentName = str(artifact_reference.model)
    if artifact_reference.version_id is not None:
        result.version = ArtifactVersion(id=artifact_reference.version_id)
        return result
    if artifact_reference.version_name is not None:
        result.version = ArtifactVersion(version_name=artifact_reference.version_name)
        return result
    if artifact_reference.version_number is not None:
        result.version = ArtifactVersion(version_number=artifact_reference.version_number)
        return result
    raise RuntimeError(f"Missing version information for model {artifact_reference.model}")


def _ensure_reference(item: Union[ArtifactReference, CodeVersion, ModelVersion, DatasetVersion]) -> ArtifactReference:
    if isinstance(item, ArtifactReference):
        return item
    elif isinstance(item, CodeVersion):
        return ArtifactReference(code=item.code_id, version_id=item.id)
    elif isinstance(item, DatasetVersion):
        return ArtifactReference(dataset=item.dataset.id, version_id=item.id)
    elif isinstance(item, ModelVersion):
        return ArtifactReference(model=item.model.id, version_id=item.id)
    else:
        raise RuntimeError(f"can not create artifact reference from unknown object '{item}'")


class Run(AttachmentContainer):
    """
    The Run acts as the ActiveRun, JobRun and Job.
    The run is not viewable in the Vectice platform until the job is started.
    """

    def __init__(
        self,
        id: int,
        job: Job,
        name: str,
        system_name: Optional[str] = "",
        created_date: Optional[datetime] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: RunStatus = RunStatus.SCHEDULED,
        auto_code: bool = False,
        check_remote_repository: bool = True,
        description: Optional[str] = None,
        properties: Optional[Dict[str, str]] = None,
    ):
        """
        :param id: The id of the run
        :param job: The job of the run
        :param name: The name of the run
        :param system_name: The system name this run was executed in
        :param created_date: The creation date of the run
        :param start_date: The starting date of the run
        :param end_date: The ending date of the run
        :param status: The status of the run
        :param auto_code: If the auto code is activated
        :param check_remote_repository: If checking remote repository option is activated.
        :param description: A quick description of the run
        :param properties: The properties of the run
        """
        super().__init__(name, id, job._client, "Run")
        self._job = job
        self._systemName = system_name
        self._description = description
        self._properties = properties
        self._createdDate = created_date
        self._startDate = start_date
        self._endDate = end_date
        self._status = status
        self._duration: Optional[int] = None
        self._integration_client: Optional[AbstractIntegration] = job._integration_client
        self._inputs: List[ArtifactReference] = []
        self._outputs: List[ArtifactReference] = []
        self._auto_code = auto_code
        self._check_remote_repository = check_remote_repository

    def __repr__(self):
        return f"Run(id={self.id}, job={self.job}, name={self.name}, system_name={self.system_name}, start_date={self.start_date}, end_date={self.end_date}, duration={self.duration}, status={self.status}, inputs={self.inputs}, outputs={self.outputs})"

    def __enter__(self) -> Run:
        if self._status == RunStatus.SCHEDULED:
            self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        status = RunStatus.COMPLETED if exc_type is None else RunStatus.FAILED
        try:
            self.end_run(status=status)
        except Exception as e:
            self.fail(reason=str(e))
        finally:
            return exc_type is None

    @property
    def id(self) -> int:
        """
        The run identifier.
        :return: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def job(self) -> Job:
        """
        The parent Job object of the run.
        :return: Job
        """
        return self._job

    @job.setter
    def job(self, job):
        self._job = job

    @property
    def name(self) -> str:
        """
        The run name.
        :return: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def system_name(self) -> Optional[str]:
        """
        The system name the run is executed in.
        :return: Optional[str]
        """
        return self._systemName

    @system_name.setter
    def system_name(self, system_name: str):
        self._systemName = system_name

    @property
    def description(self) -> Optional[str]:
        """
        A quick description of the run.
        :return: Optional[str]
        """
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def properties(self) -> Optional[Dict]:
        """
        The run properties.
        :return: Optional[Dict]
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Dict):
        self._properties = properties

    @property
    def start_date(self) -> Optional[datetime]:
        """
        The starting date of the run.
        :return: Optional[datetime]
        """
        return self._startDate

    @property
    def end_date(self) -> Optional[datetime]:
        """
        The ending date of the run.
        :return: Optional[datetime]
        """
        return self._endDate

    @end_date.setter
    def end_date(self, end_date: datetime):
        self._endDate = end_date

    @property
    def status(self) -> RunStatus:
        """
        The status of the run.
        :return: RunStatus
        """
        return self._status

    @status.setter
    def status(self, status: RunStatus):
        self._status = status

    @property
    def duration(self) -> Optional[int]:
        """
        The duration of the run.
        :return: Optional[int]
        """
        return self._duration

    @duration.setter
    def duration(self, duration: int):
        self._duration = duration

    @property
    def inputs(self) -> List[ArtifactReference]:
        """
        The artifact inputs of the run.
        :return: List[ArtifactReference]
        """
        return self._inputs.copy()

    @property
    def outputs(self) -> List[ArtifactReference]:
        """
        The artifact outputs of the run.
        :return: List[ArtifactReference]
        """
        return self._outputs.copy()

    def to_reference_input(self, item: ArtifactReference) -> ArtifactReferenceInput:
        return ArtifactReferenceInput(
            item.artifact_type,
            item.description,
            RulesDatasetVersionInput(
                parentName=str(item.dataset) if not isinstance(item.dataset, int) else None,
                parentId=item.dataset if isinstance(item.dataset, int) else None,
                version=ArtifactVersion(item.version_number, item.version_name, item.version_id)
                if item.version_strategy is None
                else None,
                autoVersion=True if item.version_strategy is not None else None,
            )
            if item.artifact_type == ArtifactType.DATASET
            else None,
            RulesModelVersionInput(
                parentName=str(item.model) if not isinstance(item.model, int) else None,
                parentId=item.model if isinstance(item.model, int) else None,
                version=ArtifactVersion(item.version_number, item.version_name, item.version_id),
            )
            if item.artifact_type == ArtifactType.MODEL
            else None,
            RulesCodeVersionInput(
                parentName=str(item.model) if not isinstance(item.model, int) else None,
                parentId=item.model if isinstance(item.model, int) else None,
                version=ArtifactVersion(item.version_number, item.version_name, item.version_id),
            )
            if item.artifact_type == ArtifactType.CODE
            else None,
        )

    def add_output(self, output: ArtifactReference):
        """
        Adds an artifact as output to the run.

        :param output: The artifact to be added as an output
        :return: None
        """
        if self._outputs is None:
            self._outputs = [output]
        else:
            self._outputs.append(output)
        if self.status != RunStatus.SCHEDULED:
            self._client.fill_run(
                self.id,
                outputs=[self.to_reference_input(output)],
            )

    def add_outputs(self, outputs: List[ArtifactReference]):
        """
        Adds a list of artifacts as outputs to the run.

        :param outputs: The list of artifacts to be added as outputs
        :return: None
        """
        if self._outputs is None:
            self._outputs = outputs
        else:
            self._outputs.extend(outputs)
        if self.status != RunStatus.SCHEDULED:
            self._client.fill_run(
                self.id,
                outputs=[self.to_reference_input(output) for output in outputs],
            )

    def add_input(self, input: ArtifactReference):
        """
        Adds an artifact as input to the run.

        :param input: The artifact to be added as an input
        :return: None
        """
        if self._inputs is None:
            self._inputs = [input]
        else:
            if input not in self._inputs:
                self._inputs.append(input)
                # finally, if run is started, add it to the server
                if self.status != RunStatus.SCHEDULED:
                    self._client.fill_run(
                        self.id,
                        inputs=[self.to_reference_input(input)],
                    )

    def add_inputs(self, artifacts: List[ArtifactReference]):
        """
        Adds a list of artifact as inputs to the run.

        :param artifacts: The list of artifacts to be added as inputs
        :return: None
        """
        # first, remove duplicate from provided list
        inputs = []
        for input in artifacts:
            if input not in inputs:
                inputs.append(input)
        # then call add_input
        for input in inputs:
            self.add_input(input)

    def start(
        self,
        inputs: Optional[List[Union[ArtifactReference, CodeVersion, ModelVersion, DatasetVersion]]] = None,
        auto_code: Optional[bool] = None,
        check_remote_repository: Optional[bool] = None,
    ) -> None:
        """
        Starts the run.
        :param inputs: The artifacts to be added as inputs to the run
        :param auto_code: Boolean for the auto code option
        :param check_remote_repository: Boolean for the checking remote repository option
        :return: None
        """
        if inputs is not None:
            artifacts_references_inputs = [_ensure_reference(item) for item in inputs if item is not None]
            self.add_inputs(artifacts_references_inputs)

        if auto_code is True or (auto_code is None and self._auto_code is True):
            code_artifact_is_present = False
            if self._inputs is not None:
                for artifact in self._inputs:
                    code_artifact_is_present = code_artifact_is_present or artifact.artifact_type == ArtifactType.CODE
            if not code_artifact_is_present:
                git_version = GitVersion.create(
                    check_remote_repository=check_remote_repository
                    if check_remote_repository is not None
                    else self._check_remote_repository
                )
                if git_version:
                    code_version = self.job.project.create_code_version(git_version=git_version)
                    self.add_input(ArtifactReference(code=code_version.code_id, version_id=code_version.id))

        job_input = JobInput(self.job.name, self.job.description, self.job.type)
        self._status = RunStatus.STARTED
        self._startDate = datetime.utcnow()
        run_input = RunInput(self.name, job_input, self.system_name, self._startDate, self.end_date, self.status)
        if self._inputs is None:
            artifact_inputs = None
        else:
            artifact_inputs = [__create_artifact_input__(artifact) for artifact in self._inputs]
        rule_input = StartRunInput(job_input, run_input, artifact_inputs)
        if self._integration_client:
            try:
                self._integration_client.before_start(self)
            except Exception as e:
                logging.warning(e)
        self._client.start_run(rule_input)
        if self._integration_client:
            try:
                self._integration_client.after_start(self)
            except Exception as e:
                logging.warning(e)

    def end_run(
        self,
        outputs: Optional[List[ArtifactReference]] = None,
        status: RunStatus = RunStatus.COMPLETED,
        reason: Optional[str] = None,
    ) -> None:
        """
        Ends the current (last) active run started by :func:`~Vectice.start_run`.
        To end a specific run, use :func:`~Vectice.stop_run` instead.

        :param outputs: The artifacts to be added as outputs to the run
        :param status: Status of the run changes by default to COMPLETED
        :param reason: Reason note for ending the run
        :return: None
        """
        if outputs is not None:
            self.add_outputs(outputs)
        run_output = self._client.get_run(self.id)
        run_output["status"] = status
        run_output["endDate"] = datetime.utcnow()
        run_output["reason"] = reason
        rule_output = StopRunInput(run_output)
        if self._integration_client is not None:
            try:
                self._integration_client.before_stop(self)
            except Exception as e:
                logging.warning(e)
        output = self._client.stop_run(rule_output)
        self._status = output.jobRun.status
        self._duration = output.jobRun.duration
        self._startDate = output.jobRun.start_date
        self._endDate = output.jobRun.end_date
        if self._integration_client is not None:
            try:
                self._integration_client.after_stop(self)
            except Exception as e:
                logging.warning(e)

    def complete(self, outputs: Optional[List[ArtifactReference]] = None) -> None:
        """
        Completes the run.

        :param outputs: The artifacts to be added as outputs to the run

        :return: None
        """
        self.end_run(outputs=outputs, status=RunStatus.COMPLETED)

    def fail(
        self,
        outputs: Optional[List[ArtifactReference]] = None,
        reason: Optional[str] = None,
    ) -> None:
        """
        Fails the run.

        :param outputs: The artifacts to be added as outputs to the run
        :param reason: Reason note for failing the run

        :return: None
        """
        self.end_run(outputs=outputs, status=RunStatus.FAILED, reason=reason)

    def abort(
        self,
        outputs: Optional[List[ArtifactReference]] = None,
        reason: Optional[str] = None,
    ) -> None:
        """
        Aborts the run.

        The end date of the Run will be set at the time this method is called.

        :param outputs: The artifacts to be added as outputs to the run
        :param reason: Reason note for aborting the run
        :return: None
        """
        self.end_run(outputs=outputs, status=RunStatus.ABORTED, reason=reason)

    def clean(self):
        """
        Cleans and rests to None all the data of the run.

        """
        self._outputs = None
        self._inputs = None
        self._endDate = None
        self._duration = None
        self._status = RunStatus.SCHEDULED
