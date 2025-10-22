import streamlit as st
from sqlalchemy.orm import Session
from main import Product, ProductVariant, Base, engine, SessionLocal
import uuid

st.set_page_config(page_title="نظام إدارة المكتبة", layout="wide", initial_sidebar_state="expanded")

# Sidebar
role = st.sidebar.selectbox("اختر الدور", ["Admin", "Sales", "StoreKeeper", "Viewer"])
st.sidebar.write(f"الدور الحالي: {role}")

st.title("نظام إدارة المكتبة")

# --- Add Product Tab ---
st.header("إضافة منتج جديد")
with st.form("product_form"):
    name = st.text_input("اسم المنتج")
    description = st.text_area("الوصف")
    group = st.text_input("المجموعة/الجروب")
    supplier = st.text_input("المورد")
    
    sku = st.text_input("SKU (أتركه فارغ للتوليد تلقائي)")
    price = st.number_input("السعر", min_value=0.0, step=0.01)
    quantity = st.number_input("الكمية", min_value=0, step=1)
    attributes = st.text_area("السمات (JSON)", placeholder='{"color": "أزرق", "size": "100 ورقة"}')
    unit = st.selectbox("وحدة القياس", ["unit", "box", "carton"])
    location = st.text_input("الموقع في المخزن")
    reorder = st.number_input("حد إعادة الطلب", min_value=0, step=1, value=5)
    
    submitted = st.form_submit_button("إضافة المنتج")
    
    if submitted:
        if not name:
            st.error("من فضلك أدخل اسم المنتج")
        else:
            db: Session = SessionLocal()
            new_product = Product(
                name=name,
                description=description,
                group=group,
                supplier=supplier
            )
            db.add(new_product)
            db.flush()
            
            if not sku:
                sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
            
            try:
                import json
                attr_dict = json.loads(attributes) if attributes else {}
            except:
                attr_dict = {}
            
            new_variant = ProductVariant(
                sku=sku,
                product_id=new_product.id,
                price=price,
                quantity=quantity,
                attributes=attr_dict,
                unit_of_measure=unit,
                reorder_level=reorder,
                location=location
            )
            db.add(new_variant)
            db.commit()
            db.close()
            
            st.success(f"تم إضافة المنتج '{name}' بنجاح! | SKU: {sku}")

# --- Display Products ---
st.divider()
st.header("المنتجات المضافة مؤخراً")
db = SessionLocal()
products = db.query(Product).order_by(Product.id.desc()).limit(10).all()

for product in products:
    with st.expander(f"📦 {product.name} (ID: {product.id})"):
        st.write(f"الوصف: {product.description}")
        st.write(f"المجموعة: {product.group}")
        st.write(f"المورد: {product.supplier}")
        if product.variants:
            for v in product.variants:
                st.write(f"SKU: {v.sku}")
                st.write(f"السمات: {v.attributes}")
                st.write(f"السعر: {v.price}")
                st.write(f"الكمية: {v.quantity}")
                st.write(f"وحدة القياس: {v.unit_of_measure}")
                st.write(f"الموقع: {v.location}")
                st.write(f"حد إعادة الطلب: {v.reorder_level}")
        else:
            st.write("لا توجد Variants حالياً")
db.close()
