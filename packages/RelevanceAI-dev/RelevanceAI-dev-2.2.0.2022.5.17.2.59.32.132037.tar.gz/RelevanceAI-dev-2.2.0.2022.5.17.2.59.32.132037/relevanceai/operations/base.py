"""
Base class for operations.
"""
from typing import Any, List, Union
from relevanceai.client.helpers import (
    Credentials,
    process_token,
)


class BaseOps:
    """
    Base class for operations
    """

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def init(self, *args, **kwargs):
        return self(*args, **kwargs)

    @classmethod
    def from_credentials(self, credentials: Credentials, *args, **kw):
        return self(credentials=credentials)

    @classmethod
    def from_token(self, token: str, *args, **kw):
        """
        If this is from a token, then we use this
        """
        credentials = process_token(token)
        return self(credentials=credentials, *args, **kw)

    @classmethod
    def from_client(self, client, *args, **kwargs):
        credentials = client.credentials
        return self(
            credentials=credentials,
            *args,
            **kwargs,
        )

    @classmethod
    def from_dataset(
        self, dataset: Any, alias: str, vector_fields: List[str], *args, **kwargs
    ):
        dataset_id = dataset.dataset_id
        credentials = dataset.credentials
        return self(
            credentials=credentials,
            dataset_id=dataset_id,
            alias=alias,
            vector_fields=vector_fields,
            vector_field=vector_fields[0],
            *args,
            **kwargs,
        )

    def _get_dataset_id(self, dataset: Union[str, Any]):
        from relevanceai.dataset import Dataset

        if isinstance(dataset, str):
            return dataset
        elif isinstance(dataset, Dataset):
            return dataset.dataset_id

    def _check_vector_fields(self, vector_fields:List[str]):
        if len(vector_fields) == 0:
            raise ValueError("Please select at least 1 vector field") #we can add a optional behaviour to use all vectors here.
        if isinstance(vector_fields,str):
            return [vector_fields]
        else:
            new_vector_fields = []
            for f in vector_fields:
                if not f.endswith('_vector_'): #this could support chunkvector in the future.
                    new_vector_fields.append(f + "_vector_") #this will modify input, but assumes this is a mistake that the user is making
                else:
                    new_vector_fields.append(f)
            return new_vector_fields
