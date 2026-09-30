from urllib.parse import quote_plus
from ..schemas import *
from .gemini_service import gemini_service

PLATFORMS={
 "Amazon":"https://www.amazon.in/s?k={q}", "Flipkart":"https://www.flipkart.com/search?q={q}",
 "IKEA":"https://www.ikea.com/in/en/search/?q={q}", "Swiggy":"https://www.swiggy.com/search?query={q}",
 "Zomato":"https://www.zomato.com/search?query={q}", "OYO":"https://www.oyorooms.com/search?location={q}"
}
def search_url(platform,q): return PLATFORMS.get(platform,PLATFORMS["Amazon"]).format(q=quote_plus(q))

def home_fallback(r):
    n=len(r.rooms); alloc=[]; items=[]
    for room in r.rooms:
        amount=r.budget/n; alloc.append(BudgetAllocation(category=room.room_type,amount=round(amount,2),percentage=round(100/n,2),note="Starter allocation for this room."))
        price=round(amount*.65,2); items.append(RecommendationItem(name=f"{room.room_type} starter decor set",category=room.room_type,estimated_price=price,currency=r.currency,platform="Amazon",reason="Leaves budget for lighting and small accessories.",search_url=search_url("Amazon",f"{room.room_type} decor {r.preferences}"),priority="recommended"))
    total=round(sum(i.estimated_price for i in items),2)
    return RecommendationResponse(title="Home Interior Budget Plan",summary="A balanced starter plan divided across your selected rooms.",budget=r.budget,currency=r.currency,total_estimated=total,remaining_budget=round(r.budget-total,2),budget_allocations=alloc,recommendations=items,tips=["Measure spaces before buying furniture.","Keep a reserve for delivery and installation.","Compare the same category across platforms."],source="fallback")

def party_fallback(r):
    alloc=[BudgetAllocation("Food & catering",r.budget*.5,50,"Main guest-serving allocation."),BudgetAllocation("Decoration",r.budget*.2,20,"Simple theme and table decoration."),BudgetAllocation("Venue",r.budget*.2,20,"Venue allowance."),BudgetAllocation("Contingency",r.budget*.1,10,"Keep this reserve until final count.")]
    items=[RecommendationItem(name=f"{r.event_type} catering for {r.guest_count} guests",category="Food",estimated_price=round(r.budget*.5,2),currency=r.currency,platform="Zomato",reason="Compare menus and per-person packages.",search_url=search_url("Zomato",f"{r.event_type} catering {r.venue}"),priority="essential"),RecommendationItem(name=f"{r.event_type} decoration package",category="Decoration",estimated_price=round(r.budget*.2,2),currency=r.currency,platform="Amazon",reason="Simple reusable decorations can control costs.",search_url=search_url("Amazon",f"{r.event_type} party decoration"),priority="recommended"),RecommendationItem(name=f"Venue options in {r.venue or 'your city'}",category="Venue",estimated_price=round(r.budget*.2,2),currency=r.currency,platform="OYO",reason="Use this as a starting point for venue research.",search_url=search_url("OYO",r.venue or r.event_type),priority="recommended")]
    total=round(sum(i.estimated_price for i in items),2)
    return RecommendationResponse(title=f"{r.event_type} Party Budget Plan",summary=f"A starter allocation for {r.guest_count} guests.",budget=r.budget,currency=r.currency,total_estimated=total,remaining_budget=round(r.budget-total,2),budget_allocations=alloc,recommendations=items,tips=["Confirm guest count before final catering.","Keep contingency untouched until needed.","Ask vendors whether taxes, delivery and setup are included."],source="fallback")

def jewelry_fallback(r):
    items=[RecommendationItem(name=f"{r.style or 'Elegant'} jewelry set",category="Jewelry set",estimated_price=round(r.budget*.55,2),currency=r.currency,platform="Amazon",reason=f"Starter match for a {r.occasion} occasion.",search_url=search_url("Amazon",f"{r.occasion} {r.style} jewelry set"),priority="recommended"),RecommendationItem(name="Matching earrings",category="Earrings",estimated_price=round(r.budget*.2,2),currency=r.currency,platform="Flipkart",reason="A smaller matching piece can complete the outfit.",search_url=search_url("Flipkart",f"{r.occasion} matching earrings"),priority="optional")]
    total=round(sum(i.estimated_price for i in items),2)
    return RecommendationResponse(title=f"Jewelry Plan for {r.occasion}",summary="An occasion-based jewelry starter plan. An outfit image can improve visible color/style matching when Gemini is enabled.",budget=r.budget,currency=r.currency,total_estimated=total,remaining_budget=round(r.budget-total,2),budget_allocations=[BudgetAllocation("Main jewelry",r.budget*.65,65,"Primary piece."),BudgetAllocation("Accessories",r.budget*.2,20,"Optional supporting pieces."),BudgetAllocation("Reserve",r.budget*.15,15,"Keep for alternatives." )],recommendations=items,tips=["Match jewelry tone with visible outfit colors.","Check dimensions and material details before buying.","Keep some budget for alternatives."],source="fallback")

def generate_home(r):
    try: return gemini_service.generate("home",r.model_dump())
    except Exception: return home_fallback(r)
def generate_party(r):
    try: return gemini_service.generate("party",r.model_dump())
    except Exception: return party_fallback(r)
def generate_jewelry(r,image_bytes=None,image_mime=None):
    try: return gemini_service.generate("jewelry",r.model_dump(),image_bytes,image_mime)
    except Exception: return jewelry_fallback(r)
