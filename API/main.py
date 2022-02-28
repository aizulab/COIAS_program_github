from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
import os
import subprocess
import shutil
import pathlib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
IMAGE_PATH = pathlib.Path("/opt/tmp_images")
origins = [
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="ファイルアップロード確認用")
async def main():
    """
    [localhost](http://localhost:8000/)
    """
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.get("/disp", summary="disp.txtを配列で取得")
def get_disp():
    disp_path = IMAGE_PATH / "disp.txt"
    with disp_path.open() as f:
        l = f.read().split()
    l = split_list(l, 4)

    return {"result": l}


def split_list(l, n):
    """
    リストをサブリストに分割する
    :param l: リスト
    :param n: サブリストの要素数
    :return: 
    """
    for idx in range(0, len(l), n):
        yield l[idx : idx + n]


@app.post("/uploadfiles/", summary="fileアップロード", tags=["files"])
async def create_upload_files(files: list[UploadFile]):
    """
    __参考__
    - [Request Files - FastAPI](https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile)
    - [フォーム – React](https://ja.reactjs.org/docs/forms.html)
    """

    # pathlibでpathの操作
    image_path = pathlib.Path("/opt/tmp_images")

    # ディレクトリがなければつくる
    image_path.mkdir(exist_ok=True)

    # fileを保存
    for file in files:

        tmp_path = image_path / file.filename

        try:
            with tmp_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                print(tmp_path)

        finally:
            file.file.close()

    return {"status_code": 200}


@app.delete("/deletefiles", summary="imageディレクトリ削除", tags=["files"])
def run_deletefiles():

    shutil.rmtree(IMAGE_PATH)

    return {"status_code": 200}


@app.put("/preprocess", summary="最新のMPCデータを取得", tags=["command"])
def run_preprocess():

    subprocess.run(["preprocess"])

    return {"status_code": 200}


@app.put("/startsearch2R", summary="ビギニング&マスク", tags=["command"])
def run_startsearch2R():

    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["startsearch2R"])

    return {"status_code": 200}


@app.put("/fits2png", summary="画像変換", tags=["command"])
def run_fits2png():
    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["fits2png"])

    return {"status_code": 200}


@app.put("/findsource", summary="光源検出", tags=["command"])
def run_findsource():

    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["findsource"])

    return {"status_code": 200}


@app.put("/prempsearchC", summary="精密軌道取得", tags=["command"])
def run_prempsearchC():

    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["prempsearchC"])

    return {"status_code": 200}


@app.put("/astsearch_new", summary="自動検出", tags=["command"])
def run_astsearch_new():

    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["astsearch_new"])

    return {"status_code": 200}


@app.put("/AstsearchR", summary="全自動処理", tags=["command"])
def run_AstsearchR(size: int = 4):

    if size != 2 and size != 4:
        raise HTTPException(status_code=400)
    else:
        size = str(size)

    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["AstsearchR"], input=size, encoding="UTF-8")

    return {"status_code": 200}


@app.put("/prempedit", summary="出力ファイル整形1", tags=["command"])
def run_prempedit():

    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["prempedit"])

    return {"status_code": 200}


@app.put("/prempedit3", summary="出力ファイル整形2", tags=["command"])
def run_prempedit3():

    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["python", "prempedit3.py"])

    return {"status_code": 200}


@app.put("/redisp", summary="再描画による確認作業", tags=["command"])
def run_redisp():

    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["redisp"])

    return {"status_code": 200}


@app.put("/Astsearch_afterReCOIAS", summary="再描画による確認作業", tags=["command"])
def run_Astsearch_afterReCOIAS():

    os.chdir(IMAGE_PATH.as_posix())
    subprocess.run(["Astsearch_afterReCOIAS"])

    return {"status_code": 200}
