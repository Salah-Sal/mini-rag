"""Controller for file data upload and validation operations.

This module provides functionality for validating and processing uploaded files,
generating unique file paths, and ensuring proper file naming and storage.
"""
from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os
from typing import Tuple, Optional

class DataController(BaseController):
    """Controller for handling file data operations.
    
    This controller manages file validation, path generation, and filename sanitization.
    It ensures files meet size and type requirements and are stored with unique identifiers.
    
    Attributes:
        size_scale: Multiplier to convert MB to bytes for file size validation (1048576)
    """
    
    def __init__(self):
        """Initialize the DataController with base controller functionality."""
        super().__init__()
        self.size_scale = 1048576  # convert MB to bytes

    def validate_uploaded_file(self, file: UploadFile) -> Tuple[bool, str]:
        """Validate an uploaded file against configured requirements.
        
        Checks:
        - File content type against allowed types
        - File size against maximum size limit
        
        Args:
            file: The FastAPI UploadFile object to validate
            
        Returns:
            A tuple containing:
            - Boolean indicating if validation passed (True) or failed (False)
            - ResponseSignal value as string indicating validation result
        """
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def generate_unique_filepath(self, orig_file_name: str, project_id: str) -> Tuple[str, str]:
        """Generate a unique filepath for storing an uploaded file.
        
        Creates a filepath with a random identifier prefix to ensure uniqueness.
        Continues generating until a non-existent path is found.
        
        Args:
            orig_file_name: Original filename from the upload
            project_id: Project ID to determine the project directory
            
        Returns:
            A tuple containing:
            - Full file path for storing the file
            - Unique file ID (random key + cleaned filename) for database reference
        """
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
        )

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name

    def get_clean_file_name(self, orig_file_name: str) -> str:
        """Sanitize a filename to ensure it's safe for storage.
        
        Removes special characters and ensures a safe filename format.
        
        Args:
            orig_file_name: Original filename to clean
            
        Returns:
            A sanitized filename with special characters removed
            (except underscores and periods) and spaces replaced with underscores
        """
        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name


