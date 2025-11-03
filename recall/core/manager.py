"""
Define functionality to remember path of the current directory for saving it later
Author: {^^}
"""


import os
from typing import Dict, NamedTuple, List
from pathlib import Path

from recall.core.database.manager import DatabaseHandler
from recall import DB_READ_ERROR, PROJECT_ID_ERROR, PROJECT_DIR_ERROR

class RecallProject(NamedTuple):
    recall_project: Dict[str, str]
    error: int


class Recall:

    def __init__(self, database_path: Path) -> None:
        # Has a relationship
        self.__database_handler = DatabaseHandler(database_path)

    @staticmethod
    def search(project_name: str, projects: List[Dict[str, str]]):
        curr_index = 0
        for project in projects:
            if project['project_name'] == project_name.lower():
                return curr_index
            curr_index += 1
        return -1

    def save(self, project_name: str, project_path: str):
        read_response = self.__database_handler.read() # what if some error occures while reading what will you do
        # if read_database.error == SUCCESS
        project = {
            'project_name': project_name,
            'project_path': project_path
        }
        if read_response.error == DB_READ_ERROR:
            return RecallProject(project, read_response.error)
        read_response.database.append(project)

        write_response = self.__database_handler.write(read_response.database)
        return RecallProject(project, write_response.error)

    def open(self, project_name: str) -> RecallProject:
        read_response = self.__database_handler.read() # what if some error occures while reading what will you do
        project = {
            'project_name': project_name,
            'project_path': ''
        }
        if read_response.error == DB_READ_ERROR:
            return RecallProject(project, read_response.error)
        
        if (project_index := self.search(project_name, read_response.database)) == -1:  # walrus operator has lower precedence than != hence True was assigned
            return RecallProject(project, PROJECT_ID_ERROR)

        project['project_path'] = read_response.database[project_index]['project_path']
        # try to open the folder path specified.
        try:
            os.startfile(project['project_path'])
        except OSError:
            return RecallProject(project, PROJECT_DIR_ERROR)
        return RecallProject(project, read_response.error)
        
    def delete(self, project_name: str) -> RecallProject:
        project = {
            'project_name': project_name,
            'project_path': ''
        }
        read_response = self.__database_handler.read()
        if read_response.error == DB_READ_ERROR:
            return RecallProject(project, read_response.error)
        
        if (project_index := self.search(project_name, read_response.database)) == -1:  # walrus operator has lower precedence than != hence True was assigned
            return RecallProject(project, PROJECT_ID_ERROR)
        try:
            project['project_path'] = read_response.database[project_index]['project_path']
            read_response.database.pop(project_index)  # has time complexity of O(n) | TODO: think about using dequeue 
        except IndexError:
            return RecallProject(project, PROJECT_ID_ERROR)
        
        write_response = self.__database_handler.write(read_response.database)
        return RecallProject(project, write_response.error)

    def update(self, project_name: str, project_path: str):
        read_response = self.__database_handler.read() # what if some error occures while reading what will you do
        project = {
            'project_name': project_name,
            'project_path': '',
            'new_project_path': project_path
        }
        if read_response.error == DB_READ_ERROR:
            return RecallProject(project, read_response.error)
        
        # get the index of the current project in database
        if (project_index := self.search(project_name, read_response.database)) == -1:  # walrus operator has lower precedence than != hence True was assigned
            return RecallProject(project, PROJECT_ID_ERROR)
        
        try:
            project['project_path'] = read_response.database[project_index]['project_path']
            read_response.database[project_index]['project_path'] = project_path  # updated the project path
        except IndexError:
            return RecallProject(project, PROJECT_ID_ERROR)
        
        write_response = self.__database_handler.write(read_response.database)
        return RecallProject(project, write_response.error)

    def list_projects(self) -> List[Dict[str, str]]:
        read_response = self.__database_handler.read()
        return read_response.database
