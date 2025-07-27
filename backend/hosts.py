import re
import sqlite3
from typing import Annotated

from fastapi import Depends
from fastapi import Response, APIRouter

from dependencies import get_current_active_user
from models import User
from scans import scan

database = "data/sqlite.db"

with sqlite3.connect(database) as con:
    con.execute("CREATE TABLE IF NOT EXISTS hosts(hostname, state, description)")
    if not con.execute("SELECT 1 FROM hosts WHERE hostname=?", ("scanme.nmap.org",)).fetchone():
        con.execute("INSERT INTO hosts VALUES(?,?,?)", ("scanme.nmap.org", 1, "test host"))
    if not con.execute("SELECT 1 FROM hosts WHERE hostname=?", ("testphp.vulnweb.com",)).fetchone():
        con.execute("INSERT INTO hosts VALUES(?,?,?)", ("testphp.vulnweb.com", 1, "test host"))
    if not con.execute("SELECT 1 FROM hosts WHERE hostname=?", ("testhtml5.vulnweb.com",)).fetchone():
        con.execute("INSERT INTO hosts VALUES(?,?,?)", ("testhtml5.vulnweb.com", 1, "test host"))
    if not con.execute("SELECT 1 FROM hosts WHERE hostname=?", ("testasp.vulnweb.com",)).fetchone():
        con.execute("INSERT INTO hosts VALUES(?,?,?)", ("testasp.vulnweb.com", 1, "test host"))
    if not con.execute("SELECT 1 FROM hosts WHERE hostname=?", ("testaspnet.vulnweb.com",)).fetchone():
        con.execute("INSERT INTO hosts VALUES(?,?,?)", ("testaspnet.vulnweb.com", 1, "test host"))
    if not con.execute("SELECT 1 FROM hosts WHERE hostname=?", ("rest.vulnweb.com",)).fetchone():
        con.execute("INSERT INTO hosts VALUES(?,?,?)", ("rest.vulnweb.com", 1, "test host"))
    if not con.execute("SELECT 1 FROM hosts WHERE hostname=?", ("vulnweb.com",)).fetchone():
        con.execute("INSERT INTO hosts VALUES(?,?,?)", ("vulnweb.com", 1, "test host"))

router = APIRouter()


@router.post(
    "/hosts",
    summary="Добавить новый хост",
    tags=["Управление хостами"]
)
async def add_host(
        hostname: str,
        state: bool,
        description: str,
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    hostname = re.sub(r"[^a-zA-Z0-9.-]", "", hostname)
    description = re.sub(r"[^a-zA-Zа-яА-Я0-9\s.,-]", "", description)
    with sqlite3.connect(database) as con:
        if con.execute("SELECT 1 FROM hosts WHERE hostname=?", (hostname,)).fetchone():
            return {"error": "Hostname exists"}
        con.execute("INSERT INTO hosts VALUES(?,?,?)", (hostname, state, description))
    return {"hostname": hostname, "status": state, "description": description, "modifiedby": current_user.username}


@router.get(
    "/hosts",
    summary="Получить список всех хостов",
    tags=["Управление хостами"]
)
async def get_hosts(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    with sqlite3.connect(database) as con:
        return {"hosts": con.execute("SELECT hostname,state,description FROM hosts").fetchall(),
                "modifiedby": current_user.username}


@router.get(
    "/metrics",
    summary="Получить метрики в Prometheus-формате",
    tags=["Мониторинг"]
)
async def metrics():
    with sqlite3.connect(database) as con:
        hosts = [r[0] for r in con.execute("SELECT hostname FROM hosts WHERE state=1").fetchall()]
    if not hosts: return {"error": "Hosts not found"}
    result = await scan(hosts)
    return Response(content=result, media_type="text/plain")

@router.post(
    "/hosts/{hostname}/toggle",
    summary="Откл./вкл. сканирование хоста",
    tags=["Управление хостами"]
)
async def toggle_host_status(
        hostname: str,
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    with sqlite3.connect(database) as con:
        res = con.execute("SELECT state FROM hosts WHERE hostname=?", (hostname,)).fetchone()
        if not res: return {"error": "Host not found"}
        con.execute("UPDATE hosts SET state=? WHERE hostname=?", (not res[0], hostname))
    return {"hostname": hostname, "new_state": not res[0], "modifiedby": current_user.username}
