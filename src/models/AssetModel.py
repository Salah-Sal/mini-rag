from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId
from sqlalchemy.future import select

class AssetModel(BaseDataModel):
    """Data access model for Asset entities.
    
    Provides methods for interacting with the Asset table, handling creation
    and retrieval of asset records associated with projects.
    
    Attributes:
        db_client: SQLAlchemy async session maker for database access.
    """

    def __init__(self, db_client: object):
        """Initialize the AssetModel.
        
        Args:
            db_client: SQLAlchemy async session maker.
        """
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """Create an instance of AssetModel asynchronously.
        
        Args:
            db_client: SQLAlchemy async session maker.
            
        Returns:
            Initialized AssetModel instance.
        """
        instance = cls(db_client)
        return instance

    async def create_asset(self, asset: Asset):
        """Create a single asset record in the database.
        
        Args:
            asset: Asset object to insert.
            
        Returns:
            The inserted Asset with updated attributes (e.g., ID).
        """
        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            await session.commit()
            await session.refresh(asset)
        return asset

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):
        """Retrieve all assets for a specific project and type.
        
        Args:
            asset_project_id: ID of the parent project.
            asset_type: Type of assets to retrieve (e.g., 'FILE').
            
        Returns:
            List of Asset objects matching the criteria.
        """
        async with self.db_client() as session:
            stmt = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_type == asset_type
            )
            result = await session.execute(stmt)
            records = result.scalars().all()
        return records

    async def get_asset_record(self, asset_project_id: str, asset_name: str):
        """Retrieve a specific asset by its project ID and name.
        
        Args:
            asset_project_id: ID of the parent project.
            asset_name: Name/identifier of the asset to retrieve.
            
        Returns:
            Asset object if found, None otherwise.
        """
        async with self.db_client() as session:
            stmt = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_name == asset_name
            )
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
        return record


    
