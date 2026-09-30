def auth(client):
    email="test@example.com"; password="StrongPassword123!"
    r=client.post("/register",json={"email":email,"full_name":"Test User","password":password})
    assert r.status_code in (200,409)
    r=client.post("/login",json={"email":email,"password":password}); assert r.status_code==200
    return {"Authorization":f"Bearer {r.json()['access_token']}"}
def test_health(client): assert client.get("/health").json()=={"status":"ok"}
def test_session(client): assert client.get("/session-info",headers=auth(client)).json()["authenticated"] is True
def test_home_fallback(client):
    r=client.post("/generate-home",headers=auth(client),json={"budget":50000,"currency":"INR","rooms":[{"room_type":"Living Room","quantity":1,"notes":"Modern"}],"preferences":"Warm"})
    assert r.status_code==200 and r.json()["source"]=="fallback"
def test_party_validation(client):
    r=client.post("/generate-party",headers=auth(client),json={"budget":-10,"guest_count":20,"event_type":"Birthday"})
    assert r.status_code==422
def test_history(client): assert isinstance(client.get("/history",headers=auth(client)).json(),list)
