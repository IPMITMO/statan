import uuid
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

class AnalyzerResult:
    def __init__(self,
                origin,
                language: str,
                language_ver: str,
                project_name: str,
                project_version: str,
                source_file_path: str,
                message: str,                
                params: str,
                start_line: int,
                severity: int=RESULT_SEVERITY.NORMAL,
                diffs: (str, None)=None,
                confidence: int=100,
                ):
        origin = origin or ''
        if not isinstance(origin, str):
            origin = origin.__class__.__name__
        if severity not in RESULT_SEVERITY.reverse:
            raise ValueError('severity is not a valid RESULT_SEVERITY')

        self.origin = origin
        self.language = language
        self.language_ver = language_ver
        self.project_name = project_name
        self.project_version = project_version
        self.source_file_path = source_file_path
        self.message = message
        self.severity = severity
        if confidence < 0 or confidence > 100:
            raise ValueError('Value of confidence should be between 0 and 100.')
        self.confidence = confidence
        self.diffs = diffs
        self.params = params
        self.start_line = start_line
        self.id = uuid.uuid4().int