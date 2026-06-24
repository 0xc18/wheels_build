import tarfile
import zipfile
import requests
from pathlib import Path

package = "maturin"
version = "1.14.1"

# Get metadata for the specific version
resp = requests.get(
    f"https://pypi.org/pypi/{package}/{version}/json"
)
resp.raise_for_status()
data = resp.json()

# Find the source distribution
sdist = next(
    f for f in data["urls"]
    if f["packagetype"] == "sdist"
)

filename = sdist["filename"]
url = sdist["url"]

# Download
archive = Path(filename)
with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with archive.open("wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

# Extract
if filename.endswith((".tar.gz", ".tgz")):
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall()
elif filename.endswith(".zip"):
    with zipfile.ZipFile(archive) as z:
        z.extractall()
else:
    raise RuntimeError(f"Unsupported archive type: {filename}")

print(f"Downloaded and extracted {filename}")
