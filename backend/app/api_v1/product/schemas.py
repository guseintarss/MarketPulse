from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    url: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductCreate):
    pass

class ProductUpdatePatrial(ProductCreate):

    name: str | None = None
    description: str | None = None
    price: int | None = None
    url: str | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
