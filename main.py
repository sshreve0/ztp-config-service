from datetime import datetime
import ntplib
import uvicorn
import os
from fastapi import FastAPI, HTTPException, Body
from starlette.responses import FileResponse
import uci_parser as uci

CONFIG_DIR = "var/www/firmware/ztp/configs"

app = FastAPI()

def get_ntp_time(server="time.nist.gov"): # unused right now
    client = ntplib.NTPClient()
    response = client.request(server, version=3)
    return datetime.fromtimestamp(response.tx_time).strftime("%Y-%m-%d_%H-%M-%S")

@app.put("/update")
async def update_config(mac: str, version: str, content: str = Body()):
    filepath = f"{CONFIG_DIR}/{mac}/" #will never exist
    content = uci.parse_file(content)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="No directory found for mac: " + mac)

    wholepath=f"{filepath}{version}/"

    os.makedirs(wholepath, exist_ok=True)
    filename = wholepath + "/network.uci"
    with open(filename, "w") as outfile:
        outfile.write(content)

    return HTTPException(status_code=200,detail="Config successfully updated.")

@app.get("/provision")
async def provision_config(mac: str, version: str = None):

    if not os.path.exists(f"{CONFIG_DIR}/{mac}/"):
        raise HTTPException(status_code=404, detail="No directory found for mac: " + mac)

    if version is None:  # Gets latest version if none specified
        version_list = os.listdir(f"{CONFIG_DIR}/{mac}/")
        if len(version_list) == 0:
            raise HTTPException(status_code=404, detail="No versions found for mac: " + mac)

        parsed_times = [datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S") for ts in version_list]

        latest_version = max(parsed_times)
        version = latest_version.strftime("%Y-%m-%d_%H-%M-%S")

    filepath = f"{CONFIG_DIR}/{mac}/{version}/network.uci"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Config not found.")


    response = FileResponse(filepath, media_type="text/plain", filename=os.path.basename(filepath))
    response.headers["Config-Version"] = f"{version}"

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
