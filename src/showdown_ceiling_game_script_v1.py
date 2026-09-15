#!/usr/bin/env python3
"""Isolated review copy of Showdown Ceiling + Game Script Layer v1."""
from __future__ import annotations
from typing import Any

def f(v:Any,d:float=0.0)->float:
    try:return float(v)
    except (TypeError,ValueError):return d

def clamp(v,lo,hi):return max(lo,min(hi,v))
def pos_multiplier(pos):return {"WR":1,"TE":.85,"RB":.80,"QB":.55,"DST":.45,"K":.20}.get(pos.upper(),.40)
def role_tier(p):return str(p.get("RoleTier") or p.get("OptimizerRoleTier") or "UNKNOWN").upper()

def adjusted_ceiling(p):
    proj=f(p.get("Projection")); p90=f(p.get("P90"),proj*1.55); fit=f(p.get("TournamentFit"),f(p.get("GreenScore_ShowdownBridge"),50)); conf=f(p.get("RoleConfidence"),75); lev=f(p.get("GSCptLeverage"),100); own=f(p.get("GSCptOwnershipPct")); pos=str(p.get("Position") or "UNK").upper(); tier=role_tier(p); frag=str(p.get("FragilityClass") or "MEDIUM").upper()
    spread=max(0,p90-proj); volatility=clamp(spread*.16*pos_multiplier(pos),0,4.5); fit_bonus=clamp((fit-80)*.075,0,2); confidence=clamp((conf-82)*.055,0,1); leverage=clamp((lev-100)*.10,0,1.5); low_owned=clamp((10-own)*.07,0,.7); role_bonus={"CORE":1,"STRONG":.7,"VALUE":.25,"UNKNOWN":0}.get(tier,-.5); frag_penalty={"LOW":0,"MEDIUM":.35,"HIGH":1}.get(frag,.35)
    boost=clamp(volatility+fit_bonus+confidence+leverage+low_owned+role_bonus-frag_penalty,0,7)
    return {"Player":p.get("Player"),"Position":pos,"Team":p.get("Team"),"Projection":round(proj,3),"BaseP90":round(p90,3),"TournamentP90":round(p90+boost,3),"CeilingBoost":round(boost,3),"TournamentFit":round(fit,2),"RoleTier":tier,"RoleConfidence":round(conf,1),"CptLeverage":round(lev,2),"CptOwnership":round(own,2)}

def script_tags(p):
    team=str(p.get("Team") or "TEAM"); pos=str(p.get("Position") or "UNK").upper()
    if pos=="QB":return [f"{team}_AIR",f"{team}_SHOOTOUT"]
    if pos in {"WR","TE"}:return [f"{team}_AIR",f"{team}_TRAILING",f"{team}_SHOOTOUT"]
    if pos=="RB":return [f"{team}_CONTROL",f"{team}_LEAD"]
    if pos=="DST":return [f"{team}_CONTROL",f"{team}_DEFENSE"]
    if pos=="K":return [f"{team}_LOW_TD",f"{team}_CONTROL"]
    return [f"{team}_OTHER"]

def apply(players):
    out=[]
    for p in players:
        q=adjusted_ceiling(p);q["ScriptTags"]=script_tags(p);out.append(q)
    return sorted(out,key=lambda x:(x["TournamentP90"],x["Projection"]),reverse=True)
