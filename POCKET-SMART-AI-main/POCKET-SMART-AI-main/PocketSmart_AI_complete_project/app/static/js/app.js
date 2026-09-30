const TOKEN_KEY="pocketsmart_access_token";
function setToken(t){localStorage.setItem(TOKEN_KEY,t);document.cookie=`access_token=${encodeURIComponent(t)}; Path=/; SameSite=Lax`}
function getToken(){return localStorage.getItem(TOKEN_KEY)}
async function logout(){await api("/logout",{method:"POST"});localStorage.removeItem(TOKEN_KEY);document.cookie="access_token=; Max-Age=0; Path=/; SameSite=Lax";location.href="/"}
async function api(path,options={}){const h=new Headers(options.headers||{}),t=getToken();if(t)h.set("Authorization",`Bearer ${t}`);if(options.body&&!(options.body instanceof FormData)&&!h.has("Content-Type"))h.set("Content-Type","application/json");try{const r=await fetch(path,{...options,headers:h}),type=r.headers.get("content-type")||"",data=type.includes("application/json")?await r.json():await r.text();if(r.status===401&&!["/login","/register"].includes(location.pathname)){localStorage.removeItem(TOKEN_KEY);location.href="/login"}return {ok:r.ok,status:r.status,data}}catch(e){return {ok:false,status:0,data:{detail:e.message}}}}
function showMessage(m){const e=document.getElementById("form-message");if(e)e.textContent=m}
function money(v,c="INR"){try{return new Intl.NumberFormat("en-IN",{style:"currency",currency:c}).format(Number(v))}catch{return `${c} ${Number(v).toFixed(2)}`}}
function escapeHtml(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]))}
function escapeAttr(v){return escapeHtml(v).replace(/`/g,"&#096;")}
