from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import func

class ProjectModel(BaseDataModel):
    """Data access model for Project entities.
    
    Provides methods for interacting with the Project table in the database,
    handling creation, retrieval, and listing of projects.
    
    Attributes:
        db_client: SQLAlchemy async session maker for database access.
    """

    def __init__(self, db_client: object):
        """Initialize the ProjectModel.
        
        Args:
            db_client: SQLAlchemy async session maker.
        """
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """Create an instance of ProjectModel asynchronously.
        
        Args:
            db_client: SQLAlchemy async session maker.
            
        Returns:
            Initialized ProjectModel instance.
        """
        instance = cls(db_client)
        return instance

    async def create_project(self, project: Project):
        """Create a single project record in the database.
        
        Args:
            project: Project object to insert.
            
        Returns:
            The inserted Project with updated attributes (e.g., ID).
        """
        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)
        
        return project

    async def get_project_or_create_one(self, project_id: str):
        """Retrieve a project by ID, creating it if it doesn't exist.
        
        Args:
            project_id: The ID of the project to retrieve or create.
            
        Returns:
            The existing or newly created Project object.
        """
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project = result.scalar_one_or_none()
                if project is None:
                    project_rec = Project(
                        project_id = project_id
                    )

                    project = await self.create_project(project=project_rec)
                    return project
                else:
                    return project

    async def get_all_projects(self, page: int=1, page_size: int=10):
        """Retrieve all projects with pagination.
        
        Args:
            page: Page number (1-indexed).
            page_size: Number of projects per page.
            
        Returns:
            A tuple containing:
            - List of Project objects for the requested page.
            - Total number of pages.
        """
        async with self.db_client() as session:
            async with session.begin():

                total_documents = await session.execute(select(
                    func.count( Project.project_id )
                ))

                total_documents = total_documents.scalar_one()

                total_pages = total_documents // page_size
                if total_documents % page_size > 0:
                    total_pages += 1

                query = select(Project).offset((page - 1) * page_size ).limit(page_size)
                projects = await session.execute(query).scalars().all()

                return projects, total_pages
