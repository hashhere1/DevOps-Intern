from fastapi import FastAPI
from routers import user,categories, suppliers, products, inventory, sales,authentication
import uvicorn

app = FastAPI()

app.include_router(user.router)
app.include_router(categories.router)
app.include_router(suppliers.router)
app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(authentication.router)
app.include_router(sales.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app",host="0.0.0.0",port=8000,reload=True)

