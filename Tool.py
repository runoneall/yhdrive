import json
import os
import shutil

folder = "./cache"

def CleanDir() -> None:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

def CutFile(TargetFilePath:str, TargetChunkSize:int) -> list:
    TargetChunkSize = TargetChunkSize * 1024 * 1024
    TargetFileSize = os.path.getsize(TargetFilePath)
    ChunksNum = TargetFileSize // TargetChunkSize + (1 if TargetFileSize % TargetChunkSize > 0 else 0)
    ChunkFileList = list()
    print('正在切片')
    with open(TargetFilePath, 'rb') as f:
        for i in range(ChunksNum):
            chunk_file_name = f"chunk_{i+1}"
            with open(f"{folder}/{chunk_file_name}", 'wb') as chunk_file:
                chunk_data = f.read(TargetChunkSize)
                chunk_file.write(chunk_data)
            print(f"切片 {chunk_file_name}")
            ChunkFileList.append(f"{folder}/{chunk_file_name}")
    return ChunkFileList

def MetaJsonMaker(FileName:str, ChunkItems:list[str], SavePath:str) -> None:
    meta = {
        'name': FileName,
        'chunks': ChunkItems
    }
    with open(SavePath, "w", encoding="utf-8") as metajson:
        json.dump(meta, metajson, ensure_ascii=False, indent=1)