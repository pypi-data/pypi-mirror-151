from . import Configuration, ApiClient
from .apis import AnalyzerApi, ParserApi
from .models import (
    MapFileRequest,
    MapFileResponse,
    MapFileParseRequest,
    MapFileParseResponse,
    ClassificationRule,
)
import base64
from typing import Optional, List
import os

__all__ = ["ClientWrapper", "MapFileResponse"]


class ClientWrapper:
    def __init__(self, server_url=None, verify_ssl=True):
        config = Configuration(host=server_url)
        if not verify_ssl:
            config.verify_ssl = False

        self.client = ApiClient(config)
        self._analyzer_api = AnalyzerApi(self.client)
        self._parser_api = ParserApi(self.client)

    def parse_map_file(self, map_file_path: str):
        with open(map_file_path, "rb") as f:
            base64_encoded_map_file = base64.b64encode(f.read()).decode("utf-8")
        parse_request = MapFileParseRequest(base64_encoded_map_file)
        return self._parser_api.parse_map_file(parse_request)

    def analyze_map_file(
        self,
        map_file_path: str,
        stack_name: str,
        target_part: str,
        compiler: str,
        project_file_path: Optional[str] = None,
        classification_rules: Optional[List[ClassificationRule]] = None,
        ignore_default_rules: Optional[bool] = False,
        **_kwargs
    ) -> MapFileResponse:
        with open(map_file_path, "rb") as f:
            base64_encoded_map_file = base64.b64encode(f.read()).decode("utf-8")
        base64_encoded_project_file = None
        if project_file_path is not None:
            with open(project_file_path, "rb") as f:
                base64_encoded_project_file = base64.b64encode(f.read()).decode("utf-8")
        if classification_rules is None:
            classification_rules = []
        map_file_request = MapFileRequest(
            map_file=base64_encoded_map_file,
            stack_name=stack_name,
            target_part=target_part,
            compiler=compiler,
            classification_rules=classification_rules,
            ignore_default_rules=ignore_default_rules,
        )
        if base64_encoded_project_file is not None:
            map_file_request.project_file = base64_encoded_project_file
            map_file_request.project_file_name = os.path.basename(project_file_path)
        return self._analyzer_api.analyze_map_file(map_file_request)
