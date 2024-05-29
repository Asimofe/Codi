from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import model  # 모델 로딩과 생성 함수가 정의된 파일

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용, 보안을 위해 실제 도메인으로 제한하는 것이 좋습니다.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

class InputData(BaseModel):
    code: str

@app.post("/generate")
async def generate_code(data: InputData):
    try:
        prompt = (
            "Here is a Python function with an error:\n\n"
            f"{data.code}\n\n"
            "Fix the above code and provide the corrected version within the following markers:\n"
        )
        # f"Here is a Python function with an error:\n\n{data.code}\n\nFix the code."
        generated_code = model.generate_code(prompt)

        # 특정 문장 이후의 텍스트를 추출
        start_marker = "Fix the above code and provide the corrected version within the following markers:\n"
        start_index = generated_code.find(start_marker)
        if start_index != -1:
            relevant_code = generated_code[start_index + len(start_marker):].strip()
        else:
            relevant_code = generated_code.strip()

        return {"generated_code": relevant_code}
        #return {"generated_code": generated_code}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory")
async def get_memory():
    try:
        memory_footprint = model.get_memory_footprint()
        return {"memory_footprint_MB": memory_footprint}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)
