"""
RoboPulse Fleet Command Center
Day 5 - authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, require_role
from app.models import User, UserRole
from app.schemas.user import Token, UserCreate, UserRead
from app.security import create_access_token, hash_password, verify_password

#first we set up our router for our endpoints
router = APIRouter(prefix="/auth", tags=["auth"])

#next we define our login endpoint, which will accept a username and password, 
# verify the credentials, and return a JWT access token if the credentials are valid.
@router.post("/token", response_model=Token)
async def login(
    #we use the OAuth2PasswordRequestForm dependency to extract the username and 
    # password from the request body. Note that this is sent as form data, not JSON
    # thanks to the Depends() function.
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return Token(access_token=access_token, token_type="bearer")


#function to register a new user. This endpoint is protected by the require_role dependency, 
# which checks if the current user has the FLEET_ADMIN role.
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.FLEET_ADMIN)),
) -> User:
    existing = await db.execute(select(User).where(User.username == payload.username))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{payload.username}' is already taken",
        )

    #create a new User object with the provided username, hashed password, and role.
    user = User(
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    #add the new user to the database, commit the transaction, and refresh the user object to get its ID.
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user