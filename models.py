from pydantic import BaseModel, Field
from typing import List,Literal

class Attribute(BaseModel):
    attribute: str = Field(description='Variant classification evidence tag as per ACMG/AMP guidelines, denoting mechanistic and empirical attributes contributing to pathogenicity or benignity inference.')
    reason: str = Field(description='Reason for your response')

class Response(BaseModel):
    result: List[Attribute] = Field(description='List of Attributes associated')
    
class Classification(BaseModel):
    class_: Literal['Pathogenic', 'Benign','N/A'] = Field(description='ACMG Attribute class only accepted values are Pathogenic, Benign,N/A')
