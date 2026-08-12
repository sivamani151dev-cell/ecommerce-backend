from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cart import Cart, CartItem
from app.models.user import User
from app.models.product import Product
from app.schemas.cart import CartResponse, AddToCart
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cart", tags=["Cart"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def get_or_create_cart(user_id: int, db: Session):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id = user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.post("/add/{product_id}", response_model=CartResponse)
def add_to_cart(product_id: int, item: AddToCart, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock. Available: {product.stock}")
    cart = get_or_create_cart(current_user.id, db)
    existing_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        new_item = CartItem(cart_id=cart.id, product_id=product_id, quantity = item.quantity)
        db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return cart

@router.get("/", response_model=CartResponse)
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = get_or_create_cart(current_user.id, db)
    return cart

@router.delete("/remove/{product_id}", status_code=204)
def remove_from_cart(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    db.delete()
    db.commit()
    return None