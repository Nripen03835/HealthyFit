from models import Medicine
from sqlalchemy import or_

def search_medicine(query):
    # Try exact match first
    med = Medicine.query.filter(Medicine.name.ilike(query)).first()
    if med:
        return med
    # Fallback to fuzzy (contains)
    med = Medicine.query.filter(Medicine.name.ilike(f'%{query}%')).first()
    return med
