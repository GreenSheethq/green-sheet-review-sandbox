#!/usr/bin/env python3
"""Green Sheet adaptive five-lineup Showdown portfolio prototype.

ISOLATED REVIEW COPY. This does not deploy or mutate the live site.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Sequence

@dataclass(frozen=True)
class Player:
    name: str
    team: str
    projection: float
    p90: float
    tournament_fit: float = 50.0
    cpt_leverage: float = 100.0
    cpt_ownership: float = 0.0
    role_tier: str = "SALARY_ONLY"
    role_confidence: float = 0.0
    fragility: str = "MEDIUM"

@dataclass(frozen=True)
class Candidate:
    cpt: str
    flex: tuple[str, ...]
    projection: float
    p90: float
    tournament_fit: float
    thesis: str
    @property
    def players(self): return (self.cpt,) + self.flex
    @property
    def signature(self): return self.cpt, tuple(sorted(self.flex))

def captain_strength(p: Player) -> float:
    role_bonus={"CORE":5.0,"STRONG":3.0,"VALUE":0.5}.get(p.role_tier.upper(),-5.0)
    fragility_penalty={"LOW":0.0,"MEDIUM":1.5,"HIGH":4.0}.get(p.fragility.upper(),2.0)
    ownership_leverage=max(-4.0,min(6.0,(p.cpt_leverage-100.0)*0.55))
    low_owned_upside=max(0.0,12.0-p.cpt_ownership)*0.22
    return p.p90*.34+p.projection*.18+p.tournament_fit*.22+p.role_confidence*.10+ownership_leverage+low_owned_upside+role_bonus-fragility_penalty

def captain_confidence(players: dict[str,Player], candidates: Sequence[Candidate]) -> dict:
    available={c.cpt for c in candidates}
    ranked=sorted((players[n] for n in available if n in players),key=captain_strength,reverse=True)
    if not ranked:return {"band":"NONE","ranked":[],"top_gap":0.0,"cluster_2":0,"cluster_4":0}
    rows=[(p.name,captain_strength(p)) for p in ranked]; top=rows[0][1]; second=rows[1][1] if len(rows)>1 else top-99
    gap=top-second; c2=sum(1 for _,s in rows if top-s<=2); c4=sum(1 for _,s in rows if top-s<=4)
    band="HIGH" if gap>=4 and c4<=2 else ("MEDIUM" if c2<=2 and c4<=3 else "LOW")
    return {"band":band,"ranked":rows,"top_gap":round(gap,3),"cluster_2":c2,"cluster_4":c4}

def captain_slots(players,candidates,desired=5):
    conf=captain_confidence(players,candidates); names=[n for n,_ in conf["ranked"]]
    if not names:return {}
    if desired!=5:return {n:1 for n in names[:desired]}
    # Prototype assumes a sufficiently deep CPT pool; reviewer should inspect sparse-pool handling before production.
    if conf["band"]=="HIGH" and len(names)>=3:return {names[0]:3,names[1]:1,names[2]:1}
    if conf["band"]=="MEDIUM" and len(names)>=3:return {names[0]:2,names[1]:2,names[2]:1}
    if len(names)>=4:return {names[0]:2,names[1]:1,names[2]:1,names[3]:1}
    # Safe review fallback for sparse pools.
    out={n:1 for n in names}; left=desired-len(out); i=0
    while left>0 and names: out[names[i%len(names)]]+=1; left-=1; i+=1
    return out

def lineup_quality(c,players):
    return c.p90*.43+c.projection*.20+c.tournament_fit*.12+captain_strength(players[c.cpt])*.25

def select_portfolio(candidates: Iterable[Candidate],players: dict[str,Player],desired=5):
    pool=list({c.signature:c for c in candidates}.values())
    if len(pool)<desired:return []
    slots=captain_slots(players,pool,desired)
    if not slots:return []
    best_p90=max(c.p90 for c in pool); best_proj=max(c.projection for c in pool)
    for p90f,projf in ((.88,.86),(.84,.82),(.80,.78),(.76,.74)):
        eligible=[c for c in pool if c.p90>=best_p90*p90f and c.projection>=best_proj*projf and c.cpt in slots]
        selected=[]; cpt_used=Counter(); player_used=Counter(); thesis_used=Counter()
        while len(selected)<desired:
            best=None; best_score=float('-inf')
            for c in eligible:
                if c in selected or cpt_used[c.cpt]>=slots[c.cpt]:continue
                repeats=sum(player_used[n] for n in c.players); tr=thesis_used[c.thesis]
                score=lineup_quality(c,players)-repeats*.45-tr*3+(2.5 if tr==0 else 0)
                if score>best_score:best_score,best=score,c
            if best is None:break
            selected.append(best); cpt_used[best.cpt]+=1; thesis_used[best.thesis]+=1; player_used.update(best.players)
        if len(selected)==desired:return selected
    return []

def portfolio_report(rows,players,all_candidates=None):
    report={"lineups":len(rows),"captain_exposure":dict(Counter(c.cpt for c in rows)),"outcome_theses":dict(Counter(c.thesis for c in rows)),"player_exposure":dict(Counter(n for c in rows for n in c.players)),"quality":[round(lineup_quality(c,players),3) for c in rows]}
    if all_candidates is not None:
        report["captain_confidence"]=captain_confidence(players,all_candidates); report["captain_slot_plan"]=captain_slots(players,all_candidates,5)
    return report
