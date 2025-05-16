from datetime import datetime
import ntplib
import uvicorn
import os
from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse

CONFIG_DIR = "var/www/firmware/ztp/configs"

app = FastAPI()

def get_ntp_time(server="time.nist.gov"):
    client = ntplib.NTPClient()
    response = client.request(server, version=3)
    return datetime.fromtimestamp(response.tx_time).strftime("%Y-%m-%d_%H-%M-%S")

@app.put("/update")
async def update_config(id: str, content: str, version: str):
    #version = get_ntp_time()

    filepath = f"{CONFIG_DIR}/{id}/{version}/"

    print(filepath)

    os.makedirs(filepath, exist_ok=True)
    filename = filepath + "/network.uci"
    with open(filename, "w") as outfile:
        outfile.write(content)

    return {"message": f"Update {id} with {content}"}

@app.get("/provision")
async def provision_config(id: str, version: str = None):
    if version is None:  # Gets latest version if none specified
        version_list = os.listdir(f"{CONFIG_DIR}/{id}/")
        print(version_list)

        parsed_times = [datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S") for ts in version_list]

        latest_version = max(parsed_times)
        version = latest_version.strftime("%Y-%m-%d_%H-%M-%S")

    filepath = f"{CONFIG_DIR}/{id}/{version}/network.uci"
    print(filepath)

    if not filepath:
        raise HTTPException(status_code=404, detail="Config file not found")

    response = FileResponse(filepath, media_type="text/plain", filename=os.path.basename(filepath))
    response.headers["Config-Version"] = f"{version}"

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
