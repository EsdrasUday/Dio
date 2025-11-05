from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchema, OutMixin

# Schema base para Categoria (usado na listagem de Atletas)
class CategoriaAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Scale", max_length=10)]

# Schema base para Centro de Treinamento (usado na listagem de Atletas)
class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="CT King", max_length=20)]

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="Joao", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="12345678900", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=75.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.70)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example='M', max_length=1)]
    categoria: CategoriaAtleta
    centro_treinamento: CentroTreinamentoAtleta

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome do atleta", example="Joao", max_length=50)]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", example=25)]


# FEATURE 2: Schema customizado para a listagem (get all)
class AtletaListOut(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="Joao", max_length=50)]
    categoria: CategoriaAtleta
    centro_treinamento: CentroTreinamentoAtleta
    
    class Config:
        from_attributes = True # Necessário para o ORM -> Schema