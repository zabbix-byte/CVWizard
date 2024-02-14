from .aptitude import Aptitude
from .education import Education
from .experience import Experience
from .licence import License
from .project import Project

from typing import List


class Profile:
    def __init__(self,
                 name: str,
                 description: str = None,
                 title: str = None,
                 location: str = None,
                 phone_number: str = None,
                 web_page: str = None,
                 email: str = None,
                 aptitudes: List[Aptitude] = [],
                 education: List[Education] = [],
                 experiences: List[Experience] = [],
                 licences: List[License] = [],
                 projects: List[Project] = []
                 ) -> None:
        self.name = name
        self.title = title
        self.description = description
        self.location = location
        self.aptitudes = aptitudes
        self.web_page = web_page
        self.email = email
        self.education = education
        self.experiences = experiences
        self.licences = licences
        self.projects = projects
        self.phone_number = phone_number

    def serrialize(self):
        for i in range(len(self.licences)):
            self.licences[i] = self.licences[i].__dict__

        for i in range(len(self.experiences)):
            self.experiences[i].serrialize_groups()
            self.experiences[i] = self.experiences[i].__dict__

        for i in range(len(self.projects)):
            self.projects[i] = self.projects[i].__dict__

        for i in range(len(self.education)):
            self.education[i] = self.education[i].__dict__

        return self.__dict__
