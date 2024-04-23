from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
# from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from PIL import Image
import utils, engine
import os
import time

app = FastAPI()

# 允许所有来源
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 确保 images 目录存在
os.makedirs("./images", exist_ok=True)
# 证件照背景颜色值
BACKGROUND_COLOR = {
    'RED': (255, 0, 0, 255),
    'BLUE': (67, 142, 219, 255),
    'WHITE': (255, 255, 255, 255)
}

@app.post("/idCardGenerator")
async def id_card_generator(
    file: UploadFile = File(...),
    backColor: str = Form(...),
    width: int = Form(...),  # 确保这里声明了 width 和 height
    height: int = Form(...)
):
    try:
        # 读取文件内容
        contents = await file.read()
        upload_file_ext = file.filename.split(".")[-1]
        upload_file_name = utils.generate_unique_id() + "." + upload_file_ext
        upload_file_path = os.path.join("./images", upload_file_name)
        with open(upload_file_path, "wb") as f:
            f.write(contents)

        input_image = Image.open(upload_file_path)
        img_pil = engine.remove_bg_mult(input_image)
        
        # 使用表单数据中的尺寸设置图片大小
        img_pil = img_pil.resize((width, height))
        
        # 从 BACKGROUND_COLOR 字典中获取颜色值
        color = BACKGROUND_COLOR.get(backColor.upper(), (255, 255, 255, 255))
        
        # 创建一个新的背景图片
        background = Image.new("RGBA", (width, height), color)
        
        # 将去除背景的图片粘贴到背景图片上
        background.paste(img_pil, (0, 0), img_pil.convert("RGBA"))  # 确保使用 RGBA 模式进行遮罩
        
        output_file_name = "out_" + utils.generate_unique_id() + ".png"
        output_file_path = os.path.join("./images", output_file_name)
        background.save(output_file_path)
        
        # 返回图片文件
        return FileResponse(output_file_path, media_type="image/png", filename=output_file_name)
    except Exception as e:
        # 如果发生错误，返回错误信息的 JSON 响应
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to upload file", "error": str(e)}
        )
            