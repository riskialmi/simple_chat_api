from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Json, ValidationError, validator, create_model, EmailStr, constr
from datetime import date, datetime
from pydantic.main import ModelMetaclass

class _AllOptionalMeta(ModelMetaclass):
    def __new__(self, name: str, bases: Tuple[type], namespaces: Dict[str, Any], **kwargs):
        annotations: dict = namespaces.get('__annotations__', {})

        for base in bases:
            for base_ in base.__mro__:
                if base_ is BaseModel:
                    break

                annotations.update(base_.__annotations__)

        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]

        namespaces['__annotations__'] = annotations

        return super().__new__(self, name, bases, namespaces, **kwargs)

class Login(BaseModel):
    name: str

class User(Login):
    id: int

    class Config:
        orm_mode = True
