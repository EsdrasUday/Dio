import uuid
from typing import Optional # FEATURE 1
from fastapi import APIRouter, Body, Query, status, HTTPException # FEATURE 1 & 3
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError # FEATURE 3
from sqlalchemy.orm import selectinload # FEATURE 2

# FEATURE 4: Imports de paginação
from fastapi_pagination import LimitOffsetPage, paginate
from workout_api.contrib.dependencies import DatabaseDependency

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaListOut # FEATURE 2
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
) -> AtletaOut:
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada.'
        )

    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )
    
    # FEATURE 3: Manipulação de Exceção de Integridade
    try:
        atleta = AtletaModel(
            **atleta_in.model_dump(exclude={'categoria', 'centro_treinamento'}),
            categoria=categoria,
            centro_treinamento=centro_treinamento
        )
        db_session.add(atleta)
        await db_session.commit()
    
    except IntegrityError as e:
        # Verifica se o erro é de violação de chave única (unique constraint) no CPF
        if 'UNIQUE constraint failed: atletas.cpf' in str(e) or 'Duplicate entry' in str(e) or 'atletas_cpf_key' in str(e):
            raise HTTPException(
                # Status code 303 conforme solicitado
                status_code=status.HTTP_303_SEE_OTHER, 
                detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
            )
        else:
            # Outro erro de integridade
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro de integridade no banco de dados."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados: {e}'
        )

    return AtletaOut.model_validate(atleta)


@router.get(
    '/',
    summary='Listar todos os atletas',
    status_code=status.HTTP_200_OK,
    # FEATURE 2: Resposta customizada
    # FEATURE 4: Paginação com LimitOffsetPage
    response_model=LimitOffsetPage[AtletaListOut],
)
async def query(
    db_session: DatabaseDependency,
    # FEATURE 1: Adicionar query parameters
    nome: Optional[str] = Query(None, description="Filtrar por nome do atleta"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF do atleta")
) -> LimitOffsetPage[AtletaListOut]:
    
    # Monta a query base com eager loading (otimizado)
    statement = select(AtletaModel).options(
        selectinload(AtletaModel.categoria),
        selectinload(AtletaModel.centro_treinamento)
    )

    # FEATURE 1: Aplica filtros se eles forem fornecidos
    if nome:
        statement = statement.where(AtletaModel.nome == nome)
    if cpf:
        statement = statement.where(AtletaModel.cpf == cpf)

    # FEATURE 4: Aplica a paginação na query
    # O paginate aplicará limit e offset automaticamente
    return await paginate(db_session, statement)


@router.get(
    '/{id}',
    summary='Consulta um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}'
        )

    return AtletaOut.model_validate(atleta)


@router.patch(
    '/{id}',
    summary='Editar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(
    id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut:
    atleta = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}'
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return AtletaOut.model_validate(atleta)


@router.delete(
    '/{id}',
    summary='Deletar um atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}'
        )

    await db_session.delete(atleta)
    await db_session.commit()