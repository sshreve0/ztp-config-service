from datetime import datetime
from typing import Annotated
import ntplib
import os
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import FileResponse
import uci_parser as uci
import db
import auth
import uvicorn #included for testing

CONFIG_DIR = "../mnt/var/www/firmware/ztp/configs"

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_ntp_time():
    servers = ["time-a-b.nist.gov","time-b-b.nist.gov","time-c-b.nist.gov","time-d-b.nist.gov"]

    client = ntplib.NTPClient()
    for server in servers:
        try:
            response = client.request(server, version=3)
            return datetime.utcfromtimestamp(response.tx_time)
        except Exception as e:
            print(f"Failed to get time from {server}: {e}")
    raise RuntimeError("ERROR: All NTP servers failed.")

@app.put("/state")
async def set_state( mac: str, state: str):

    time = await get_ntp_time()
    time = time.strftime("%Y-%m-%d_%H-%M")
    #authenticated = auth.verify(mac, token, time)
    print("TIME: " + time)
    authenticated = True

    if not authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized")

    print(state)
    if state not in {"succeeded", "failed", "synced"}:
        raise HTTPException(status_code=400, detail="Invalid state: " + state)

    result = db.set_state(mac,state)
    print(result)

    return HTTPException(status_code=200,detail="Device state successfully updated.")

@app.put("/update")
async def update_config(token: Annotated[str, Depends(oauth2_scheme)],mac: str, version: str, content: str = Body()):

    time = (get_ntp_time().strftime("%Y-%m-%d_%H-%M"))
    authenticated = auth.verify(mac, token, time)

    if not authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized")

    loc = db.get_location_by_mac(mac)

    filepath = f"{CONFIG_DIR}/{loc}/{mac}/"
    content = uci.parse_file(content)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="No directory found for mac: " + mac)

    wholepath=f"{filepath}{version}/"

    os.makedirs(wholepath, exist_ok=True)
    filename = wholepath + "/configs.uci"
    with open(filename, "w") as outfile:
        outfile.write(content)

    return HTTPException(status_code=200,detail="Config successfully updated.")

@app.get("/provision")
async def provision_config(token: Annotated[str, Depends(oauth2_scheme)],mac: str, version: str = None):

    time = get_ntp_time().strftime("%Y-%m-%d_%H-%M")
    authenticated = auth.verify(mac, token, time)

    if not authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized")

    loc = db.get_location_by_mac(mac)

    filepath = f"{CONFIG_DIR}/{loc}/{mac}/"

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="No directory found for mac: " + mac)

    if version is None:  # Gets latest version if none specified
        version_list = os.listdir(filepath)
        if len(version_list) == 0:
            raise HTTPException(status_code=404, detail="No versions found for mac: " + mac)

        parsed_times = [datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S") for ts in version_list]

        latest_version = max(parsed_times)
        version = latest_version.strftime("%Y-%m-%d_%H-%M-%S")

    fullpath = f"{filepath}/{version}/configs.uci"
    if not os.path.exists(fullpath):
        raise HTTPException(status_code=404, detail="Config not found.")

    response = FileResponse(fullpath, media_type="text/plain", filename=os.path.basename(fullpath))
    response.headers["Config-Version"] = f"{version}"

    return response

#if __name__ == '__main__':
#    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
